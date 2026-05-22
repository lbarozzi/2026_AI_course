'''
Author: Lba
Date: 2026-05-22
Description: Main applicaition entry point for the project. This file initializes the application, sets up necessary configurations, and starts the main execution loop. It serves as the central hub for coordinating various components of the application and ensuring that they work together seamlessly.
'''

from gestore import Gestore
from optimizer import Optimizer
from pathlib import Path
from time import perf_counter


def _format_percorso(colli):
    nodi = []
    for c in colli:
        cliente = c.cliente
        nome = cliente.nome_completo if cliente is not None else "Cliente"
        cid = c.id
        nodi.append(f"{cid}:{nome}")
    return " -> ".join(nodi)


def main(tipo: str = "demo"):
    if tipo != "demo":
        raise ValueError("Tipo non supportato. Usa 'demo'.")

    n_test = 20

    gestore = Gestore.crea_gestore(
        numero_veicoli=8,
        numero_guidatori=20,
        colli_per_veicolo=10,
        numero_clienti=220,
        percentuale_rotti=0.15,
    )

    if len(gestore.colli) < n_test:
        pkl = Path("gestore.pkl")
        if pkl.exists():
            pkl.unlink()
        gestore = Gestore.crea_gestore(
            numero_veicoli=8,
            numero_guidatori=20,
            colli_per_veicolo=10,
            numero_clienti=220,
            percentuale_rotti=0.15,
        )

    colli = gestore.colli[:n_test]
    if len(colli) < 2:
        print("Non ci sono abbastanza colli per eseguire l'ottimizzazione.")
        return

    optimizer = Optimizer(origine=(0.0, 0.0), ritorno_origine=True)

    ordine_iniziale = colli
    distanza_iniziale = optimizer.distanza_totale(ordine_iniziale)

    tempo_fuzzy_start = perf_counter()
    ordine_fuzzy = optimizer.fuzzy(
        colli,
        generazioni=350,
        popolazione_size=180,
        mutation_rate=0.12,
        elite_size=8,
        seed=42,
    )
    tempo_fuzzy = perf_counter() - tempo_fuzzy_start
    distanza_fuzzy = optimizer.distanza_totale(ordine_fuzzy)

    brute_timeout_s = 20.0
    tempo_brute_start = perf_counter()
    brute_completato = True
    ordine_brute = []
    distanza_brute = None
    try:
        ordine_brute = optimizer.brute(colli, max_seconds=brute_timeout_s)
        distanza_brute = optimizer.distanza_totale(ordine_brute)
    except TimeoutError:
        brute_completato = False
    tempo_brute = perf_counter() - tempo_brute_start

    miglioramento_brute = (
        ((distanza_iniziale - distanza_brute) / distanza_iniziale) * 100
        if (distanza_iniziale and distanza_brute is not None)
        else None
    )
    miglioramento_fuzzy = (
        ((distanza_iniziale - distanza_fuzzy) / distanza_iniziale) * 100 if distanza_iniziale else 0.0
    )

    rapporto_tempi = (tempo_brute / tempo_fuzzy) if tempo_fuzzy else float("inf")

    print("=== Confronto Optimizer (TSP) ===")
    print(f"Colli considerati: {len(colli)}")
    print(f"Distanza iniziale: {distanza_iniziale:.3f}")
    print(f"Distanza fuzzy (genetico): {distanza_fuzzy:.3f}")
    print(f"Tempo fuzzy: {tempo_fuzzy:.4f} s")
    print(f"Miglioramento fuzzy su iniziale: {miglioramento_fuzzy:.2f}%")
    if brute_completato:
        print(f"Distanza brute (ricorsivo): {distanza_brute:.3f}")
        print(f"Tempo brute: {tempo_brute:.4f} s")
        print(f"Miglioramento brute: {miglioramento_brute:.2f}%")
        print(f"Rapporto tempi brute/fuzzy: {rapporto_tempi:.2f}x")
        print("\nPercorso brute:")
        print(_format_percorso(ordine_brute))
    else:
        print(
            f"Brute non completato entro {brute_timeout_s:.1f}s "
            f"(tempo misurato: {tempo_brute:.4f} s)"
        )
        print("Distanza brute: non disponibile (timeout)")
        print(f"Rapporto tempi brute/fuzzy: >= {rapporto_tempi:.2f}x (limite inferiore)")

    print("\nPercorso fuzzy:")
    print(_format_percorso(ordine_fuzzy))


if __name__ == "__main__":
    main()

