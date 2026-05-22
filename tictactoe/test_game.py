"""
Script di test per verificare il corretto funzionamento del gioco e dell'AI
"""

from game import TicTacToe
from player import Player


def test_game_creation():
    """Test: Creazione del gioco"""
    game = TicTacToe()
    assert len(game.board) == 9
    assert game.current_player == 'X'
    print("✅ Test creazione gioco: PASSATO")


def test_make_move():
    """Test: Effettuare una mossa"""
    game = TicTacToe()
    result = game.make_move(0)
    assert result == True
    assert game.board[0] == 'X'
    assert game.current_player == 'O'
    print("✅ Test mossa: PASSATO")


def test_invalid_move():
    """Test: Mossa non valida"""
    game = TicTacToe()
    game.make_move(0)
    result = game.make_move(0)  # Prova a occupare la stessa posizione
    assert result == False
    print("✅ Test mossa non valida: PASSATO")


def test_winner_detection():
    """Test: Rilevamento del vincitore"""
    game = TicTacToe()
    # Simula una vittoria di X in diagonale
    game.make_move(0)  # X
    game.make_move(1)  # O
    game.make_move(4)  # X
    game.make_move(2)  # O
    game.make_move(8)  # X
    
    winner = game.check_winner()
    assert winner == 'X'
    print("✅ Test rilevamento vincitore: PASSATO")


def test_draw_detection():
    """Test: Rilevamento del pareggio"""
    game = TicTacToe()
    # Posizioni per un pareggio: X O X / O X X / O X O
    moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
    for move in moves:
        game.make_move(move)
    
    assert game.check_winner() is None
    assert game.is_board_full()
    print("✅ Test rilevamento pareggio: PASSATO")


def test_available_moves():
    """Test: Lista delle mosse disponibili"""
    game = TicTacToe()
    game.make_move(0)
    game.make_move(4)
    
    available = game.get_available_moves()
    assert 0 not in available
    assert 4 not in available
    assert len(available) == 7
    print("✅ Test mosse disponibili: PASSATO")


def test_ai_makes_move():
    """Test: L'AI effettua una mossa"""
    game = TicTacToe()
    game.make_move(0)  # Mossa umana
    
    ai = Player()
    best_move = ai.get_best_move(game)
    
    assert best_move is not None
    assert best_move in game.get_available_moves()
    print("✅ Test AI mossa: PASSATO")


def test_minimax_prevents_loss():
    """Test: Minimax previene la sconfitta"""
    game = TicTacToe()
    
    # Setup: Umano sta per vincere con X in posizione 2
    game.make_move(0)  # X in 0
    game.make_move(3)  # O in 3
    game.make_move(1)  # X in 1
    game.make_move(5)  # O in 5
    
    ai = Player(ai_symbol='O', human_symbol='X')
    best_move = ai.get_best_move(game)
    
    # Verifica che la mossa sia valida e impedisca la vittoria dell'umano
    assert best_move in game.get_available_moves()
    game.make_move(best_move)
    # Dopo la mossa dell'AI, l'umano non dovrebbe poter vincere subito
    game.make_move(2)  # Umano prova a vincere
    assert game.check_winner() != 'X'
    print("✅ Test Minimax blocca vittoria: PASSATO")


def test_undo_move():
    """Test: Annullamento di una mossa"""
    game = TicTacToe()
    game.make_move(0)
    assert game.board[0] == 'X'
    
    game.undo_move(0)
    assert game.board[0] == ' '
    assert game.current_player == 'X'
    print("✅ Test annullamento mossa: PASSATO")


def test_ai_vs_ai_game():
    """Test: AI vs AI completa una partita"""
    game = TicTacToe()
    ai_x = Player(ai_symbol='X', human_symbol='O')
    ai_o = Player(ai_symbol='O', human_symbol='X')
    
    # Simula una partita AI vs AI
    while not game.is_game_over():
        if game.current_player == 'X':
            move = ai_x.get_best_move(game)
        else:
            move = ai_o.get_best_move(game)
        
        game.make_move(move)
    
    # La partita dovrebbe terminare
    assert game.is_game_over()
    # Con due AI Minimax perfette, il risultato è sempre pareggio
    assert game.check_winner() is None
    print("✅ Test AI vs AI: PASSATO")


def test_moves_history():
    """Test: Cronologia delle mosse"""
    game = TicTacToe()
    
    game.make_move(0)  # X in 0
    game.make_move(4)  # O in 4
    game.make_move(2)  # X in 2
    
    assert len(game.moves_history) == 3
    assert game.moves_history[0] == (1, 0, 'X')
    assert game.moves_history[1] == (2, 4, 'O')
    assert game.moves_history[2] == (3, 2, 'X')
    print("✅ Test cronologia mosse: PASSATO")


if __name__ == "__main__":
    print("=" * 50)
    print("ESECUZIONE TEST DEL TIC TAC TOE")
    print("=" * 50)
    print()
    
    test_game_creation()
    test_make_move()
    test_invalid_move()
    test_winner_detection()
    test_draw_detection()
    test_available_moves()
    test_ai_makes_move()
    test_minimax_prevents_loss()
    test_undo_move()
    test_ai_vs_ai_game()
    test_moves_history()
    
    print()
    print("=" * 50)
    print("✅ TUTTI I TEST PASSATI!")
    print("=" * 50)
