#!/usr/bin/env python3
# Skill mappa-orientamenti-corpus — creata dall'Avv. Giuseppe Girlando, Studio Legale Girlando (Catania)
"""Prepara il corpus: converte i file di input/sentenze/ in testo con marcatori di pagina.

Uso: python3 prepara_corpus.py <cartella_pratica>

Per ciascun file in <cartella>/input/sentenze/ scrive <cartella>/lavoro/testi/<nome>.txt.
- PDF: una riga "[[p.N]]" prima del testo di ogni pagina (pdftotext -layout; fallback pypdf).
- DOCX: testo estratto (pandoc o python-docx); nessuna paginazione.
- TXT/MD: copiati.
Scrive inoltre <cartella>/lavoro/manifesto.tsv con: file, formato, pagine, caratteri,
stato (ok / sospetta_scansione / vuoto / errore) e un'anteprima dell'intestazione.
Non fa OCR: i PDF senza testo vengono soltanto segnalati.
"""
import csv
import shutil
import subprocess
import sys
from pathlib import Path

SOGLIA_CARATTERI_PER_PAGINA = 200  # sotto questa media, il PDF è probabilmente una scansione


def testo_pdf(src: Path) -> tuple[str, int]:
    """Ritorna (testo con marcatori, n_pagine)."""
    pagine: list[str] = []
    try:
        out = subprocess.run(
            ["pdftotext", "-layout", str(src), "-"],
            capture_output=True, text=True, check=True
        ).stdout
        pagine = out.split("\f")
        if pagine and not pagine[-1].strip():
            pagine = pagine[:-1]
    except Exception:
        try:
            from pypdf import PdfReader  # type: ignore
            reader = PdfReader(str(src))
            pagine = [(p.extract_text() or "") for p in reader.pages]
        except Exception as e:  # pragma: no cover
            raise RuntimeError(f"estrazione fallita: {e}")
    parti = [f"[[p.{i}]]\n{t.strip()}\n" for i, t in enumerate(pagine, start=1)]
    return "\n".join(parti), len(pagine)


def testo_docx(src: Path) -> str:
    if shutil.which("pandoc"):
        return subprocess.run(
            ["pandoc", str(src), "-t", "plain", "--wrap=none"],
            capture_output=True, text=True, check=True
        ).stdout
    from docx import Document  # type: ignore
    return "\n".join(p.text for p in Document(str(src)).paragraphs)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    base = Path(sys.argv[1]).expanduser().resolve()
    src_dir = base / "input" / "sentenze"
    out_dir = base / "lavoro" / "testi"
    if not src_dir.is_dir():
        print(f"Cartella non trovata: {src_dir}")
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    righe = []
    for src in sorted(p for p in src_dir.iterdir() if p.is_file() and not p.name.startswith(".")):
        ext = src.suffix.lower()
        stato, pagine, testo = "ok", 0, ""
        try:
            if ext == ".pdf":
                testo, pagine = testo_pdf(src)
                media = len(testo.strip()) / max(pagine, 1)
                if not testo.strip():
                    stato = "vuoto"
                elif media < SOGLIA_CARATTERI_PER_PAGINA:
                    stato = "sospetta_scansione"
            elif ext == ".docx":
                testo = testo_docx(src)
            elif ext in (".txt", ".md"):
                testo = src.read_text(encoding="utf-8", errors="replace")
            else:
                stato = "formato_non_gestito"
        except Exception as e:
            stato, testo = f"errore: {e}", ""

        dest = out_dir / (src.stem + ".txt")
        if testo:
            dest.write_text(testo, encoding="utf-8")
        anteprima = " ".join(testo.strip().split())[:160]
        righe.append([src.name, ext.lstrip("."), pagine, len(testo), stato, anteprima])
        print(f"{src.name:60s} {stato:22s} pag={pagine:<4d} car={len(testo)}")

    man = base / "lavoro" / "manifesto.tsv"
    with man.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["file", "formato", "pagine", "caratteri", "stato", "anteprima"])
        w.writerows(righe)
    print(f"\nManifesto: {man}")
    problemi = [r for r in righe if r[4] != "ok"]
    if problemi:
        print(f"File da segnalare all'utente: {len(problemi)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
