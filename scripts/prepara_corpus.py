#!/usr/bin/env python3
# Skill mappa-orientamenti-corpus — creata dall'Avv. Giuseppe Girlando, Studio Legale Girlando (Catania)
"""Prepara il corpus: crea la struttura, assegna gli ID e converte le sentenze in testo.

Uso:
    python3 prepara_corpus.py <cartella_pratica> [--da <cartella_sorgente>] [--no-raccogli]

Che cosa fa, nell'ordine:
 1. crea <cartella>/input/sentenze/ e <cartella>/lavoro/testi/ se non esistono;
 2. raccoglie in input/sentenze/ i file di sentenza trovati al primo livello della cartella
    di pratica (o in --da), spostandoli; con --no-raccogli non sposta nulla;
 3. verifica le dipendenze di estrazione necessarie ai formati presenti;
 4. assegna gli ID S01, S02 ... in ordine alfabetico di nome file, CONSERVANDO quelli gia'
    presenti in lavoro/mappa-id.tsv (i file nuovi prendono ID successivi: nessuno slitta);
 5. scrive lavoro/testi/Sxx.txt — PDF con marcatori "[[p.N]]" a inizio pagina (pdftotext
    -layout, fallback pypdf), docx via pandoc o python-docx, txt/md copiati;
 6. riscrive lavoro/mappa-id.tsv con id, file, formato, pagine, caratteri, stato, anteprima.

Non fa OCR: i PDF privi di testo vengono soltanto segnalati come "sospetta_scansione".
"""
import csv
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ESTENSIONI = {".pdf", ".docx", ".txt", ".md"}
# non sono sentenze: non vanno raccolti in input/sentenze/ anche se stanno nella cartella
ESCLUSI = ("report", "readme", "stile", "note", "appunti", "inventario", "sinossi", "strategia")
SOGLIA_CARATTERI_PER_PAGINA = 200  # sotto questa media, il PDF è probabilmente una scansione


# --------------------------------------------------------------------------- dipendenze

def dipendenze(estensioni: set[str]) -> list[str]:
    """Ritorna l'elenco dei problemi bloccanti per i formati effettivamente presenti."""
    problemi = []
    if ".pdf" in estensioni:
        ok_pdftotext = shutil.which("pdftotext") is not None
        try:
            import pypdf  # noqa: F401
            ok_pypdf = True
        except Exception:
            ok_pypdf = False
        if not (ok_pdftotext or ok_pypdf):
            problemi.append(
                "PDF presenti ma nessun estrattore disponibile. "
                "Installare poppler-utils (comando pdftotext) oppure: pip install pypdf"
            )
        elif not ok_pdftotext:
            print("Avviso: pdftotext non trovato, uso pypdf (impaginazione meno fedele).")
    if ".docx" in estensioni:
        ok_pandoc = shutil.which("pandoc") is not None
        try:
            import docx  # noqa: F401
            ok_docx = True
        except Exception:
            ok_docx = False
        if not (ok_pandoc or ok_docx):
            problemi.append(
                "DOCX presenti ma nessun estrattore disponibile. "
                "Installare pandoc oppure: pip install python-docx"
            )
    return problemi


# --------------------------------------------------------------------------- estrazione

def testo_pdf(src: Path) -> tuple[str, int]:
    """Ritorna (testo con marcatori di pagina, n_pagine)."""
    pagine: list[str] = []
    if shutil.which("pdftotext"):
        try:
            out = subprocess.run(
                ["pdftotext", "-layout", str(src), "-"],
                capture_output=True, text=True, check=True
            ).stdout
            pagine = out.split("\f")
            if pagine and not pagine[-1].strip():
                pagine = pagine[:-1]
        except Exception:
            pagine = []
    if not pagine:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(str(src))
        pagine = [(p.extract_text() or "") for p in reader.pages]
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


# --------------------------------------------------------------------------- ID stabili

