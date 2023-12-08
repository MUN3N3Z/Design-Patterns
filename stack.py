class StateObject:
    def __init__(self, board, current_prompt, turn, current_player, game_over_flag) -> None:
        self.board = board
        self.current_prompt = current_prompt
        self.turn = turn
        self.current_player = current_player
        self.game_over = game_over_flag
    
    

class StateStack:
    def __init__(self):
        self.states = []
        self.popped_states = []

    def __len__(self):
        return len(self.states)

    def push(self, state):
        self.states.append(state)

    def undo(self):
        popped = self.states.pop()
        self.popped_states.append(popped)
    
    def redo(self):
        popped = self.popped_states.pop()
        self.states.append(popped)

    def next(self):
        self.popped_states = []

    def current(self):
        return self.states[-1]