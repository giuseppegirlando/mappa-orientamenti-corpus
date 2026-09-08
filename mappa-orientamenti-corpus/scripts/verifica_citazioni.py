#!/usr/bin/env python3
# Skill mappa-orientamenti-corpus — creata dall'Avv. Giuseppe Girlando, Studio Legale Girlando (Catania)
"""Verifica che ogni riferimento (Sxx, p. N, «incipit») esista nel testo della sentenza.

Uso: python3 verifica_citazioni.py <cartella_pratica> <file.md> [<file.md> ...]

Legge la corrispondenza ID -> file da <cartella>/lavoro/inventario.md (cerca righe che
contengono un ID "Sxx" e un nome di file presente in lavoro/testi/). Poi, per ogni
riferimento trovato nei file markdown indicati:
  - controlla che l'incipit compaia nel testo dell'ID (confronto normalizzato:
    minuscole, spazi compressi, apostrofi e virgolette uniformati);
  - se è indicata una pagina e il testo è paginato, controlla che compaia in quella pagina.
Stampa un elenco degli scarti. Esce con codice 1 se ce ne sono.
"""
import re
import sys
import unicodedata
from pathlib import Path

RIF = re.compile(r"\(\s*(S\d{2,3})\s*(?:,\s*p\.\s*(\d+))?\s*,\s*«([^»]{6,})»\s*\)")
PAG = re.compile(r"\[\[p\.(\d+)\]\]")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[\s\-\u00ad]+", " ", s)  # spazi, trattini e trattini morbidi (a capo)
    return s.lower().strip()


def mappa_id(base: Path) -> dict[str, Path]:
    testi = base / "lavoro" / "testi"
    stems = {p.stem: p for p in testi.glob("*.txt")}
    inv = base / "lavoro" / "inventario.md"
    m: dict[str, Path] = {}
    if inv.exists():
        for riga in inv.read_text(encoding="utf-8").splitlines():
            ids = re.findall(r"\bS\d{2,3}\b", riga)
            if not ids:
                continue
            for stem, p in stems.items():
                if stem in riga or (stem + ".pdf") in riga or (stem + ".docx") in riga:
                    m.setdefault(ids[0], p)
                    break
    return m


def pagine(testo: str) -> list[tuple[int, str]]:
    parti = PAG.split(testo)
    if len(parti) == 1:
        return []
    out = []
    for i in range(1, len(parti), 2):
        out.append((int(parti[i]), parti[i + 1]))
    return out


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    base = Path(sys.argv[1]).expanduser().resolve()
    idmap = mappa_id(base)
    if not idmap:
        print("Attenzione: nessuna corrispondenza ID->file ricavata da lavoro/inventario.md. "
              "L'inventario deve riportare, sulla stessa riga, l'ID (S01…) e il nome del file.")
    cache: dict[str, str] = {}
    scarti, totale = [], 0

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
                p = idmap.get(sid)
                if not p:
                    scarti.append((md.name, nlin, sid, pag, inc, "ID non mappato"))
                    continue
                testo = cache.setdefault(sid, p.read_text(encoding="utf-8", errors="replace"))
                ninc = norm(inc)
                if ninc not in norm(testo):
                    scarti.append((md.name, nlin, sid, pag, inc, "incipit non trovato nel testo"))
                    continue
                if pag:
                    pp = pagine(testo)
                    if pp:
                        trovato = any(n == int(pag) and ninc in norm(t) for n, t in pp)
                        if not trovato:
                            dove = [n for n, t in pp if ninc in norm(t)]
                            scarti.append((md.name, nlin, sid, pag, inc,
                                           f"pagina errata (trovato a p. {dove})"))

    print(f"Riferimenti controllati: {totale} — scarti: {len(scarti)}")
    for s in scarti:
        print(f"  {s[0]}:{s[1]}  {s[2]} p.{s[3] or '-'}  «{s[4][:50]}»  → {s[5]}")
    return 1 if scarti else 0


if __name__ == "__main__":
    sys.exit(main())
