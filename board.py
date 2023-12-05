from worker import Worker

class Board:
    # translations from cardinal directions to array 
    # index offsets in our 5x + y coordinate system
    address_translations = {
            'n': -5, 
            'ne': -4, 
            'e': 1, 
            'se': 6, 
            's': 5, 
            'sw': 4, 
            'w': -1, 
            'nw': -6
        }
    
    # arrays containing the east and west directions for bound checking
    east_directions = ["e", "ne", "se"]
    west_directions = ["w", "nw", "sw"]
    def __init__(self, p11=16, p12=8, p21=6, p22=18):
        # Keep track of cell levels and worker locations
        self._levels = [0 for i in range(0, 25)]
        self._workers = {
            'A': p11,
            'B': p12,
            'Y': p21,
            'Z': p22,
        }
        self._board = self._draw()

    def __repr__(self):
        return self._board

    def _draw(self):
        """draw takes in four worker positions as ints
           as well as an array of all the spaces' levels
           and returns the drawn ASCII board"""
        board = ""
        for i in range(0, 5):
            board += "+--+--+--+--+--+\n"
            for j in range(0, 5):
                # convert the index 
                index = 5 * i + j
                board += "|"
                board += str(self._levels[index])
                if index in self._workers.values():    
                    if index == self._workers['A']:
                        board += "A"
                    elif index == self._workers['B']:
                        board += "B"
                    elif index == self._workers['Y']:
                        board += "Y"
                    elif index == self._workers['Z']:
                        board += "Z"
                else:
                    board += " "
            board += "|\n"
        board += "+--+--+--+--+--+"
        return board
    
    def update_board(self):
        self._board = self._draw()
    
    def _valid_move_or_build(self, new_position, current_position, direction, move=True):
        """Takes in the proposed action p"sition, the worker's current position,
           and the direction they're attempting to make an action in. Returns
           True if the proposed position can be moved to or built on, and false
           if it cannot be."""
        # can't move or build west if we're on the left edge of the board.
        if current_position % 5 == 0 and direction in Board.west_directions:
            return False
        # can't move or build east if we're on the right edge of the board
        elif current_position % 5 == 4 and direction in Board.east_directions:
            return False
        # can't move to/build out of bounds
        elif new_position < 0 or new_position > 24:
            return False
        # can't make a move to/build on a position with a height more than 1 greater than the worker's current height
        elif move and self._levels[new_position] > self._levels[current_position] + 1:
            return False
        # can't move to/build on a space with another worker on it
        elif new_position in self._workers.values():
            return False
        # can't move/build to a space with height of 4 (a dome)
        elif self._levels[new_position] == 4:
            return False
        else:
            return True
    
    def check_move(self, worker: str, direction: str, update: bool=True):
        """ Check validity of a proposed move direction 
            and execute it if valid. Returns true on
            success and updates the board, returns false
            on failure and doesn't update the board."""
        #  Translate 2-d address into 1-d
        offset = Board.address_translations[direction]

        # Translate worker to current location
        current_position = self._workers[worker]
        new_position = offset + current_position

        
        if self._valid_move_or_build(new_position, current_position, direction):
            # Conditionally update position of worker
            if update:
                self._workers[worker] = new_position
                self._board = self._draw()
            return True
        else:
            return False
        
    def check_build(self, worker: str, direction: str, update: bool=True):
        #  Translate 2-d address into 1-d
        offset = Board.address_translations[direction]

        # Translate worker to current location
        current_position = self._workers[worker]
        build_position = offset + current_position
        # Check validity of move direction
        if (self._valid_move_or_build(build_position, current_position, direction, False)):
            # Conditionally update build_position level
            if update:
                self._levels[build_position] += 1
                self._board = self._draw()
            return True
        else:
            return False
        
    def check_winner(self):
        """ Check there's a winner after a turn
        i.e. worker is on level 3 """
        worker_positions = self._workers.values()
        for position in worker_positions:
            if self._levels[position] == 3:
                return True
        return False