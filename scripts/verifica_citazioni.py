#!/usr/bin/env python3
# Skill mappa-orientamenti-corpus — creata dall'Avv. Giuseppe Girlando, Studio Legale Girlando (Catania)
"""Verifica che ogni riferimento (Sxx, p. N, «incipit») esista davvero nel testo della sentenza.

Uso:
    python3 verifica_citazioni.py <cartella_pratica> <file.md> [<file.md> ...]
    (anche lavoro/schede/*.md: la shell espande il glob)

v1.2: per ogni incipit non trovato propone il passaggio piu' simile del testo.

La corrispondenza ID -> testo e' diretta: lavoro/testi/Sxx.txt, come scritto da
prepara_corpus.py. Nessuna deduzione dal testo dell'inventario, quindi nessun controllo
che gira a vuoto perche' un nome di file e' stato trascritto in modo diverso.

Per ogni riferimento trovato nei file markdown indicati:
  - controlla che l'incipit compaia nel testo di quell'ID (confronto normalizzato:
    minuscole, spazi compressi, trattini di a capo e apostrofi uniformati);
  - se e' indicata una pagina e il testo e' paginato, controlla che compaia in quella
    pagina e, se no, dice a quale pagina si trova.
Segnala inoltre le sentenze del corpus mai citate e gli ID citati che non esistono.
Esce con codice 1 se ci sono scarti.
"""
import csv
import difflib
import re
import sys
import unicodedata
from pathlib import Path

RIF = re.compile(r"\(\s*(S\d{2,3})\s*(?:,\s*p\.\s*(\d+))?\s*,\s*«([^»]{6,})»\s*\)")
PAG = re.compile(r"\[\[p\.(\d+)\]\]")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"[\s\-\u00ad\u2010-\u2015]+", " ", s)
    return s.lower().strip()


def mappa_id(base: Path) -> dict[str, Path]:
    """ID -> file di testo. Diretta dai nomi in lavoro/testi/, che li scrive lo script."""
    testi = base / "lavoro" / "testi"
    return {p.stem: p for p in sorted(testi.glob("S*.txt"))} if testi.is_dir() else {}


def etichette(base: Path) -> dict[str, str]:
    """ID -> nome del file originale, solo per rendere leggibili i messaggi."""
    tsv = base / "lavoro" / "mappa-id.tsv"
    out: dict[str, str] = {}
    if tsv.exists():
        with tsv.open(encoding="utf-8", newline="") as f:
            for riga in csv.DictReader(f, delimiter="\t"):
                if riga.get("id"):
                    out[riga["id"]] = riga.get("file", "")
    return out


def pagine(testo: str) -> list[tuple[int, str]]:
    parti = PAG.split(testo)
    if len(parti) == 1:
        return []
    return [(int(parti[i]), parti[i + 1]) for i in range(1, len(parti), 2)]


def vicino(ninc: str, ntesto: str) -> str:
    """Passaggio del testo piu' simile all'incipit non trovato (aiuta a correggere senza grep)."""
    parole = ninc.split()
    if len(parole) < 3:
        return ""
    chiave = " ".join(parole[:2])
    L = len(ninc)
    cands = []
    start = 0
    while True:
        i = ntesto.find(chiave, start)
        if i < 0 or len(cands) > 200:
            break
        cands.append(ntesto[i:i + L + 20])
        start = i + 1
    if not cands:
        # ripiego: finestre allineate sulla parola piu' lunga
        lunga = max(parole, key=len)
        start = 0
        while True:
            i = ntesto.find(lunga, start)
            if i < 0 or len(cands) > 200:
                break
            cands.append(ntesto[max(0, i - L // 2):i + L])
            start = i + 1
    if not cands:
        return ""
    best = max(cands, key=lambda c: difflib.SequenceMatcher(None, ninc, c).ratio())
    r = difflib.SequenceMatcher(None, ninc, best).ratio()
    return f"{best.strip()[:L + 20]} (somiglianza {r:.2f})" if r >= 0.6 else ""


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    base = Path(sys.argv[1]).expanduser().resolve()
    idmap = mappa_id(base)
    nomi = etichette(base)
    if not idmap:
        print(f"Nessun testo in {base/'lavoro'/'testi'}. Eseguire prima prepara_corpus.py.")
        return 2

    cache: dict[str, str] = {}
    scarti: list[tuple] = []
    citati: set[str] = set()
    totale = 0

    for fmd in sys.argv[2:]:
        md = Path(fmd)
        if not md.is_absolute():
            md = base / md
        if not md.exists():
            print(f"File non trovato: {md}")
            continue
        for nlin, riga in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            for sid, pag, inc in RIF.findall(riga):
                totale += 1
                citati.add(sid)
                p = idmap.get(sid)
                if not p:
                    scarti.append((md.name, nlin, sid, pag, inc, "ID inesistente nel corpus"))
                    continue
                testo = cache.setdefault(sid, p.read_text(encoding="utf-8", errors="replace"))
                ninc = norm(inc)
                ntesto = norm(testo)
                if ninc not in ntesto:
                    sugg = vicino(ninc, ntesto)
                    msg = "incipit non trovato nel testo" + (f" — piu' vicino: «{sugg}»" if sugg else "")
                    scarti.append((md.name, nlin, sid, pag, inc, msg))
                    continue
                if pag:
                    pp = pagine(testo)
                    if pp and not any(n == int(pag) and ninc in norm(t) for n, t in pp):
                        dove = [n for n, t in pp if ninc in norm(t)]
                        scarti.append((md.name, nlin, sid, pag, inc,
                                       f"pagina errata (trovato a p. {dove})"))

    print(f"Riferimenti controllati: {totale} — scarti: {len(scarti)}")
    for s in scarti:
        etich = f" [{nomi.get(s[2], '')}]" if nomi.get(s[2]) else ""
        print(f"  {s[0]}:{s[1]}  {s[2]}{etich} p.{s[3] or '-'}  «{s[4][:50]}»  → {s[5]}")

    mai = sorted(set(idmap) - citati)
    if mai:
        print(f"\nSentenze del corpus mai citate ({len(mai)}): " + ", ".join(mai))
        print("Non e' un errore, ma va spiegato: o non sono pertinenti, o la mappa le ha perse.")
    return 1 if scarti else 0


if __name__ == "__main__":
    sys.exit(main())
