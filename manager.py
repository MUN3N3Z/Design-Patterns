
class Manager:
    white_player = ["A", "B"]
    blue_player = ["Y", "Z"]
    def __init__(self,enable_redo_undo, enable_score, player=white_player) -> None:
        self._current_player = Manager.white_player
        self._enable_redo_undo = enable_redo_undo
        self._enable_score = enable_score
        # Keep track of player turns
        self._turn = 1
        
    def get_current_player(self):
        return self._current_player
    
    def get_turn_number(self):
        return self._turn
    
    def update_turn(self):
        # Update turn count and current player
        self._turn += 1
        self._current_player = Manager.white_player if (self._turn % 2 != 0) else Manager.blue_player
        
    def check_move(worker, direction):
        pass