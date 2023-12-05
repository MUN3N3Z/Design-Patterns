from sys import argv, exit
from manager import Manager

class GameCLI:
    # class variables for valid inputs    
    def __init__(self, white_player, blue_player, enable_redo_undo, enable_score) -> None:
        self._manager = Manager(white_player, blue_player, enable_redo_undo, enable_score)
        
    def run(self):
        while True:
            # auto-win functionality
            # yesno = input("autowin?")
            # if yesno == "yes":
            #     self._manager.game_over = yesno

            self._manager.check_if_game_over()

            self._manager.print_board()

            self._manager.prompt_player()
                
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