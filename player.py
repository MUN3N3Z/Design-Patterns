from worker import Worker

class Player:
    def __init__(self, name:str) -> None:
        self._player_name = name
        self._workers = [Worker('A'), Worker('B')] if name == "white_player" else [Worker('Y'), Worker('Z')]
        