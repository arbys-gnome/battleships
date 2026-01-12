from game import Game
# from net.session import NetworkSession

class TerminalUI:
    def __init__(self, game: Game):
        self.game = game

    def start(self):
        self.__start_menu()

    def __start_menu(self):
        print("Battleships")
        print("1) Local 1v1")
        # print("2) Host network game")
        # print("3) Join network game")
        choice = input("Choose mode: ")
        if choice == '1':
            self.__game_loop()
        elif choice == '2':
            port = int(input("Port to listen on (e.g. 65432): "))
            # NetworkSession.host(port, '🟦', '🟥')
        elif choice == '3':
            host = input("Host IP: ")
            port = int(input("Port: "))
            # NetworkSession.join(host, port, '🟦', '🟥')
        else:
            print("Unknown choice")

    def __game_loop(self):
        # first phase (place ships)
        print("Player 1, place your ships")
        # for local mode we place ships for both players
        self.game.place_ships()

        # second phase (fight)
        game_over = False
        while not game_over:
            raw = input("Give x and y (separated by space): ")
            parts = raw.strip().split()
            if len(parts) != 2:
                print("Invalid input")
                continue
            x = int(parts[0])
            y = int(parts[1])
            result = self.game.try_hit(x, y)
            print("Result:", result)

            # print boards for both players (for debug / local play)
            p1_board, p1_opp = self.game.get_player1_boards()
            p2_board, p2_opp = self.game.get_player2_boards()
            print("--- Player 1 board ---")
            print(p1_board)
            print("--- Player 1 view of opponent ---")
            print(p1_opp)
            print("--- Player 2 board ---")
            print(p2_board)
            print("--- Player 2 view of opponent ---")
            print(p2_opp)

            game_over = self.game.game_over()

        self.__display_winner()

    def __display_winner(self):
        winner = self.game.get_winner()
        if winner is None:
            print("It's a draw (unexpected)")
        else:
            print(f"Player {winner} won!")