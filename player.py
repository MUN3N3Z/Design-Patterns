from worker import Worker
from board import Board
import random

class Player:
    def __init__(self, name:str, board: Board) -> None:
        self._player_name = name
        self._workers = (Worker('A'), Worker('B')) if name == "white" else (Worker('Y'), Worker('Z'))
        self._board = board
        self.score = (0, 0, 0)
        self._chosen_worker = ""

    @property
    def name(self):
        return self._player_name

    @property
    def workers(self):
        return self._workers
    
    @property
    def worker_names(self):
        """Returns the Player's workers 
           as an array of strings"""
        workers_list = []
        for worker in self._workers:
            workers_list.append(worker.name)

        return workers_list
    
    def calculate_center_score(self, position: int):        
        if position % 5 == 0 or position % 5 == 4 or (position >= 0 and position <= 4) or (position >= 20 and position <= 24):
            return 0
        elif position >= 6 and position <= 18 and position != 12:
            return 1
        else:
            return 2

    def calculate_distance_score(self, position: int, board: Board, player: bool):
        if player:
            letter1 = "Y"
            letter2 = "Z"
        else:
            letter1 = "A"
            letter2 = "B"
        # get self coordinates
        pos_x = int(position / 5)
        pos_y = position % 5
        # get the first enemy worker's coordinates
        enemy1_x = int(board.worker_positions[letter1] / 5)
        enemy1_y = board.worker_positions[letter1] % 5
        # get the second enemy worker's coordinates
        enemy2_x = int(board.worker_positions[letter2] / 5)
        enemy2_y = board.worker_positions[letter2] % 5
        # calculate the difference between the coordinates and return the min subtracted from 8
        dist1 = abs(pos_x - enemy1_x + pos_y - enemy1_y)
        dist2 = abs(pos_x - enemy2_x + pos_y - enemy2_y)
        return (8 - min(dist1, dist2))

    def calculate_height_score(self, position: int, board: Board):
        """ Returned weighted height score of a worker """
        return board.levels[position]
    
    def calculate_stats(self, worker, direction):
        other_worker_name = self._workers[1].name if worker == 0 else self._workers[0].name
        other_worker_position = self._board.worker_positions[other_worker_name]
        if self._board.check_move(worker, direction, False):
            new_position = Board.address_translations[direction] + self._board.worker_positions[worker]
            player = True if self._player_name == "white" else False
            # Calculate score for each player's workers
            center_score = self.calculate_center_score(new_position) + self.calculate_center_score(other_worker_position)
            height_score = self.calculate_height_score(new_position, self._board) + self.calculate_height_score(other_worker_position, self._board)
            distance_score = self.calculate_distance_score(new_position, self._board, player) + self.calculate_distance_score(other_worker_position, self._board, player)
            self.score = (center_score, height_score, distance_score)
            return self.score
        else:
            return (-1, -1, -1)

class HumanPlayer(Player):
    def __init__(self, name: str, board: Board) -> None:
        super().__init__(name, board)
    
    def pick_worker(self):
        while True:
            piece = input("Select a worker to move\n")
            
            if piece == "A" or piece == "Y":
                index = 0
            elif piece == "B" or piece == "Z":
                index = 1

            if piece not in ["A", "B", "Y", "Z"]:
                print("Not a valid worker")
            elif piece not in self.worker_names:
                print("That is not your worker")
            elif not self._workers[index].has_valid_moves:
                print("That worker cannot move")
            else:
                break
        self._chosen_worker = piece
        return piece
    
    def pick_move(self):
        while True:
            move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if move not in Board.valid_directions:
                print("Not a valid direction")
            elif not self._board.check_move(self._chosen_worker, move, False):
                print(f"Cannot move {move}")
            else:
                break
        self.score = self.calculate_stats(self._chosen_worker, move)
        return move

    def pick_build(self):
        while True:
            build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if build not in Board.valid_directions:
                print("Not a valid direction")
            # check if can build in direction
            elif not self._board.check_build(self._chosen_worker, build):
                print(f"Cannot build {build}")
            else:
                break
        return build

    
class HeuristicPlayer(Player):
    def __init__(self, name: str, board: Board) -> None:
        super().__init__(name, board)
        self._next_move = ""

    def pick_worker(self):
        options = [0 for i in range(0, 16)]
        scores = [(0, 0, 0) for i in range(0, 16)]
        for worker in range(0, 2):
            new_worker_name = self._workers[worker].name
            
            for direction in range(0, 8):
                new_direction = Board.valid_directions[direction]
                #  Translate new 2-d proposed position to 1-d
                height_score, center_score, distance_score = self.calculate_stats(new_worker_name, new_direction)

                options[8 * (worker) + direction] = 3 * height_score + 2 * center_score + 1 * distance_score
                scores[8 * (worker) + direction] = (height_score, center_score, distance_score)
        
        best_move = max(options)
        best_index = options.index(best_move)

        if best_index < 8:
            # return the 0 worker
            worker = 0
        else:
            # return the 1 worker
            worker = 1

        self.score = scores[best_index]
        self._next_move = best_index % 8
        self._chosen_worker = self._workers[worker].name
        
        return self._chosen_worker
    
    def pick_move(self):
        return Board.valid_directions[self._next_move]

    def pick_build(self):
        while True:
            random_direction = Board.valid_directions[random.randint(0, 7)]
            if self._board.check_build(self._chosen_worker, random_direction, False):
                return random_direction
    
class RandomPlayer(Player):
    def __init__(self, name: str, board: Board) -> None:
        super().__init__(name, board)
    
    def pick_worker(self):
        while True:
            random_worker = self._workers[random.randint(0, 1)]
            if random_worker.has_valid_moves:
                self._chosen_worker = random_worker.name
                return random_worker.name
    
    def pick_move(self):
        while True:
            random_direction = Board.valid_directions[random.randint(0, 7)]
            if self._board.check_move(self._chosen_worker, random_direction, False):
                self.score = self.calculate_stats(self._chosen_worker, random_direction)
                return random_direction
    
    def pick_build(self):
        while True:
            random_direction = Board.valid_directions[random.randint(0, 7)]
            if self._board.check_build(self._chosen_worker, random_direction, False):
                return random_direction
