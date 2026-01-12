from .fleet import Fleet
from .board import Board
from .ship import Ship

class Player:
    def __init__(self, fleet: Fleet, friedly_ship_symbol: str, enemy_ship_symbol: str, board_size: int):
        self.__fleet = fleet
        self.__player_board = Board(friedly_ship_symbol, board_size)
        self.__opponent_board = Board(enemy_ship_symbol, board_size)
        # map coordinates (x,y) -> Ship (for hits)
        self.__ship_positions: dict[tuple[int,int], Ship] = {}

        #  0 1
        # -----
        # |x|x| 0
        # | | | 1 
        # -----
        # 
        # ship_postions = {(0, 0) = ShipX}
        # ship_postions = {(0, 1) = ShipX}
        # ship_positons[(0, 1)] = ship_positions.get((0, 1)) = ShipX
        #


    #TODO: change direction to an enum (in class)
    def __place_ship(self, x: int, y: int, direction: str, ship_size: int) -> bool:
        """
        Calls the board's method for placing a ship and registers the ship's
        occupied positions in the `__ship_positions` mapping.
        """
        ok = self.__player_board.place_ship(x, y, direction, ship_size)
        if not ok:
            return False

        # register ship positions so we can map hits to ship instances
        ship = None
        for s in self.__fleet.get_ships():
            if s.get_size() == ship_size and not s.is_destroyed():
                # Heuristic: pick the first ship with the same size that isn't destroyed
                ship = s
                break
        if ship is None:
            # Fallback: create a Ship to represent positions (shouldn't happen)
            ship = Ship(ship_size)

        # depending on direction record the positions
        self.__ship_positions[(x, y)] = ship
        if direction == "l":
            for i in range(1, ship_size):
                self.__ship_positions[(x, y - i)] = ship
        elif direction == "r":
            for i in range(1, ship_size):
                self.__ship_positions[(x, y + i)] = ship
        elif direction == "up":
            for i in range(1, ship_size):
                self.__ship_positions[(x - i, y)] = ship
        elif direction == "dn":
            for i in range(1, ship_size):
                self.__ship_positions[(x + i, y)] = ship

        return True

    def place_ships(self):
        """Gets the input from the user and places the ships"""
        for ship in self.__fleet.get_ships():
            while True:
                print(self.__player_board.get_printable())
                x = int(input("Give x of head: "))
                y = int(input("Give y of head: "))
                direction = input("Give direction(l, r, up, dn)")
                # TODO: check input validity (in class)
                ok = self.__place_ship(x, y, direction, ship.get_size())
                if ok:
                    break
                print("Can't place ship on the given location")

    def try_hit(self, x, y) -> str:
        """Attempt to mark a hit on our internal opponent board (used for local mode).
        Returns 'miss' or 'hit' or 'already'."""
        return self.__opponent_board.try_hit(x, y)

    def has_remaining_ships(self) -> bool:
        return not self.__fleet.destroyed()

    # Network / game integration helpers
    def receive_fire(self, x: int, y: int) -> str:
        """Process an incoming fire at (x,y) on this player's board and return
        one of: 'miss', 'hit', 'sunk', 'win', 'already'"""
        result = self.__player_board.try_hit(x, y)
        if result == 'miss':
            return 'miss'
        if result == 'already':
            return 'already'
        if result == 'hit':
            # find ship object for this coordinate (if any)
            ship: Ship | None = self.__ship_positions.get((x, y), None)
            if ship is not None: # TODO: convert to error
                ship.hit()
                if ship.is_destroyed():
                    if self.__fleet.destroyed():
                        return 'win'
                    return 'sunk'
                return 'hit'
            # if no ship object mapping found, just return 'hit'
            return 'hit'

        # default
        return 'miss'

    def mark_opponent_board(self, x: int, y: int, result: str):
        """Update the local view of the opponent board based on a result."""
        if result in ['miss']:
            self.__opponent_board.set_symbol(x, y, '.')
        elif result in ['hit', 'sunk', 'win']:
            self.__opponent_board.set_symbol(x, y, 'X')
        # ignore unknown results

    def get_player_board_printable(self) -> str:
        return self.__player_board.get_printable()

    def get_opponent_board_printable(self) -> str:
        return self.__opponent_board.get_printable()