from board import Board
from worker import Worker
from player import Player, HumanPlayer, HeuristicPlayer, RandomPlayer

class Manager:
    def __init__(self, white_player: str, blue_player: str, enable_redo_undo: bool, enable_score: bool) -> None:
        self._board = Board()
        
        self._players = (self._create_player("white", white_player), self._create_player("blue", blue_player))

        self._current_player = 0

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
        if (player_type == "human"):
            return HumanPlayer(player_name, self._board)
        elif (player_type == "heuristic"):
            return HeuristicPlayer(player_name, self._board)
        else:
            return RandomPlayer(player_name, self._board)
    
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
        self._board = Board()
        self._turn = 1
        self.game_over = False
        self._current_player = 0

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
        
        # Request desired piece from human player
        piece = self._players[self._current_player].pick_worker()
        
        # Request move direction from human player
        move = self._players[self._current_player].pick_move()
        self._board.check_move(piece, move)
        
        # Request a build direction from human player
        build = self._players[self._current_player].pick_build()
        self._board.check_build(piece, build)
        
        summary = f"{piece},{move},{build}"
        
        if self._enable_score:
            summary += f" {self._players[self._current_player].score}"
            
        print(summary)

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