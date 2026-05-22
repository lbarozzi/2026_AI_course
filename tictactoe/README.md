# Tic Tac Toe - AI Player con Algoritmo Minimax

Un'implementazione completa del gioco del Tic Tac Toe in Python con un giocatore AI intelligente basato sull'algoritmo **Minimax**. Il progetto è strutturato in modo semplice e modulare, con un'interfaccia a carattere (terminale).

## 📋 Contenuti del Progetto

### File Principali

- **`main.py`** - Interfaccia a carattere per giocare (con supporto a 3 modalità)
- **`game.py`** - Classe `TicTacToe` che gestisce lo stato e la logica del gioco
- **`player.py`** - Classe `Player` che implementa l'algoritmo Minimax per l'AI
- **`test_game.py`** - Suite di test automatici
- **`README.md`** - Documentazione completa
- **`GAME_MODES.md`** - Descrizione dettagliata di tutte le modalità di gioco
- **`QUICKSTART.md`** - Guida rapida di avvio

## 🎮 Come Giocare

### Prerequisiti
- Python 3.6+
- Nessuna libreria esterna richiesta

### Esecuzione

```bash
python main.py
```

### Modalità di Gioco

All'avvio del programma, potrai scegliere tra tre modalità:

#### **Modalità 0: Umano vs Umano**
```
0 - Umano vs Umano
```
- Due giocatori umani giocano l'uno contro l'altro
- Giocatore 1 usa il simbolo 'X'
- Giocatore 2 usa il simbolo 'O'
- Perfetto per giocare in due!

#### **Modalità 1: Umano vs AI** (Default)
```
1 - Umano vs AI (Minimax)
```
- Tu giochi con il simbolo 'X'
- L'AI gioca con il simbolo 'O'
- L'AI è **imbattibile** - il meglio che puoi sperare è il pareggio!

#### **Modalità 2: AI vs AI**
```
2 - AI vs AI (Minimax)
```
- Due AI Minimax giocano l'una contro l'altra
- AI 1 gioca con il simbolo 'X'
- AI 2 gioca con il simbolo 'O'
- Con due AI Minimax perfette, il risultato è sempre **pareggio**
- Interessante per osservare il gioco ottimale!

### Regole del Gioco

1. La griglia è numerata da **0 a 8** per facilitare l'inserimento delle mosse
2. Vince chi allinea 3 simboli uguali in orizzontale, verticale o diagonale
3. Se la griglia si riempie senza vincitori, è un pareggio

### Layout della Griglia

```
 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8
```

### Esempio di Partita

Quando avvii `python main.py`, vedrai:

```
**************************************************
*                                                *
*   Benvenuto a TIC TAC TOE con AI Minimax!    *
*                                                *
**************************************************

==================================================
SCEGLI LA MODALITÀ DI GIOCO
==================================================
0 - Umano vs Umano
1 - Umano vs AI (Minimax)
2 - AI vs AI (Minimax)

Inserisci la tua scelta (0/1/2): 1

==================================================
MODALITÀ: UMANO VS AI
==================================================
Tu giochi con 'X'
L'AI gioca con 'O'

 X |   |  
---+---+---
   | O |  
---+---+---
   |   |  

Posizioni:
 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8

>>> Turno del Giocatore X!
Giocatore X, la tua mossa (0-8): ...
```

## 🎯 Gestione delle Modalità di Gioco

Il programma principale (`main.py`) gestisce dinamicamente le tre modalità di gioco:

### Flusso del Programma

```
1. Mostra il menu di benvenuto
   ↓
2. Chiedi quanti AI vuoi (0, 1, o 2)
   ↓
3. Inizializza i giocatori in base alla scelta
   ↓
4. Ciclo principale:
   - Mostra la griglia
   - Se è il turno di un umano → Leggi input
   - Se è il turno di un AI → Calcola mossa con Minimax
   - Continua finché il gioco non è finito
   ↓
5. Mostra il risultato
   ↓
6. Chiedi se giocare di nuovo
```

### Logica di Assegnazione Giocatori

| Modalità | Num AI | Giocatore X | Giocatore O |
|----------|--------|-------------|------------|
| Umano vs Umano | 0 | Umano 1 | Umano 2 |
| Umano vs AI | 1 | Umano | AI |
| AI vs AI | 2 | AI 1 | AI 2 |

## 🧠 Algoritmo Minimax

### Che cos'è il Minimax?

L'algoritmo **Minimax** è un algoritmo decisionale ricorsivo che trova la mossa ottimale in un gioco a due giocatori. 

### Come Funziona

1. **Fase di Massimizzazione**: L'AI cerca la mossa che massimizza il suo punteggio
2. **Fase di Minimizzazione**: L'avversario (umano) tenta di minimizzare il punteggio dell'AI
3. **Ricorsione**: L'algoritmo esplora ricorsivamente tutte le possibili mosse future

### Sistema di Punteggio

- **+10**: Vittoria dell'AI
- **-10**: Vittoria dell'umano
- **0**: Pareggio

