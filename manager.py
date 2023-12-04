from board import Board

class Manager:
    white_player = ["A", "B"]
    blue_player = ["Y", "Z"]
    def __init__(self, enable_redo_undo=False, enable_score=False, player=white_player) -> None:
        self._current_player = player
        self._enable_redo_undo = enable_redo_undo
        self._enable_score = enable_score
        self._board = Board()
        # Keep track of player turns
        self._turn = 1
        self.game_over = False
        
    def get_current_player(self):
        return self._current_player
    
    def get_turn_number(self):
        return self._turn
    
    def get_board(self):
        return self._board

    def _check_board_for_win(self):
        self.game_over = self._board.check_winner()
    
    def update_turn(self):
        # Update turn count and current player
        self._turn += 1
        self._current_player = Manager.white_player if (self._turn % 2 != 0) else Manager.blue_player
        self._board.update_board()
        self._check_board_for_win()

    def reset(self):
        self._board = Board()
        self._turn = 1
        self.game_over = False
        self._current_player = Manager.white_player