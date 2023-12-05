class Worker:
    valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
    def __init__(self, name:str) -> None:
        self._name = name
        self.has_valid_moves = True
    
    def get_name(self):
        return self._name