from sys import argv, exit
from manager import Manager

class GameCLI:
    # class variables for valid inputs    
    def __init__(self, player1: str, player2: str, enable_redo_undo: bool=False, enable_score: bool=False) -> None:
        self._manager = Manager(player1, player2, enable_redo_undo, enable_score)
        
    def run(self):
        while True:
            self._manager.check_if_game_over()

            self._manager.print_board()

            self._manager.prompt_player()
                
            self._manager.update_turn()

def check_arg(argument, ok_args):
    if argument > len(argv) - 1:
        arg = ok_args[0]
    elif argv[argument] in ok_args:
        arg = argv[argument]
    else:
        print("Invalid argument.")
        exit(0)
    return arg

if __name__ == "__main__":
    ok_args12 = ["human", "heuristic", "random"]
    ok_args34 = ["off", "on"]
    arg1 = check_arg(1, ok_args12)
    arg2 = check_arg(2, ok_args12)
    arg3 = check_arg(3, ok_args34)
    arg4 = check_arg(4, ok_args34)

    arg3 = True if arg3 == "on" else False
    arg4 = True if arg4 == "on" else False
    
    GameCLI(arg1, arg2, arg3, arg4).run()