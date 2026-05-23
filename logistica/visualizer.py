"""
Visualizzazione grafica dei percorsi di consegna.
"""

from __future__ import annotations

from math import ceil
from pathlib import Path
from typing import Sequence, Tuple

import matplotlib.pyplot as plt


class RouteVisualizer:
    def __init__(self, origine: Tuple[float, float] = (0.0, 0.0)):
        self.origine = origine

    def _coord(self, collo) -> Tuple[float, float]:
        cliente = collo.cliente
        if cliente is None:
            raise ValueError("Ogni collo deve avere un cliente associato")
        return float(cliente.lat), float(cliente.lng)

    def _plot_route(self, ax, colli: Sequence, titolo: str, color: str):
        punti_x = [self.origine[0]]
        punti_y = [self.origine[1]]

        for collo in colli:
            x, y = self._coord(collo)
            punti_x.append(x)
            punti_y.append(y)

        punti_x.append(self.origine[0])
        punti_y.append(self.origine[1])

        ax.plot(punti_x, punti_y, marker="o", color=color, linewidth=2)
        ax.scatter([self.origine[0]], [self.origine[1]], color="black", s=90, label="Origine", zorder=3)

        for collo in colli:
            x, y = self._coord(collo)
            ax.annotate(str(collo.id), (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)

        ax.set_title(titolo)
        ax.set_xlabel("Lat")
        ax.set_ylabel("Lng")
        ax.grid(True, alpha=0.3)
        ax.legend()

    def mostra_confronto(
        self,
        percorso_originale: Sequence,
        percorso_ottimizzato: Sequence,
        output_path: str = "percorsi.png",
        show: bool = False,
    ) -> str:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
        self._plot_route(axes[0], percorso_originale, "Percorso originale", "tab:red")
        self._plot_route(axes[1], percorso_ottimizzato, "Percorso ottimizzato", "tab:green")

        output = Path(output_path)
        fig.savefig(output, dpi=150)

        if show:
            plt.show()
        else:
            plt.close(fig)

        return str(output)

    def salva_confronto_percorso(
        self,
        percorso_originale: Sequence,
        percorso_ottimizzato: Sequence,
        titolo_ottimizzato: str,
        output_path: str,
    ) -> str:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
        self._plot_route(axes[0], percorso_originale, "Originale", "black")
        self._plot_route(axes[1], percorso_ottimizzato, titolo_ottimizzato, "tab:green")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=150)
        plt.close(fig)
        return str(output)

    def mostra_griglia(
        self,
        percorsi: Sequence[tuple[str, Sequence, str]],
        output_path: str = "percorsi.png",
        show: bool = False,
    ) -> str:
        if not percorsi:
            raise ValueError("Serve almeno un percorso da visualizzare")

        colonne = 2
        righe = ceil(len(percorsi) / colonne)
        fig, axes = plt.subplots(righe, colonne, figsize=(7 * colonne, 5 * righe), constrained_layout=True)

        axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for ax, (titolo, percorso, colore) in zip(axes_flat, percorsi):
            self._plot_route(ax, percorso, titolo, colore)

        for ax in axes_flat[len(percorsi):]:
            ax.axis("off")

        output = Path(output_path)
        fig.savefig(output, dpi=150)

        if show:
            plt.show()
        else:
            plt.close(fig)

        return str(output)

    def salva_progressione_confronto(
        self,
        percorso_originale: Sequence,
        percorso_ottimizzato: Sequence,
        output_dir: str = "percorsi_step",
        frames: int = 20,
    ) -> list[str]:
        output_folder = Path(output_dir)
        output_folder.mkdir(parents=True, exist_ok=True)

        limite = min(frames, len(percorso_originale), len(percorso_ottimizzato))
        immagini = []

        for idx in range(1, limite + 1):
            fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
            self._plot_route(axes[0], percorso_originale[:idx], f"Originale - step {idx}", "tab:red")
            self._plot_route(axes[1], percorso_ottimizzato[:idx], f"Ottimizzato - step {idx}", "tab:green")

            output_path = output_folder / f"percorso_{idx:02d}.png"
            fig.savefig(output_path, dpi=150)
            plt.close(fig)
            immagini.append(str(output_path))

        return immagini

    def salva_immagini_per_percorso(
        self,
        percorso_originale: Sequence,
        percorsi_ottimizzati: Sequence[tuple[str, Sequence, str]],
        output_dir: str = "percorsi_algo",
    ) -> list[str]:
        output_folder = Path(output_dir)
        output_folder.mkdir(parents=True, exist_ok=True)

        immagini = []
        for idx, (nome, percorso, colore) in enumerate(percorsi_ottimizzati, start=1):
            fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
            self._plot_route(axes[0], percorso_originale, "Originale", "black")
            self._plot_route(axes[1], percorso, nome, colore)

            slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in nome).strip("_")
            output_path = output_folder / f"{idx:02d}_{slug}.png"
            fig.savefig(output_path, dpi=150)
            plt.close(fig)
            immagini.append(str(output_path))

        return immagini

    def salva_confronto_algoritmi_per_mezzo(
        self,
        percorso_originale: Sequence,
        risultati_algoritmi: Sequence[dict],
        output_path: str,
    ) -> str:
        pannelli = [("Originale", percorso_originale, "black", True)]
        for r in risultati_algoritmi:
            pannelli.append((r["nome"], r.get("percorso", []), r.get("colore", "tab:blue"), r.get("completato", False)))

        colonne = 3
        righe = ceil(len(pannelli) / colonne)
        fig, axes = plt.subplots(righe, colonne, figsize=(6 * colonne, 4.8 * righe), constrained_layout=True)
        axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for ax, (titolo, percorso, colore, completato) in zip(axes_flat, pannelli):
            if completato and percorso:
                self._plot_route(ax, percorso, titolo, colore)
            elif titolo == "Originale":
                self._plot_route(ax, percorso, titolo, colore)
            else:
                ax.set_title(f"{titolo} (timeout)")
                ax.axis("off")
                ax.text(0.5, 0.5, "Timeout", ha="center", va="center", fontsize=12, transform=ax.transAxes)

        for ax in axes_flat[len(pannelli):]:
            ax.axis("off")

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, dpi=150)
        plt.close(fig)
        return str(out)
