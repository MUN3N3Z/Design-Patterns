from board import Board
from worker import Worker
from player import Player, HumanStrategy
from stack import StateObject, StateStack

class PromptState:
    next_state = 1
    def __init__(self, manager, prompt_function, secondary_function=None):
        self._manager = manager
        self._prompt = prompt_function
        self._check = secondary_function
        self._index = PromptState.next_state
        if PromptState.next_state == 5:
            PromptState.next_state = 0
        else:
            PromptState.next_state += 1

    def process_state(self, piece):
        result = self._prompt()
        if self._check != None:
            self._check(piece, result)
        self._update_state()
        return (result, self._index)

    def update_checks(self, check):
        self._check = check
    
    def _update_state(self):
        self._manager.current_prompt = self._manager._prompts[self._index]

class Manager:
    def __init__(self, white_player: str, blue_player: str, enable_redo_undo: bool, enable_score: bool) -> None:
        self._board = Board()
        
        self._players = (self._create_player("white", white_player), self._create_player("blue", blue_player))

        self._prompts = [PromptState(self, self._players[0].pick_worker), PromptState(self, self._players[0].pick_move, self._board.check_move), PromptState(self, self._players[0].pick_build, self._board.check_build),
                         PromptState(self, self._players[1].pick_worker), PromptState(self, self._players[1].pick_move, self._board.check_move), PromptState(self, self._players[1].pick_build, self._board.check_build)]
        
        self.current_prompt = self._prompts[0]

        self._current_player = 0

        self._state_stack = StateStack()

        self._worker_ownership = {"A": self._players[0].workers[0], 
                                  "B": self._players[0].workers[1],
                                  "Y": self._players[1].workers[0],
                                  "Z": self._players[1].workers[1]}

        self._valid_workers = self.players[0].worker_names + self.players[1].worker_names

        self._enable_redo_undo = enable_redo_undo
        self._enable_score = enable_score

        self._turn = 1
        self._game_over = False

    def _create_player(self, player_name:str, player_type:str) -> Player:
        """ Create players based on their types """
        return Player(player_name, self._board, player_type)
    
    @property
    def current_player(self):
        return self._players[self._current_player]
    
    @property
    def players(self):
        return self._players
    
    @property
    def board(self):
        return self._board

    def _check_board_for_win(self):
        self.game_over = self._board.check_winner()
    
    def update_turn(self):
        # Update turn count and current player
        self._turn += 1
        self._current_player = 0 if (self._turn % 2 != 0) else 1
        self._board.update_board()
        for player in self._players:
            for worker in player.workers:
                self.evaluate_moves(worker)
        self._check_board_for_win()

    def evaluate_moves(self, worker: Worker):
        valid = False
        for direction in Board.valid_directions:
            valid = valid or self._board.check_move(worker.name, direction, False)
        worker.has_valid_moves = valid

    def reset(self):
        # self._board = Board()
        # self._update_prompts()
        # self._current_prompt = self._prompts[0]
        # self._current_player = 0
        # self._turn = 1
        # self.game_over = False
        reset_state = self._state_stack.reset()
        self._update_state(reset_state)
        for player in self._players:
            for worker in player.workers:
                worker.has_valid_moves = True

    def print_board(self):
        """ Print current state of the board on the terminal"""
        print(self._board)
        player = self._players[0].name if self._turn % 2 != 0 else self._players[1].name
        workers = ("".join(self._players[0].worker_names)) if (self._turn % 2 != 0) else ("".join(self._players[1].worker_names))
        turn_text = f"Turn: {self._turn}, {player} ({workers})"
        if self._enable_score:
            turn_text += f", {self._players[self._current_player].score}"
        print(turn_text)

    def prompt_player(self):
        """Function that handles the logic of prompting the player
           and outputting game-specific information."""
        p11, p12, p21, p22 = self._board.worker_positions['A'], self._board.worker_positions['B'], self._board.worker_positions['Y'], self._board.worker_positions['Z']
        saved_board = Board(p11, p12, p21, p22, self._board.levels)
        self._state_stack.push(StateObject(saved_board, self.current_prompt, self._turn, self._current_player, self._game_over))
        
        if self._enable_redo_undo and (type(self._players[0]._strategy) == HumanStrategy or type(self._players[1]._strategy) == HumanStrategy):
            while True:
                response = input("undo, redo, or next\n")
                if response == "undo":
                    if len(self._state_stack) > 1:
                        self._state_stack.undo()
                        self._update_state(self._state_stack.current())
                    elif len(self._state_stack) == 1:
                        self._update_state(self._state_stack.current())
                    self.print_board()
                elif response == "redo":
                    if len(self._state_stack.popped_states) > 0:
                        self._state_stack.redo()
                        self._update_state(self._state_stack.current())
                    self.print_board()
                elif response == "next":
                    self._state_stack.next()
                    break

        piece = None

        # use the state pattern to get input from the player
        while True:
            result = self.current_prompt.process_state(piece)
            if result[1] == 1 or result[1] == 4: # if the next state is a move state, we just got back the piece
                piece = result[0]
            elif result[1] == 2 or result[1] == 5: # if the next state is a build state, we just got back the move
                move = result[0]
            elif result[1] == 3 or result[1] == 0: # if the next state is a piece state, we just got back the build
                build = result[0]
                break
        
        summary = f"{piece},{move},{build}"
        
        if self._enable_score:
            summary += f" {self._players[self._current_player].score}"

        print(summary)

    def _update_state(self, state_object):
        p11, p12, p21, p22 = state_object.board.worker_positions['A'], state_object.board.worker_positions['B'], state_object.board.worker_positions['Y'], state_object.board.worker_positions['Z']
        saved_board = Board(p11, p12, p21, p22, state_object.board.levels)
        self._board = saved_board
        self._update_prompts()
        for player in self._players:
            player.board = state_object.board
        self.current_prompt = state_object.current_prompt
        self._turn = state_object.turn
        self._current_player = state_object.current_player
        self._game_over = state_object.game_over

    def _update_prompts(self):
        self._prompts[1].update_checks(self._board.check_move)
        self._prompts[2].update_checks(self._board.check_build) 
        self._prompts[4].update_checks(self._board.check_move)
        self._prompts[5].update_checks(self._board.check_build)

    def check_if_game_over(self):
        if self._game_over:
            self._determine_winner()
        # else if the current player has no valid moves, determine the winner
        else:
            workers = self._players[self._current_player].workers
            if (workers[0].has_valid_moves or workers[1].has_valid_moves) == False:
                self._determine_winner()
    
    def _determine_winner(self):
        if self._current_player == 0:
            print(self._players[1].name + " has won")
        elif self._current_player == 1:
            print(self._players[0].name + " has won")

        play_again = input("Play again?\n")
        if play_again == "yes":
            self.reset()
        else:
            exit(0)