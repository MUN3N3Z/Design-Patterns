from worker import Worker
from manager import Manager
import random

class Player:
    def __init__(self, name:str) -> None:
        self._player_name = name
        self._workers = (Worker('A'), Worker('B')) if name == "white" else (Worker('Y'), Worker('Z'))
        
    def get_name(self):
        return self._player_name

    def get_workers(self):
        return self._workers
    
    def get_worker_names(self):
        """Returns the Player's workers 
           as an array of strings"""
        workers_list = []
        for worker in self._workers:
            workers_list.append(worker._name)

        return workers_list

class HumanPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def pick_worker(self):
        return input("Select a worker to move\n")
    
    def pick_move(self):
        return input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")

    def pick_build(self):
        return input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")

    
class HeuristicPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.score = (0, 0, 0)

    def calculate_center_score(self, position):        
        if position % 5 == 0 or position % 5 == 4 or (position >= 0 and position <= 4) or (position >= 20 and position <= 24):
            return 0
        elif position >= 6 and position <= 18 and position != 12:
            return 1
        else:
            return 2

    def pick_worker(self):
        for worker in self._workers:
            for direction in Manager.valid_directions:
                # score in all three categories, append to a list of scores
                break
            break
        # get the max score, store the scores/best move, and return the best worker
        pass

    def pick_move(self):
        pass

    def pick_build(self):
        pass
    
class RandomPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def pick_worker(self):
        return self._workers[random.randint(0, 1)]
    
    def pick_move(self):
        return Manager.valid_directions[random.randint(0, 7)]
    
    def pick_build(self):
        return Manager.valid_directions[random.randint(0, 7)]