La profondità della ricorsione viene considerata nel calcolo:
- **+10 - profondità**: Vittorie veloci sono premiate (l'AI preferisce vincere subito)
- **profondità - 10**: Sconfitte lente sono penalizzate (l'AI cerca di ritardare la sconfitta il più possibile)

### Pseudo-codice dell'Algoritmo

```
function minimax(game, depth, is_maximizing):
    if game is won by AI:
        return 10 - depth
    if game is won by human:
        return depth - 10
    if game is a draw:
        return 0
    
    if is_maximizing:
        best_score = -infinity
        for each possible move:
            make_move
            score = minimax(game, depth + 1, false)
            undo_move
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = +infinity
        for each possible move:
            make_move
            score = minimax(game, depth + 1, true)
            undo_move
            best_score = min(score, best_score)
        return best_score
```

## 📁 Struttura del Codice

### Classe `TicTacToe` (game.py)

Gestisce lo stato del gioco e la logica di base.

**Attributi:**
- `board`: Lista di 9 elementi rappresentante la griglia
- `human`: Simbolo del giocatore umano ('X')
- `ai`: Simbolo dell'AI ('O')
- `current_player`: Simbolo del giocatore corrente

**Metodi principali:**
- `make_move(position)`: Effettua una mossa sulla griglia
- `undo_move(position)`: Annulla una mossa (usato dall'algoritmo Minimax)
- `get_available_moves()`: Ritorna le posizioni libere
- `check_winner()`: Controlla se c'è un vincitore
- `is_game_over()`: Verifica se il gioco è finito
- `display()`: Mostra la griglia di gioco

### Classe `Player` (player.py)

Implementa l'intelligenza artificiale basata su Minimax.

**Metodi:**
- `get_best_move(game)`: Trova la mossa migliore
- `minimax(game, depth, is_maximizing)`: Algoritmo ricorsivo Minimax

### Funzioni Principali (main.py)

- `get_number_of_ai()`: Richiede all'utente il numero di AI (0, 1, o 2)
- `get_human_move(game, player_symbol)`: Legge l'input dell'utente
- `get_ai_move(game, ai_player)`: Ottiene la mossa dell'AI
- `play_game(num_ai)`: Gestisce il flusso principale del gioco in base alle modalità

## 💡 Strategie Chiave dell'AI

L'AI con Minimax è **imbattibile** in condizioni ideali. Alcune strategie che implementa automaticamente:

1. **Vittoria**: Se può vincere al turno successivo, lo fa
2. **Difesa**: Se l'avversario può vincere al turno successivo, blocca
3. **Controllo del Centro**: Preferisce il centro della griglia quando possibile
4. **Posizionamento Strategico**: Crea minacce multiple (forks) per forzare la sconfitta dell'avversario
5. **Minimizzazione delle Perdite**: Se non può vincere, cerca il pareggio

Queste strategie funzionano in **tutte le modalità di gioco**:
- In modalità **Umano vs AI**: L'AI protegge dai tuoi attacchi
- In modalità **Umano vs Umano**: Nessun AI, giocatori umani controllano tutto
- In modalità **AI vs AI**: Entrambi gli AI giocano in modo ottimale, risultato sempre pareggio

## 🔄 Flusso del Gioco

```
START
  ↓
Inizializza il gioco
  ↓
┌─────────────────────┐
│ Gioco in corso?     │
│ (Non finito)        │
└──────────┬──────────┘
          ↓
    Se turno umano:
         ↓
    Leggi input
         ↓
    Effettua mossa
    
    Se turno AI:
         ↓
    Calcola mossa con Minimax
         ↓
    Effettua mossa
         ↓
    Torna all'inizio del ciclo
         
         ↓
┌─────────────────────┐
│ Fine gioco          │
│ Mostra risultato    │
└──────────┬──────────┘
          ↓
Chiedi se giocare di nuovo
          ↓
         END
```

## 📊 Complessità Computazionale

### Tempo
- **Worst case**: O(9!) ≈ 362,880 stati da analizzare al primo turno
- **Pratico**: Molto più veloce grazie all'effetto del branching factor decrescente

### Spazio
- O(profondità massima) = O(9) per la ricorsione

## ✨ Punti di Forza del Codice

1. ✅ **Semplicità**: Codice leggibile e facile da mantenere
2. ✅ **Modularità**: Classe `TicTacToe` separata da `Player`
3. ✅ **Documentazione**: Docstring completi per ogni metodo
4. ✅ **Nessuna Dipendenza**: Solo librerie standard di Python
5. ✅ **Intuitivo**: Interfaccia a carattere chiara e user-friendly

## 🎯 Possibili Miglioramenti

- Aggiungere una modalità umano vs umano
- Implementare un'interfaccia grafica (tkinter o pygame)
- Aggiungere statistiche di gioco (vittorie, sconfitte, pareggi)
- Ottimizzare con Alpha-Beta pruning per velocizzare l'algoritmo
- Aggiungere livelli di difficoltà (random move, minimax limitato, ecc.)

## 📝 Licenza

Questo progetto è fornito come materiale educativo.

## 👨‍💻 Autore

Progetto creato per scopi didattici.

---

**Divertiti a giocare e impara come funziona uno dei più importanti algoritmi dell'IA! 🤖🎮**
