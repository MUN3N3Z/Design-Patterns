from board import Board
from player import Player
from worker import Worker
from player import HumanPlayer, HeuristicPlayer, RandomPlayer

class Manager:
    valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
    def __init__(self, white_player, blue_player, enable_redo_undo=False, enable_score=False) -> None:
        self._players = (self._create_player("white", white_player), self._create_player("blue", blue_player))

        self._current_player = 0

        self._worker_ownership = {"A": self._players[0].get_workers()[0], 
                                  "B": self._players[0].get_workers()[1],
                                  "Y": self._players[1].get_workers()[0],
                                  "Z": self._players[1].get_workers()[1]}

        self._valid_workers = self.get_players()[0].get_worker_names() + self.get_players()[1].get_worker_names()

        self._enable_redo_undo = enable_redo_undo
        self._enable_score = enable_score

        self._board = Board()

        self._turn = 1
        self._game_over = False

    def _create_player(player_name:str, player_type:str) -> Player:
        """ Create players based on their types """
        if (player_type == "human"):
            return HumanPlayer(player_name)
        elif (player_type == "heuristic"):
            return HeuristicPlayer(player_name)
        else:
            return RandomPlayer(player_name)
        
    def get_current_player(self):
        return self._players[self._current_player]
    
    def get_players(self):
        return self._players
    
    def get_board(self):
        return self._board

    def _check_board_for_win(self):
        self.game_over = self._board.check_winner()
    
    def update_turn(self):
        # Update turn count and current player
        self._turn += 1
        self._current_player = 0 if (self._turn % 2 != 0) else 1
        self._board.update_board()
        for player in self._players:
            for worker in player.get_workers():
                self.evaluate_moves(worker)
        self._check_board_for_win()

    def evaluate_moves(self, worker: Worker):
        valid = False
        for direction in Manager.valid_directions:
            valid = valid or self._board.check_move(worker.get_name(), direction, False)
        worker.has_valid_moves = valid

    def reset(self):
        self._board = Board()
        self._turn = 1
        self.game_over = False
        self._current_player = 0

    def print_board(self):
        """ Print current state of the board on the terminal"""
        print(self._board)
        player = self._players[0].get_name() if self._turn % 2 != 0 else self._players[1].get_name()
        workers = ("".join(self._players[0].get_worker_names())) if (self._turn % 2 != 0) else ("".join(self._players[1].get_worker_names()))
        print(f"Turn: {self._turn}, {player} ({workers})")

    def prompt_player(self):
        """Function that handles the logic of prompting the player
           and outputting game-specific information."""
        # Request desired piece from human player
        while True:
            piece = self._players[self._current_player].pick_worker()
            if piece not in self._valid_workers:
                print("Not a valid worker")
                return False
            elif piece not in self._players[self._current_player].get_worker_names():
                print("That is not your worker")
                return False
            elif not self._worker_ownership[piece].has_valid_moves:
                print("That worker cannot move")
                return False
            else:
                break
        
        # Request move direction from human player
        while True:
            move = self._players[self._current_player].pick_move()
            if move not in Manager.valid_directions:
                print("Not a valid direction")
            elif not self._board.check_move(piece, move):
                print(f"Cannot move {move}")
            else:
                break
        
        # Request a build direction from human player
        while True:
            build = self._players[self._current_player].pick_build()
            if build not in Manager.valid_directions:
                print("Not a valid direction")
            # check if can build in direction
            elif not self._board.check_build(piece, build):
                print(f"Cannot build {build}")
            else:
                break
            
        print(piece + "," + move + "," + build)

    def check_if_game_over(self):
        if self._game_over:
            self._determine_winner()
        # else if the current player has no valid moves, determine the winner
        else:
            workers = self._players[self._current_player].get_workers()
            if (workers[0].has_valid_moves or workers[1].has_valid_moves) == False:
                self._determine_winner()
    
    def _determine_winner(self):
        if self._current_player == 0:
            print(self._players[1].get_name() + " has won")
        elif self._current_player == 1:
            print(self._players[0].get_name() + " has won")

        play_again = input("Play again?\n")
        if play_again == "yes":
            self.reset()
        else:
            exit(0)