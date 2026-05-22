"""
Classe Player con algoritmo Minimax per il Tic Tac Toe
"""


class Player:
    """
    Player AI che utilizza l'algoritmo Minimax per trovare la mossa migliore.
    L'algoritmo Minimax è un algoritmo decisionale ricorsivo che:
    - Massimizza il punteggio per il giocatore AI
    - Minimizza il punteggio per l'avversario
    """

    def __init__(self, ai_symbol='O', human_symbol='X'):
        """
        Inizializza il player AI.
        
        Args:
            ai_symbol (str): Il simbolo utilizzato dall'AI ('O' di default)
            human_symbol (str): Il simbolo utilizzato dall'umano ('X' di default)
        """
        self.ai_symbol = ai_symbol
        self.human_symbol = human_symbol

    def get_best_move(self, game):
        """
        Trova la mossa migliore utilizzando l'algoritmo Minimax.
        
        Args:
            game (TicTacToe): L'oggetto del gioco
            
        Returns:
            int: La posizione migliore dove piazzare il simbolo
        """
        best_score = float('-inf')
        best_move = None

        # Prova tutte le mosse disponibili
        for move in game.get_available_moves():
            game.make_move(move)
            score = self.minimax(game, 0, False)
            game.undo_move(move)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game, depth, is_maximizing):
        """
        Algoritmo Minimax ricorsivo.
        Valuta tutte le possibili configurazioni di gioco per trovare la mossa ottimale.
        
        Args:
            game (TicTacToe): L'oggetto del gioco
            depth (int): La profondità della ricorsione (usata per il scoring)
            is_maximizing (bool): True se stiamo massimizzando (turno AI), 
                                 False se stiamo minimizzando (turno umano)
            
        Returns:
            int: Un punteggio che rappresenta la bontà della posizione
                10: Vittoria dell'AI
                -10: Vittoria dell'umano
                0: Pareggio
        """
        winner = game.check_winner()

        # Caso base: il gioco è finito
        if winner == self.ai_symbol:
            # AI ha vinto: ritorna punteggio positivo (ridotto per profondità)
            # Le vittorie più veloci hanno priorità
            return 10 - depth
        elif winner == self.human_symbol:
            # Umano ha vinto: ritorna punteggio negativo
            # Le sconfitte più lente hanno priorità (cercheremo di evitarle il più tardi possibile)
            return depth - 10
        elif game.is_board_full():
            # Pareggio
            return 0

        if is_maximizing:
            # Turno dell'AI: massimizza il punteggio
            max_score = float('-inf')
            for move in game.get_available_moves():
                game.make_move(move)
                score = self.minimax(game, depth + 1, False)
                game.undo_move(move)
                max_score = max(score, max_score)
            return max_score
        else:
            # Turno dell'umano: minimizza il punteggio
            min_score = float('inf')
            for move in game.get_available_moves():
                game.make_move(move)
                score = self.minimax(game, depth + 1, True)
                game.undo_move(move)
                min_score = min(score, min_score)
            return min_score
