# 🚀 Guida Rapida di Avvio

## Esecuzione del Gioco

```bash
python main.py
```

### Scegli una Modalità

```
0 - Umano vs Umano     (Due giocatori umani)
1 - Umano vs AI        (Tu contro l'AI - la scelta più popolare!)
2 - AI vs AI           (Guarda due AI perfette giocare)
```

---

## 📖 Descrizione delle Modalità

| Modalità | Descrizione |
|----------|------------|
| **0** | Due giocatori umani sullo stesso PC |
| **1** | Tu (X) contro l'AI (O) - L'AI è imbattibile! |
| **2** | Due AI giocano l'una contro l'altra - Sempre pareggio |

Per una descrizione dettagliata di ogni modalità, leggi **[GAME_MODES.md](GAME_MODES.md)**

---

## Esecuzione dei Test

Per verificare che tutto funzioni correttamente:

```bash
python test_game.py
```

Questo esegue una suite di test che verifica:
- ✅ Creazione del gioco
- ✅ Effettuazione mosse
- ✅ Rilevamento vincitori
- ✅ Rilevamento pareggi
- ✅ Algoritmo Minimax
- ✅ AI vs AI

---

## Struttura dei File

```
tictactoe/
├── main.py           # Punto di ingresso - Esegui questo per giocare
├── game.py           # Logica del gioco (Classe TicTacToe)
├── player.py         # AI con algoritmo Minimax (Classe Player)
├── test_game.py      # Test automatici
├── README.md         # Documentazione completa
├── GAME_MODES.md     # Descrizione dettagliata delle modalità
└── QUICKSTART.md     # Questa guida
```

---

## Comandi Rapidi

| Comando | Descrizione |
|---------|-------------|
| `python main.py` | Avvia il gioco e scegli la modalità |
| `python test_game.py` | Esegui i test automatici |
| `python -m py_compile *.py` | Verifica sintassi di tutti i file |

---

## Requisiti

- **Python 3.6+**
- Nessuna libreria esterna richiesta!

---

Buon divertimento! 🎮
