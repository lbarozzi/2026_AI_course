"""
Interfaccia principale per il gioco del Tic Tac Toe
Permette di giocare in tre modalità: Umano vs AI, Umano vs Umano, AI vs AI
"""

import time
from game import TicTacToe
from player import Player


def get_number_of_ai():
    """
    Chiede all'utente quanti giocatori AI vuole.
    
    Returns:
        int: 0 (Umano vs Umano), 1 (Umano vs AI), 2 (AI vs AI)
    """
    while True:
        print("\n" + "=" * 50)
        print("SCEGLI LA MODALITÀ DI GIOCO")
        print("=" * 50)
        print("0 - Umano vs Umano")
        print("1 - Umano vs AI (Minimax)")
        print("2 - AI vs AI (Minimax)")
        
        try:
            choice = int(input("\nInserisci la tua scelta (0/1/2): "))
            if choice in [0, 1, 2]:
                return choice
            else:
                print("Inserisci un numero tra 0 e 2!")
        except ValueError:
            print("Inserisci un numero valido!")


def get_human_move(game, player_symbol):
    """
    Chiede al giocatore umano di inserire una mossa valida.
    
    Args:
        game (TicTacToe): L'oggetto del gioco
        player_symbol (str): Il simbolo del giocatore ('X' o 'O')
        
    Returns:
        int: La posizione scelta dal giocatore
    """
    while True:
        try:
            position = int(input(f"Giocatore {player_symbol}, la tua mossa (0-8): "))
            if position < 0 or position > 8:
                print("Inserisci un numero tra 0 e 8!")
                continue
            if not game.make_move(position):
                print("Posizione già occupata! Scegli un'altra.")
                continue
            return position
        except ValueError:
            print("Inserisci un numero valido!")


def get_ai_move(game, ai_player):
    """
    Ottiene la mossa dell'AI.
    
    Args:
        game (TicTacToe): L'oggetto del gioco
        ai_player (Player): L'oggetto Player con l'AI
        
    Returns:
        int: La posizione scelta dall'AI
    """
    print(f">>> L'AI giocatore {game.current_player} sta pensando...")
    move = ai_player.get_best_move(game)
    game.make_move(move)
    print(f"L'AI ha giocato alla posizione {move}")
    time.sleep(1)  # Piccola pausa per leggibilità
    return move


def play_game(num_ai):
    """
    Gestisce il flusso principale del gioco.
    
    Args:
        num_ai (int): Numero di giocatori AI (0, 1, o 2)
    """
    game = TicTacToe()
    ai_x = Player(ai_symbol='X', human_symbol='O') if num_ai >= 1 else None
    ai_o = Player(ai_symbol='O', human_symbol='X') if num_ai >= 2 else None

    # Mostra la modalità di gioco
    if num_ai == 0:
        print("\n" + "=" * 50)
        print("MODALITÀ: UMANO VS UMANO")
        print("=" * 50)
        print("Giocatore 1: X")
        print("Giocatore 2: O")
    elif num_ai == 1:
        print("\n" + "=" * 50)
        print("MODALITÀ: UMANO VS AI")
        print("=" * 50)
        print("Tu giochi con 'X'")
        print("L'AI gioca con 'O'")
    else:  # num_ai == 2
        print("\n" + "=" * 50)
        print("MODALITÀ: AI VS AI")
        print("=" * 50)
        print("AI 1 gioca con 'X'")
        print("AI 2 gioca con 'O'")
        print("Premi Invio per continuare...")
        input()

    # Ciclo principale del gioco
    while not game.is_game_over():
        game.display()

        if game.current_player == 'X':
            if num_ai >= 1:  # X è controllato dall'AI
                get_ai_move(game, ai_x)
            else:  # X è controllato da umano
                print(">>> Turno del Giocatore X!")
                get_human_move(game, 'X')
        else:  # game.current_player == 'O'
            if num_ai == 2:  # O è controllato dall'AI
                get_ai_move(game, ai_o)
            elif num_ai == 1:  # O è controllato dall'AI
                get_ai_move(game, ai_x)  # Usa l'AI player
            else:  # O è controllato da umano
                print(">>> Turno del Giocatore O!")
                get_human_move(game, 'O')

    # Gioco finito
    game.display()
    winner = game.check_winner()

    if winner == 'X':
        if num_ai == 0:
            print("🎉 GIOCATORE X HA VINTO! 🎉")
        elif num_ai == 1:
            print("😔 L'AI ha vinto. Riprova! 😔")
        else:
            print("🤖 AI 1 (X) HA VINTO! 🤖")
    elif winner == 'O':
        if num_ai == 0:
            print("🎉 GIOCATORE O HA VINTO! 🎉")
        elif num_ai == 1:
            print("🎉 HAI VINTO! Complimenti! 🎉")
        else:
            print("🤖 AI 2 (O) HA VINTO! 🤖")
    else:
        print("⚖️  È un pareggio! ⚖️")

    # Chiedi se giocare di nuovo
    print("\n" + "=" * 50)
    while True:
        again = input("Vuoi giocare ancora? (s/n): ").lower()
        if again == 's':
            game.reset()
            play_game(num_ai)
            break
        elif again == 'n':
            print("Grazie per aver giocato! Arrivederci! 👋")
            break
        else:
            print("Inserisci 's' per sì o 'n' per no.")


if __name__ == "__main__":
    print("\n")
    print("*" * 50)
    print("*" + " " * 48 + "*")
    print("*" + "  Benvenuto a TIC TAC TOE con AI Minimax!".center(48) + "*")
    print("*" + " " * 48 + "*")
    print("*" * 50)
    
    num_ai = get_number_of_ai()
    play_game(num_ai)
