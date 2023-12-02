class Board:
    def __init__(self, p11=16, p12=8, p21=6, p22=18):
        self._levels = [0 for _ in range(0, 25)]
        self._p11 = p11
        self._p12 = p12
        self._p21 = p21
        self._p22 = p22
        self._board = self.draw(self._p11, self._p12, self._p21, self._p22, self._levels)

    def __repr__(self):
        return self._board

    """draw takes in four worker positions as ints
       as well as an array of all the spaces' levels
       and returns the drawn ASCII board"""
    def draw(self, p11, p12, p21, p22, levels):
        board = ""
        for i in range(0, 5):
            board += "+--+--+--+--+--+\n"
            for j in range(0, 5):
                index = 5 * i + j
                board += "|"
                board += str(levels[index])
                if index == p11:
                    board += "A"
                elif index == p12:
                    board += "B"
                elif index == p21:
                    board += "Y"
                elif index == p22:
                    board += "Z"
                else:
                    board += " "
            board += "|\n"
        board += "+--+--+--+--+--+\n"
        return board
    
    def update_board(self, p11, p12, p21, p22, levels):
        self._board = self.draw(p11, p12, p21, p22, levels)