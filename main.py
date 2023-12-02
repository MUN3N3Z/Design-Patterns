from board import Board
from sys import argv, exit
from manager import Manager

class GameCLI:
    # class variables for valid inputs
    valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
    
    def __init__(self, white_player, blue_player, enable_redo_undo, enable_score) -> None:
        self._board = Board()
        self._manager = Manager(enable_redo_undo, enable_score, white_player)
        self._valid_workers = self._manager.white_player + self._manager.blue_player
        
    def run(self):
        while True:
            print(self._board)
            turn = self._manager.get_turn_number()
            player = "white" if turn % 2 != 0 else "blue"
            workers = "AB" if turn % 2 != 0 else "YZ"
            print(f"Turn: {turn}, {player} ({workers})")
            # Request desired piece from human player
            while True:
                piece = input("Select a worker to move\n")
                if piece not in self._valid_workers:
                    print("Not a valid worker")
                elif piece not in self._manager.get_current_player():
                    print("That is not your worker")
                else:
                    break
            
            # Request move direction from human player
            while True:
                move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                if move not in GameCLI.valid_directions:
                    print("Not a valid direction")
                # check if can move in direction
                else:
                    break
            
            # Request a build direction from human player
            while True:
                build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                if build not in GameCLI.valid_directions:
                    print("Not a valid direction")
                # check if can build in direction
                else:
                    break
                
            print(piece + "," + move + "," + build)
            self._manager.update_turn()

def check_arg(argument, ok_args):
    if argument > len(argv) - 1:
        arg = ok_args[0]
    elif argv[argument] in ok_args:
        arg = argument
    else:
        print("Invalid argument.")
        exit()
    return arg

if __name__ == "__main__":
    ok_args12 = ["human", "heuristic", "random"]
    ok_args34 = ["off", "on"]
    arg1 = check_arg(1, ok_args12)
    arg2 = check_arg(2, ok_args12)
    arg3 = check_arg(3, ok_args34)
    arg4 = check_arg(4, ok_args34)
    
    GameCLI(arg1, arg2, arg3, arg4).run()