import unicodedata

class Board:
    def __init__(self, ship_symbol: str, size: int = 10):
        if type(size) is not int:
            raise Exception("ERROR: size must be an integer")

        self.__ship_symbol_w = 0
        for ch in ship_symbol:
            ch_is_emoji: bool = unicodedata.east_asian_width(ch) == 'W'
            self.__ship_symbol_w += 2 if ch_is_emoji else 1

        self.__empty_symbol = ' ' * self.__ship_symbol_w
        self.__ship_symbol = ship_symbol
        self.__board = [[self.__empty_symbol for _ in range(size)] for _ in range(size)]

    def get_printable(self) -> str:
        return self.__str__()

    def place_ship(self, x: int, y: int, direction: str, ship_length: int) -> bool:
        """
        Places the ship in the board.
        
        :param self: class instance
        :param x: the x coordinate of the ship's head
        :param y: the y coordinate of the ship's head
        :param direction: direction of the ship's tail
        :return: True if the placement was successfull, False otherwise
        :rtype: bool
        """

        # check if the head can be placed
        if x < 0 or x >= len(self.__board) or \
           y < 0 or y >= len(self.__board[x]) or \
           self.__board[x][y] != " ":
            return False
        
        # check if the rest of the ship can be placed 
        if direction == "l":
            for i in range(1, ship_length):
                if y - i < 0 or self.__board[x][y - i] != " ":
                    return False
        elif direction == "r":
            for i in range(1, ship_length):
                if y + i >= len(self.__board[x]) or self.__board[x][y + i] != " ":
                    return False
        elif direction == "up":
            for i in range(1, ship_length):
                if x - i < 0 or self.__board[x - i][y] != " ":
                    return False
        elif direction == "dn":
            for i in range(1, ship_length):
                if y + i >= len(self.__board) or self.__board[x + i][y] != " ":
                    return False
        else:
            return False

        # mark the place were the ship is placed
        self.__board[x][y] = self.__ship_symbol
        if direction == "l":
            for i in range(1, ship_length):
                self.__board[x][y - i] = self.__ship_symbol
        elif direction == "r":
            for i in range(1, ship_length):
                self.__board[x][y + i] = self.__ship_symbol
        elif direction == "up":
            for i in range(1, ship_length):
                self.__board[x - i][y] = self.__ship_symbol
        elif direction == "dn":
            for i in range(1, ship_length):
                self.__board[x + i][y] = self.__ship_symbol

        return True # success

    def __has_ship(self, x, y) -> bool:
        return self.__board[x][y] != " "

    def try_hit(self, x, y) -> bool:
        # TODO: check if this was already hit
        if self.__has_ship(x, y):
            # TODO: mark the ship as hit
            return True
        return False

    def __str__(self) -> str:
        fmt_board = ''
        border = "-" * (len(self.__board[0]) * (3 + self.__ship_symbol_w) + 1)
        for row in self.__board:
            fmt_row = '|' + str(row)[1:-1].replace(', ', '|').replace("'", " ") + '|'
            fmt_board += f'{border}\n{fmt_row}\n'
        fmt_board += border + '\n'
        return fmt_board

