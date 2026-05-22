# 🎮 Modalità di Gioco - Documentazione Dettagliata

## Panoramica delle Modalità

Il gioco del Tic Tac Toe supporta **3 modalità di gioco** selezionabili all'avvio:

```
0 - Umano vs Umano
1 - Umano vs AI (Minimax)
2 - AI vs AI (Minimax)
```

---

## 📋 Modalità 0: Umano vs Umano

### Descrizione
Due giocatori umani giocano l'uno contro l'altro sullo stesso computer.

### Come Funziona
```
Giocatore 1 → Usa il simbolo 'X' → Gioca per primo
Giocatore 2 → Usa il simbolo 'O' → Gioca per secondo
```

### Flusso
1. Giocatore 1 (X) inserisce una posizione (0-8)
2. Viene mostrata la griglia aggiornata
3. Giocatore 2 (O) inserisce una posizione (0-8)
4. Viene mostrata la griglia aggiornata
5. Ripete fino a vittoria o pareggio

### Risultati Possibili
- ✅ Giocatore X vince
- ✅ Giocatore O vince
- ⚖️ Pareggio

### Esempio di Schermata
```
>>> Turno del Giocatore X!
Giocatore X, la tua mossa (0-8): 4

 X |   |  
---+---+---
   | X |  
---+---+---
   |   |  

>>> Turno del Giocatore O!
Giocatore O, la tua mossa (0-8): 0

 O | X |  
---+---+---
   | X |  
---+---+---
   |   |  
```

### Use Case
- 👥 Giocare in coppia sullo stesso PC
- 🧠 Imparare il gioco
- 🎓 Capire la strategia del Tic Tac Toe

---

## 🤖 Modalità 1: Umano vs AI

### Descrizione
Un giocatore umano sfida un'AI intelligente basata su Minimax. L'AI è **imbattibile** in condizioni ideali.

### Come Funziona
```
Tu (Umano) → Simbolo 'X' → Giochi per primo
AI (Minimax) → Simbolo 'O' → Gioca per secondo
```

### Flusso
1. Viene mostrata la griglia vuota
2. Tu inserisci una posizione (0-8)
3. Viene mostrata la griglia aggiornata
4. L'AI calcola la migliore risposta con Minimax
5. L'AI effettua la mossa
6. Viene mostrata la griglia aggiornata
7. Ripete fino a vittoria dell'AI o pareggio

### Risultati Possibili
- ❌ L'AI vince (più probabile!)
- ✅ Tu vinci (quasi impossibile!)
- ⚖️ Pareggio (il miglior risultato possibile)

### Esempio di Schermata
```
>>> Il tuo turno!
Giocatore X, la tua mossa (0-8): 4

   |   |  
---+---+---
   | X |  
---+---+---
   |   |  

>>> L'AI giocatore O sta pensando...
L'AI ha giocato alla posizione 1

   | O |  
---+---+---
   | X |  
---+---+---
   |   |  
```

### Caratteristiche dell'AI
- 🧠 **Intelligenza**: L'AI analizzerà ogni possibile mossa futura
- 🛡️ **Difesa**: Blocca i tuoi tentativi di vittoria
- ⚡ **Velocità**: Risponde istantaneamente
- 🎯 **Precisione**: Prende sempre la mossa ottimale

### Use Case
- 🏆 Testare le tue abilità di gioco
- 📚 Imparare strategie di gioco ottimali
- 🧠 Comprendere come funziona Minimax
- 🎓 Esercizio educativo

---

## 🤖🤖 Modalità 2: AI vs AI

### Descrizione
Due AI Minimax giocano l'una contro l'altra. Interessante per osservare il gioco "perfetto".

### Come Funziona
```
AI 1 → Simbolo 'X' → Gioca per primo
AI 2 → Simbolo 'O' → Gioca per secondo
```

### Flusso
1. Premi Invio per iniziare
2. AI 1 calcola la migliore mossa
3. AI 1 effettua la mossa
4. AI 2 calcola la migliore mossa
5. AI 2 effettua la mossa
6. Ripete fino a conclusione

### Risultati Possibili
- ⚖️ **Sempre pareggio!** (entrambi gli AI giocano perfettamente)

### Esempio di Schermata
```
==================================================
MODALITÀ: AI VS AI
==================================================
AI 1 gioca con 'X'
AI 2 gioca con 'O'
Premi Invio per continuare...

>>> L'AI giocatore X sta pensando...
L'AI ha giocato alla posizione 4

   |   |  
---+---+---
   | X |  
---+---+---
   |   |  

>>> L'AI giocatore O sta pensando...
L'AI ha giocato alla posizione 1

   | O |  
---+---+---
   | X |  
---+---+---
   |   |  
```

### Caratteristiche
- 🧠 Entrambi gli AI usano Minimax
- ⚡ Calcoli ottimali per ogni turno
- ⏸️ Pause tra le mosse per leggibilità
- 📊 Osservazione del gioco perfetto

### Use Case
- 🔬 Ricerca e analisi del gioco
- 📚 Imparare il gioco ottimale
- 🧪 Test dell'algoritmo Minimax
- 🎓 Verificare che due AI perfette raggiungono il pareggio

---

## 🎮 Confronto delle Modalità

| Aspetto | Umano vs Umano | Umano vs AI | AI vs AI |
|---------|----------------|------------|----------|
| **Numero di AI** | 0 | 1 | 2 |
| **Difficoltà** | Dipende dai giocatori | Molto difficile | N/A |
| **Tempo di gioco** | Veloce/Media | Veloce | Veloce |
| **Risultato più probabile** | Varia | Vittoria AI | Pareggio |
| **Educativo** | Buono | Eccellente | Eccellente |
| **Divertimento** | Alto | Alto | Medio |

---

## 🔄 Passaggio tra Modalità

Dopo ogni partita, il programma chiede:
```
Vuoi giocare ancora? (s/n):
```

Se rispondi **'s'** (sì), puoi giocare di nuovo **nella stessa modalità**.

Se rispondi **'n'** (no), il programma termina.

Per cambiare modalità, devi riavviare il programma:
```bash
python main.py
```

---

## 💡 Suggerimenti per Ogni Modalità

### Per Umano vs Umano
- 🎯 Prova a controllare il centro della griglia
- 🛡️ Difenditi dagli attacchi dell'avversario
- 🧠 Pianifica strategie multi-turno

### Per Umano vs AI
- ⚖️ Il miglior risultato è il pareggio
- 🛡️ Sempre bloccare i tentativi di vittoria dell'AI
- 🧠 Osserva come l'AI respinge i tuoi attacchi
- 📚 Impara le strategie ottimali

### Per AI vs AI
- 🔍 Osserva attentamente i movimenti di entrambi gli AI
- 📊 Nota come entrambi gli AI seguono strategie complementari
- 🧠 Comprendi perché il risultato è sempre pareggio
- 📝 Prendi appunti sugli schemi di gioco

---

## 🚀 Avvio Rapido

```bash
# Avvia il gioco
python main.py

# Scegli la modalità:
# 0 - Umano vs Umano
# 1 - Umano vs AI
# 2 - AI vs AI

# Inizia a giocare!
```

**Divertiti! 🎮**
