from .fleet import Fleet
from .board import Board

class Player:
    def __init__(self, fleet: Fleet):
        self.__fleet = fleet

    def __place_ship(self, board: Board, x, y, direction) -> bool:
        # Places the ship on the board and returns True if the placement was successful, else returns False"""
       return board.place_ship(x, y, direction)

    def place_ships(self, board: Board):
        for ship in self.__fleet.get_ships():
            # TODO: get input
            # x, y = input()
            x = 0
            y = 2
            direction = "r" # or "l" or "up" or "dn"
            while not self.__place_ship(board, x, y, direction):
                print("Can't place ship on given location")

    def try_hit(self, board: Board, x, y) -> bool:
        # Tryies to hit the given location and returns True if it was a hit, False otherwise
        return board.try_hit(x, y)

    def has_remaining_ships(self) -> bool:
        return self.__fleet.empty()