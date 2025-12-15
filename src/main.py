from domain.game import Game

#TODO: make a settings class

def main():
    player1_color = '🟦'
    player2_color = '🟥'
    board_size = 10
    game = Game(player1_color, player2_color, board_size)
    game.start_game_loop()

if __name__ == "__main__":
    main()
