from domain import Player, Fleet

class Game:
    def __init__(self, friendly_symbol: str, enemy_symbol: str, board_size: int = 10):
        self.__is_running = False
        self.__first_player_turn = True
        self.__setup(friendly_symbol, enemy_symbol, board_size)
    
    def __setup(self, friendly_symbol: str, enemy_symbol: str, board_size: int):
        self.__player1 = Player(Fleet(), friendly_symbol, enemy_symbol, board_size)
        self.__player2 = Player(Fleet(), friendly_symbol, enemy_symbol, board_size)

    def place_ships(self):
        self.__player1.place_ships()
        self.__player2.place_ships()

    def try_hit(self, x: int, y: int) -> str:
        """Apply a hit from the current player to the opponent and return
        the result ('miss','hit','sunk','win')."""
        if self.__first_player_turn:
            result = self.__player2.receive_fire(x, y)
            self.__player1.mark_opponent_board(x, y, result)
            self.__first_player_turn = False
            return result
        else: # player2's turn
            result = self.__player1.receive_fire(x, y)
            self.__player2.mark_opponent_board(x, y, result)
            self.__first_player_turn = True
            return result

    def game_over(self):
        if not self.__player1.has_remaining_ships() or not self.__player2.has_remaining_ships():
            return True
        return False

    def get_player1_boards(self) -> tuple[str,str]:
        """Return (player_board_printable, opponent_board_printable) for player1."""
        return (self.__player1.get_player_board_printable(), self.__player1.get_opponent_board_printable())

    def get_player2_boards(self) -> tuple[str,str]:
        """Return (player_board_printable, opponent_board_printable) for player2."""
        return (self.__player2.get_player_board_printable(), self.__player2.get_opponent_board_printable())

    def get_winner(self) -> int | None:
        """Return 1 if player1 won, 2 if player2 won, or None if no winner yet."""
        if not self.__player2.has_remaining_ships():
            return 1
        if not self.__player1.has_remaining_ships():
            return 2
        return None

    def __str__(self):
        return "The game " + ("is" if self.__is_running else "is not") + " running"
