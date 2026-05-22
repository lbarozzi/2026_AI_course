"""
Classe per il gioco del Tic Tac Toe
"""


class TicTacToe:
    """
    Gestisce lo stato e la logica del gioco del Tic Tac Toe.
    La griglia è rappresentata come una lista di 9 elementi (indici 0-8).
    Mapping della griglia:
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
    """

    def __init__(self):
        """Inizializza una nuova partita."""
        self.board = [' '] * 9  # Griglia vuota
        self.human = 'X'
        self.ai = 'O'
        self.current_player = 'X'
        self.moves_history = []  # Cronologia delle mosse

    def make_move(self, position):
        """
        Effettua una mossa sulla griglia.
        
        Args:
            position (int): Posizione 0-8 dove piazzare il simbolo
            
        Returns:
            bool: True se la mossa è valida, False altrimenti
        """
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            # Registra la mossa nella cronologia
            self.moves_history.append((len(self.moves_history) + 1, position, self.current_player))
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def undo_move(self, position):
        """
        Annulla una mossa (usato dall'algoritmo minimax).
        
        Args:
            position (int): Posizione della mossa da annullare
        """
        self.board[position] = ' '
        # Rimuovi la mossa dalla cronologia se esiste
        if self.moves_history and self.moves_history[-1][1] == position:
            self.moves_history.pop()
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_available_moves(self):
        """
        Ritorna la lista delle posizioni libere sulla griglia.
        
        Returns:
            list: Lista di indici dove è possibile piazzare un simbolo
        """
        return [i for i in range(9) if self.board[i] == ' ']

    def check_winner(self):
        """
        Controlla se c'è un vincitore.
        
        Returns:
            str: 'X' se X ha vinto, 'O' se O ha vinto, None se non c'è vincitore
        """
        # Tutte le combinazioni vincenti possibili
        winning_combinations = [
            [0, 1, 2],  # Righe
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],  # Colonne
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],  # Diagonali
            [2, 4, 6],
        ]

        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                    and self.board[combo[0]] != ' '):
                return self.board[combo[0]]

        return None

    def is_board_full(self):
        """
        Controlla se la griglia è piena.
        
        Returns:
            bool: True se non ci sono mosse disponibili
        """
        return len(self.get_available_moves()) == 0

    def is_game_over(self):
        """
        Controlla se il gioco è finito.
        
        Returns:
            bool: True se c'è un vincitore o la griglia è piena
        """
        return self.check_winner() is not None or self.is_board_full()

    def reset(self):
        """Resetta il gioco a uno stato iniziale."""
        self.board = [' '] * 9
        self.current_player = 'X'
        self.moves_history = []

    def display(self):
        """Mostra la griglia di gioco con posizioni occupate e libere."""
        print("\n")
        # Funzione helper per ottenere il contenuto di una cella
        def get_cell(pos):
            if self.board[pos] != ' ':
                return self.board[pos]  # Mostra X o O se occupato
            else:
                return str(pos)  # Mostra il numero se libero
        
        # Mostra la griglia unificata
        print(f" {get_cell(0)} | {get_cell(1)} | {get_cell(2)}")
        print("---+---+---")
        print(f" {get_cell(3)} | {get_cell(4)} | {get_cell(5)}")
        print("---+---+---")
        print(f" {get_cell(6)} | {get_cell(7)} | {get_cell(8)}")
        print()

    def get_board_copy(self):
        """
        Ritorna una copia della griglia.
        
        Returns:
            list: Copia della griglia attuale
        """
        return self.board.copy()
