'''
Author: Lba
Date: 2026-05-22
Description: Main applicaition entry point for the project. This file initializes the application, sets up necessary configurations, and starts the main execution loop. It serves as the central hub for coordinating various components of the application and ensuring that they work together seamlessly.
'''

from gestore import Gestore
from optimizer import Optimizer
from pathlib import Path
from time import perf_counter
from visualizer import RouteVisualizer


def _format_percorso(colli):
    nodi = []
    for c in colli:
        cliente = c.cliente
        nome = cliente.nome_completo if cliente is not None else "Cliente"
        cid = c.id
        nodi.append(f"{cid}:{nome}")
    return " -> ".join(nodi)


def _distribuisci_colli_per_mezzo(colli, numero_mezzi: int):
    percorsi = [[] for _ in range(numero_mezzi)]
    for idx, collo in enumerate(colli):
        percorsi[idx % numero_mezzi].append(collo)
    return percorsi


def main(tipo: str = "demo"):
    if tipo != "demo":
        raise ValueError("Tipo non supportato. Usa 'demo'.")

    numero_mezzi_target = 40
    timeout_percorso_s = 8.0

    gestore = Gestore.crea_gestore(
        numero_veicoli=10,
        numero_guidatori=20,
        colli_per_veicolo=10,
        numero_clienti=220,
        percentuale_rotti=0.15,
    )

    if len(gestore.mezzi) < numero_mezzi_target or len(gestore.colli) < numero_mezzi_target:
        pkl = Path("gestore.pkl")
        if pkl.exists():
            pkl.unlink()
        gestore = Gestore.crea_gestore(
            numero_veicoli=10,
            numero_guidatori=20,
            colli_per_veicolo=10,
            numero_clienti=220,
            percentuale_rotti=0.15,
        )

    mezzi = gestore.mezzi[:numero_mezzi_target]
    colli = gestore.colli
    if not colli or not mezzi:
        print("Non ci sono abbastanza dati per eseguire l'ottimizzazione per mezzo.")
        return

    optimizer = Optimizer(origine=(0.0, 0.0), ritorno_origine=True)
    visualizer = RouteVisualizer(origine=(0.0, 0.0))

    percorsi_originali = _distribuisci_colli_per_mezzo(colli, len(mezzi))
    output_dir = Path("percorsi_mezzi_algoritmi")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== Ottimizzazione per mezzo ===")
    print(f"Mezzi considerati: {len(mezzi)}")
    print(f"Colli totali: {len(colli)}")
    print(f"Output immagini: {output_dir}")
    print()

    immagini_salvate = 0
    for idx, (mezzo, percorso_originale) in enumerate(zip(mezzi, percorsi_originali), start=1):
        nome_mezzo = type(mezzo).__name__
        distanza_orig = optimizer.distanza_totale(percorso_originale)

        algoritmi = [
            ("Forza bruta", lambda: optimizer.brute(percorso_originale, max_seconds=timeout_percorso_s), "tab:blue"),
            ("Held-Karp", lambda: optimizer.held_karp(percorso_originale, max_seconds=timeout_percorso_s), "tab:purple"),
            ("Nearest Neighbor", lambda: optimizer.nearest_neighbor(percorso_originale), "tab:orange"),
            ("2-Opt", lambda: optimizer.two_opt(percorso_originale, max_seconds=timeout_percorso_s), "tab:brown"),
            ("NN + 2-Opt", lambda: optimizer.nn_two_opt(percorso_originale, max_seconds=timeout_percorso_s), "tab:green"),
            (
                "Fuzzy",
                lambda: optimizer.fuzzy(
                    percorso_originale,
                    generazioni=120,
                    popolazione_size=50,
                    mutation_rate=0.12,
                    elite_size=4,
                    seed=42,
                ),
                "tab:red",
            ),
        ]

        risultati = []
        for nome, funzione, colore in algoritmi:
            start = perf_counter()
            try:
                percorso = funzione()
                elapsed = perf_counter() - start
                distanza = optimizer.distanza_totale(percorso)
                miglioramento = ((distanza_orig - distanza) / distanza_orig) * 100 if distanza_orig else 0.0
                risultati.append(
                    {
                        "nome": nome,
                        "percorso": percorso,
                        "tempo": elapsed,
                        "distanza": distanza,
                        "miglioramento": miglioramento,
                        "completato": True,
                        "colore": colore,
                    }
                )
            except TimeoutError:
                elapsed = perf_counter() - start
                risultati.append(
                    {
                        "nome": nome,
                        "percorso": [],
                        "tempo": elapsed,
                        "distanza": None,
                        "miglioramento": None,
                        "completato": False,
                        "colore": colore,
                    }
                )

        completati = [r for r in risultati if r["completato"]]
        if completati:
            best = min(completati, key=lambda r: r["distanza"])
            distanza_opt = best["distanza"]
            miglioramento = best["miglioramento"]
            tempo = best["tempo"]
            stato = f"best={best['nome']}"
        else:
            distanza_opt = distanza_orig
            miglioramento = 0.0
            tempo = 0.0
            stato = "nessun algoritmo completato"

        out_path = output_dir / f"mezzo_{idx:02d}_{nome_mezzo.lower()}.png"
        visualizer.salva_confronto_algoritmi_per_mezzo(
            percorso_originale,
            risultati,
            str(out_path),
        )
        immagini_salvate += 1

        print(
            f"{idx:02d}. {nome_mezzo} | colli={len(percorso_originale)} | "
            f"dist_orig={distanza_orig:.2f} | dist_opt={distanza_opt:.2f} | "
            f"miglioramento={miglioramento:.2f}% | tempo={tempo:.4f}s | {stato}"
        )

    print()
    print(f"Immagini comparative salvate: {immagini_salvate} in {output_dir}/")


if __name__ == "__main__":
    main()