def id_esistenti(tsv: Path) -> dict[str, str]:
    """Legge mappa-id.tsv e ritorna {nome_file_originale: ID}."""
    m: dict[str, str] = {}
    if not tsv.exists():
        return m
    with tsv.open(encoding="utf-8", newline="") as f:
        for riga in csv.DictReader(f, delimiter="\t"):
            if riga.get("id") and riga.get("file"):
                m[riga["file"]] = riga["id"]
    return m


def assegna_id(files: list[Path], gia_noti: dict[str, str]) -> dict[str, str]:
    """Conserva gli ID gia' assegnati; ai file nuovi da' i primi ID liberi."""
    usati = {v for k, v in gia_noti.items() if k in {f.name for f in files}}
    prossimo = 1
    mappa: dict[str, str] = {}
    for f in files:
        if f.name in gia_noti:
            mappa[f.name] = gia_noti[f.name]
    for f in files:
        if f.name in mappa:
            continue
        while f"S{prossimo:02d}" in usati:
            prossimo += 1
        sid = f"S{prossimo:02d}"
        mappa[f.name] = sid
        usati.add(sid)
    return mappa


# --------------------------------------------------------------------------- raccolta

def raccogli(dest: Path, sorgente: Path) -> list[str]:
    """Sposta in dest i file di sentenza trovati al primo livello di sorgente."""
    mossi = []
    if not sorgente.is_dir() or sorgente.resolve() == dest.resolve():
        return mossi
    for p in sorted(sorgente.iterdir()):
        if not p.is_file() or p.name.startswith(".") or p.suffix.lower() not in ESTENSIONI:
            continue
        if p.name.startswith("_") or p.name.lower().startswith(ESCLUSI):
            continue
        target = dest / p.name
        if target.exists():
            continue
        shutil.move(str(p), str(target))
        mossi.append(p.name)
    return mossi


# --------------------------------------------------------------------------- main

def main() -> int:
    args = [a for a in sys.argv[1:]]
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2
    base = Path(args[0]).expanduser().resolve()
    da: Path | None = None
    fai_raccolta = True
    i = 1
    while i < len(args):
        if args[i] == "--da" and i + 1 < len(args):
            da = Path(args[i + 1]).expanduser().resolve()
            i += 2
        elif args[i] == "--no-raccogli":
            fai_raccolta = False
            i += 1
        else:
            print(f"Argomento non riconosciuto: {args[i]}")
            return 2

    src_dir = base / "input" / "sentenze"
    out_dir = base / "lavoro" / "testi"
    src_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    if fai_raccolta:
        mossi = raccogli(src_dir, da if da else base)
        if mossi:
            print(f"Raccolti in input/sentenze/ ({len(mossi)}): " + ", ".join(mossi))

    files = sorted(
        (p for p in src_dir.iterdir() if p.is_file() and not p.name.startswith(".")),
        key=lambda p: unicodedata.normalize("NFKD", p.name).lower()
    )
    if not files:
        print(f"Nessun file in {src_dir}. Mettere qui le sentenze (pdf, docx, txt, md).")
        return 1

    problemi_dip = dipendenze({p.suffix.lower() for p in files})
    if problemi_dip:
        for p in problemi_dip:
            print(f"BLOCCANTE: {p}")
        return 1

    tsv = base / "lavoro" / "mappa-id.tsv"
    mappa = assegna_id(files, id_esistenti(tsv))

    righe = []
    for src in files:
        sid = mappa[src.name]
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

        if testo:
            (out_dir / f"{sid}.txt").write_text(testo, encoding="utf-8")
        anteprima = " ".join(testo.strip().split())[:160]
        righe.append([sid, src.name, ext.lstrip("."), pagine, len(testo), stato, anteprima])
        print(f"{sid}  {src.name:52.52s} {stato:22s} pag={pagine:<4d} car={len(testo)}")

    with tsv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["id", "file", "formato", "pagine", "caratteri", "stato", "anteprima"])
        w.writerows(righe)
    print(f"\nMappa ID: {tsv}\nTesti:    {out_dir}")

    problemi = [r for r in righe if r[5] != "ok"]
    if problemi:
        print(f"\nDa segnalare all'utente ({len(problemi)}):")
        for r in problemi:
            print(f"  {r[0]}  {r[1]}  → {r[5]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
