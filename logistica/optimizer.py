"""
Ottimizzazione ordine consegne (TSP semplificato) su una lista di colli.
"""

from __future__ import annotations

from math import sqrt
from random import Random
from time import perf_counter
from typing import List, Sequence, Tuple
from colli import Collo4d

class Optimizer:
    def __init__(self, origine: Tuple[float, float] = (0.0, 0.0), ritorno_origine: bool = True):
        self.origine = origine
        self.ritorno_origine = ritorno_origine

    def _coord_cliente(self, collo: Collo4d) -> Tuple[float, float]:
        cliente = collo.cliente
        if cliente is None:
            raise ValueError("Ogni collo deve avere un cliente associato")
        
        lat = cliente.lat
        lng = cliente.lng
        if lat is None or lng is None:
            raise ValueError("Il cliente associato al collo non ha coordinate valide")

        return float(lat), float(lng)

    def _dist(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def distanza_totale(self, route: Sequence) -> float:
        if not route:
            return 0.0

        totale = 0.0
        precedente = self.origine

        for collo in route:
            corrente = self._coord_cliente(collo)
            totale += self._dist(precedente, corrente)
            precedente = corrente

        if self.ritorno_origine:
            totale += self._dist(precedente, self.origine)

        return totale

    def brute(self, colli: Sequence, max_seconds: float | None = None) -> List:
        """
        Ricerca esaustiva ricorsiva (backtracking) del percorso minimo.
        Complessita: O(n!).
        """
        if not colli:
            return []

        start_time = perf_counter()
        migliore_percorso = []
        migliore_distanza = float("inf")

        def visita(parziale: List, rimanenti: List, distanza_parziale: float, ultimo_punto: Tuple[float, float]):
            nonlocal migliore_percorso, migliore_distanza

            if max_seconds is not None and perf_counter() - start_time >= max_seconds:
                raise TimeoutError(
                    f"Tempo massimo superato nel brute force ({max_seconds:.2f}s)"
                )

            if not rimanenti:
                distanza_finale = distanza_parziale
                if self.ritorno_origine:
                    distanza_finale += self._dist(ultimo_punto, self.origine)

                if distanza_finale < migliore_distanza:
                    migliore_distanza = distanza_finale
                    migliore_percorso = parziale.copy()
                return

            if distanza_parziale >= migliore_distanza:
                return

            for i, collo in enumerate(rimanenti):
                punto = self._coord_cliente(collo)
                incremento = self._dist(ultimo_punto, punto)
                parziale.append(collo)

                prossimi = rimanenti[:i] + rimanenti[i + 1 :]
                visita(parziale, prossimi, distanza_parziale + incremento, punto)

                parziale.pop()

        visita([], list(colli), 0.0, self.origine)
        return migliore_percorso

    def fuzzy(
        self,
        colli: Sequence,
        generazioni: int = 250,
        popolazione_size: int = 80,
        mutation_rate: float = 0.12,
        elite_size: int = 4,
        seed: int | None = None,
    ) -> List:

        colli = list(colli)
        n = len(colli)
        if n <= 1:
            return colli

        rng = Random(seed)
        popolazione_size = max(10, popolazione_size)
        elite_size = max(1, min(elite_size, popolazione_size // 2))

        popolazione = [rng.sample(colli, n) for _ in range(popolazione_size)]

        def fitness(individuo: List) -> float:
            return 1.0 / (self.distanza_totale(individuo) + 1e-9)

        def torneo(popolazione_locale: List[List], k: int = 4) -> List:
            candidati = rng.sample(popolazione_locale, k=min(k, len(popolazione_locale)))
            return max(candidati, key=fitness)

        def crossover_ox(p1: List, p2: List) -> List:
            a, b = sorted(rng.sample(range(n), 2))
            figlio = [None] * n
            figlio[a : b + 1] = p1[a : b + 1]

            resto = [x for x in p2 if x not in figlio]
            idx_resto = 0
            for i in range(n):
                if figlio[i] is None:
                    figlio[i] = resto[idx_resto]
                    idx_resto += 1
            return figlio

        def mutazione_swap(individuo: List):
            if rng.random() < mutation_rate:
                i, j = rng.sample(range(n), 2)
                individuo[i], individuo[j] = individuo[j], individuo[i]

        for _ in range(generazioni):
            ordinata = sorted(popolazione, key=self.distanza_totale)
            nuova = [ind.copy() for ind in ordinata[:elite_size]]

            while len(nuova) < popolazione_size:
                p1 = torneo(ordinata)
                p2 = torneo(ordinata)
                figlio = crossover_ox(p1, p2)
                mutazione_swap(figlio)
                nuova.append(figlio)

            popolazione = nuova

        migliore = min(popolazione, key=self.distanza_totale)
        return migliore
