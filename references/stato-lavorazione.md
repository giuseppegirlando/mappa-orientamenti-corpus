# Modello — `lavoro/stato-lavorazione.md`

Leggerlo all'inizio di ogni sessione, prima di qualsiasi altra cosa, e aggiornarlo alla fine di ogni comando. È l'unica memoria tra sessioni: quello che non è scritto qui è perduto.

È uno **stato**, non un diario: deve stare in una pagina. Le osservazioni di merito (contrasti scoperti, collegamenti tra sentenze, dubbi di pertinenza) vanno in `lavoro/note-lavorazione.md`; i fatti della causa raccolti al gate in `lavoro/scheda-fatti.md`. Qui resta al più una riga di rinvio. L'intestazione "Fase corrente" si aggiorna a ogni chiusura di fase.

```markdown
# Stato di lavorazione — <tema>

## Fase corrente
<avvio | inventario | schede | mappa 3a | mappa 3b | gate | strategia | report | chiuso>
Fase successiva proposta: <…>
Piano sessioni: <2 sessioni (A: fasi 1-2; B: fasi 3-5) | 3 sessioni | unica> — sessione in corso: <A/B/C>

## Corpus
- Sentenze lavorabili: N (S01–Sxx)
- Problemi: <file illeggibili, incompleti, duplicati, sospette scansioni, con ID>
- Provenienza: <ricerca su banca dati (quale query) | citate dalla controparte |
  materiale del cliente | raccolta mista — dettagliare>
- Raggruppamenti ipotizzati in inventario: <…>

## Quesito
- Provvisorio (fase 1): <testo>
- Definitivo (fase 3): <testo, oppure "non ancora confermato">
- Modifiche rispetto al provvisorio e perché: <…>

## Schede
- Completate: S01–Sxx (oppure elenco)
- Mancanti / da rifare: <ID e motivo>
- Sinossi allineata alle schede: <sì / no, mancano …>
- Controllo citazioni sulle schede: <pulito | N scarti, di cui M corretti>
- Osservazioni di merito: v. lavoro/note-lavorazione.md

## Mappa
- Raggruppamenti confermati dall'utente il: <data>
- Controllo citazioni su mappa-orientamenti.md: <pulito | N scarti>
- Chiusa il: <data> | aperta

## Posizione difesa (solo dopo il gate)
- Parte assistita:
- Risultato voluto:
- Grado, rito, foro:
- Fatti accertati / non accertati: v. lavoro/scheda-fatti.md
- Posizione dichiarata anticipatamente prima del gate: <sì/no; se sì, non usata fino al gate>

## Correzioni post-gate
<data, che cosa è cambiato nella mappa, perché>

## Verifica citazioni (fase 5)
- Ultimo esito dello script: <pulito | N scarti, di cui M spiegati>
- Su quali file: <mappa-orientamenti.md, strategia.md, REPORT-…>
- Sentenze mai citate con citazione propria: <ID, con la ragione>

## Problemi aperti
<solo quelli ancora aperti; i risolti si cancellano, non si barrano>
```
