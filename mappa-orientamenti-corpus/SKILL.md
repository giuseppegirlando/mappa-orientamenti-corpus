---
name: mappa-orientamenti-corpus
description: "Ricostruisce le tesi giurisprudenziali su un quesito da un CORPUS CHIUSO di sentenze fornite dall'utente (PDF o testo), senza fonti esterne, e — dopo la mappa neutra e un gate sulla posizione difesa — propone tesi difensive e fronti d'attacco etichettati per fondamento. Lavora su cartella, per fasi separate con arresto dopo ciascuna, con un unico report finale in prosa argomentativa. ATTIVARE ESCLUSIVAMENTE su richiesta nominativa espressa dell'utente: quando scrive 'mappa-orientamenti-corpus', 'usa la skill mappa-orientamenti-corpus', o un comando 'mappa fase' (mappa inventario, mappa schede, mappa tesi, mappa posizione, mappa strategia, mappa report, mappa stato). NON attivare per inferenza dal contesto, anche se l'utente carica sentenze e chiede di ricostruire orientamenti o contrasti senza nominare la skill: in quel caso rispondere normalmente e, al più, segnalare che la skill esiste."
---

# Mappa orientamenti su corpus chiuso

Skill creata dall'Avv. Giuseppe Girlando (Studio Legale Girlando, Catania), versione 1.0 dell'8 settembre 2026.

## Che cosa fa e perché è costruita così

Un avvocato che ha raccolto venti o trenta sentenze su un tema ha bisogno di due cose che si ostacolano a vicenda: una fotografia onesta di come la giurisprudenza si divide, e una strategia per la propria parte. Se la strategia arriva prima, la fotografia viene scattata a favore; se la fotografia viene dichiarata "vincente" per una tesi, la strategia deve poi smentirla. Per questo la skill lavora in due tempi separati da un gate: prima la mappa cieca, poi la posizione, poi la strategia.

La seconda ragione strutturale è il perimetro. Il corpus è chiuso: la skill non cerca nulla fuori dai file forniti e non attinge a conoscenza propria su norme, massime o precedenti. Ma il corpus l'ha selezionato l'utente, quindi "chiuso" non vuol dire "completo": ogni conclusione va detta come conclusione *sul corpus*, e i vuoti vanno dichiarati. Quando la strategia ha bisogno di qualcosa che nel corpus non c'è, la skill lo segna come "da verificare fuori corpus" e si ferma: la verifica esterna e lo stress test avvengono dopo, con altre skill (`ricerca-giurisprudenziale-aggiornata`, `avvocato-del-diavolo-small`).

## Interazione: una fase per volta

La skill non corre da sola fino al report. Ogni comando esegue una sola fase, mostra in chat il risultato o un riepilogo, aggiorna lo stato e si ferma; il comando successivo lo dà l'utente. Non concatenare mai due fasi, neppure se l'utente scrive "vai avanti fino alla fine": in quel caso spiega che i punti di arresto servono a correggere il tiro (quesito, raggruppamenti, schede, mappa) prima che l'errore si propaghi, e chiedi quale fase eseguire.

I file di `lavoro/` sono leggibili dall'utente in ogni momento: `inventario.md`, ogni scheda, `mappa-orientamenti.md` e `strategia.md` sono passaggi intermedi da rivedere, non scatole nere. Se l'utente corregge un file intermedio, la fase successiva parte dalla sua versione.

## Dove stanno i file

La skill è pensata per Cowork con una cartella di pratica: l'utente mette le sentenze in `<cartella>/input/sentenze/` e tutto il resto viene scritto lì. È l'unico ambiente in cui la continuità tra sessioni funziona, perché `lavoro/` e `stato-lavorazione.md` restano su disco.

In chat (claude.ai) i file caricati stanno in `/mnt/user-data/uploads/` e il filesystem si azzera tra una conversazione e l'altra: la skill può lavorare solo entro una sessione, copiando gli upload in una cartella di lavoro temporanea e restituendo i file intermedi come output. Con 20–30 sentenze la sessione non basta: dillo subito all'utente e proponi Cowork.

## Regole inderogabili

1. Usa soltanto il testo delle sentenze presenti in `input/sentenze/`. Non citare norme, massime, precedenti o dottrina che non compaiano in quel testo. Se una norma è citata dal giudice, la si riporta come citazione del giudice, non come conoscenza propria.
2. Ogni affermazione sul contenuto di una sentenza porta un riferimento: `(ID, p. N, «primi 10-15 parole del passaggio»)`. Se il testo non ha paginazione, si usa solo l'incipit. L'incipit deve essere letterale: serve al controllo automatico.
3. Distingui sempre fatti rilevanti, domanda, decisione, ratio decidendi, argomenti concorrenti, obiter e precedenti richiamati. Non attribuire a una sentenza un principio che non sia ricavabile dal suo testo; non uniformare decisioni diverse per comodità espositiva.
4. Ogni punto di ogni scheda porta un livello di certezza: *espresso* (il giudice lo dice), *inferito* (si ricava dal ragionamento), *incerto* (il testo lo consente ma non lo impone).
5. Ogni argomento della fase strategica porta un'etichetta di fondamento: `[attestato]` (una sentenza del corpus lo dice), `[costruito]` (ricavato per estensione, distinzione o contraddizione da sentenze del corpus, con indicazione di quali), `[da verificare fuori corpus]` (richiede fonti che nel corpus non ci sono; la skill lo formula come ipotesi e non lo sviluppa).
6. Se un file è illeggibile, incompleto o privo del passaggio necessario, dichiaralo nell'inventario e nella scheda. Non si riempie con quello che "probabilmente" dice.
7. Quando individui un contrasto, verifica se è reale o se dipende da differenze di fattispecie, disciplina applicabile, domanda, eccezioni, prova, rito o tempo. Un contrasto apparente vale quanto uno reale, ma va chiamato con il suo nome.
8. La posizione difesa non si chiede e non si assume prima che la mappa sia chiusa. Se l'utente la dichiara spontaneamente all'inizio, prendine nota in `stato-lavorazione.md` come "posizione dichiarata anticipatamente" e non usarla fino a `mappa posizione`.
9. Terminologia tecnico-giuridica italiana; prosa nel report finale (vedi `references/struttura-report.md`).

## Struttura della cartella di lavoro

```
<cartella pratica>/
├── input/sentenze/            ← i file forniti dall'utente (PDF, docx, txt, md)
├── lavoro/
│   ├── testi/                 ← testo estratto con marcatori di pagina [[p.N]]
│   ├── inventario.md
│   ├── schede/S01.md ... S30.md
│   ├── mappa-orientamenti.md  ← mappa neutra (bozza di lavoro)
│   ├── strategia.md           ← bozza di lavoro dopo il gate
│   └── stato-lavorazione.md
└── REPORT-orientamenti-<tema>.md   ← unico deliverable
```

Tutto ciò che sta in `lavoro/` è strumentale: serve alla continuità tra sessioni e al controllo, non va consegnato. Il deliverable è un solo file.

## Comandi

L'utente pilota la skill con comandi brevi. Ogni comando aggiorna `stato-lavorazione.md` alla fine.

| Comando | Effetto |
|---|---|
| `mappa inventario` | Fase 1: estrazione testi e censimento del corpus |
| `mappa schede` | Fase 2: schede analitiche a lotti di 5, con ripresa automatica |
| `mappa scheda S07` | Rifà o completa una singola scheda |
| `mappa tesi "<quesito>"` | Fase 3: mappa neutra degli orientamenti sul quesito |
| `mappa posizione` | Gate: chiede la posizione difesa e la registra |
| `mappa strategia` | Fase 4: tesi difensive e fronti d'attacco etichettati |
| `mappa report` | Fase 5: controllo delle citazioni e stesura del report unico |
| `mappa stato` | Legge `stato-lavorazione.md` e dice dove si è e cosa manca |

Se l'utente descrive l'obiettivo in linguaggio naturale senza comando, individua la fase corrispondente dallo stato di lavorazione e proponi il comando; non saltare fasi. Se manca `stato-lavorazione.md`, si parte dall'inventario.

## Fase 1 — Inventario

Esegui `scripts/prepara_corpus.py <cartella pratica>`. Lo script converte ogni file di `input/sentenze/` in testo con marcatori `[[p.N]]` (per i PDF nativi) o senza marcatori (per docx/txt/md, dove la pagina non esiste), scrive `lavoro/testi/` e un manifesto con lunghezza, presenza di testo, sospetti di scansione. Se un PDF risulta privo di testo (scansione), segnalalo e chiedi all'utente se vuole l'OCR o preferisce sostituire il file; non procedere a OCR di propria iniziativa su 30 file.

Poi, leggendo solo l'apertura e la chiusura di ciascun testo (intestazione, dispositivo), compila `lavoro/inventario.md`: una riga per sentenza con ID progressivo (S01, S02 …), organo e sezione, data e numero, grado, esito, nome file, stato del testo (completo / incompleto / illeggibile), e un'ipotesi di raggruppamento tematico. Segnala duplicati (stessa sentenza in due file, o stessa decisione in gradi diversi). Non sintetizzare ancora il merito: l'inventario serve a sapere con che cosa si lavora, e a decidere se il corpus è quello giusto prima di investire trenta schede.

Chiudi la fase dicendo all'utente quante sentenze sono lavorabili, quali problemi ci sono, e quali raggruppamenti hai ipotizzato. Aspetta conferma prima delle schede.

## Fase 2 — Schede

Una scheda per sentenza, nel formato di `references/scheda-sentenza.md`. Leggi il testo integrale della sentenza da `lavoro/testi/` solo quando ne fai la scheda (lettura just-in-time), mai tutte insieme: trenta sentenze non stanno in una sessione e non devono starci.

Lavora a lotti di cinque. Alla fine di ogni lotto aggiorna `stato-lavorazione.md` (schede fatte, prossimo ID) e chiedi se continuare. Se la sessione riparte, `mappa schede` legge lo stato e riprende dal primo ID mancante.

La scheda è tabellare e asciutta: è uno strumento di lavoro, non prosa. Due parti meritano attenzione speciale perché sono quelle che la fase 4 userà di più:

- la sezione **F, limiti applicativi**: presupposti, fatti ostativi, onere della prova, profili temporali e di rito, elementi che potrebbero distinguere il precedente. È il materiale del distinguishing.
- la sezione **H, tensioni interne**: punti in cui la motivazione dice una cosa e ne applica un'altra, in cui il principio enunciato è più largo o più stretto della regola applicata, in cui un argomento accessorio contraddice la ratio dichiarata. Queste tensioni non sono contrasti tra sentenze: stanno dentro una sola motivazione, e sono spesso il fronte d'attacco migliore. Se non ce ne sono, scrivilo.

## Fase 3 — Mappa neutra

Presuppone tutte le schede. Richiede il quesito giuridico preciso: se l'utente lo formula in modo vago, riformulalo tu e chiedi conferma prima di procedere, perché una mappa su un quesito sbagliato è inutile.

Lavora dalle schede, ma per ogni passaggio che citi nella mappa rileggi il punto nel testo originale in `lavoro/testi/` (cerca l'incipit). La scheda è una mediazione; la citazione va sull'originale.

Scrivi `lavoro/mappa-orientamenti.md` con questo contenuto, in questo ordine:

1. **Le tesi.** Per ciascun orientamento: regola di diritto in una frase; sentenze aderenti; ricostruzione fattispecie → questione → norma → interpretazione → presupposto → conclusione → effetto; ratio decisiva; onere della prova; limiti. Le sentenze che non aderiscono chiaramente a nessuna tesi vanno in una categoria propria, non forzate.
2. **Le ragioni sotto le tesi.** Che cosa muove davvero ciascun orientamento: un'esigenza sistematica, una lettura testuale, una preoccupazione di effetti pratici, un precedente ritenuto vincolante. È qui che si capisce se due tesi sono conciliabili.
3. **Contrasti.** Reali; apparenti (e da che cosa dipendono: fatti, rito, domanda, prova, disciplina intertemporale); mutamenti nel tempo; tensioni interne alle singole motivazioni raccolte dalle sezioni H.
4. **Punti di incontro.** Ciò su cui tutte le tesi concordano, anche implicitamente. Sono i punti che nessuna strategia può contestare.
5. **Spazi di conferma e confutazione.** Per ogni tesi: quali elementi del corpus la rafforzerebbero se ripresi, quali la indeboliscono, quali fattispecie non ha mai affrontato.
6. **Persuasività nel corpus.** Forza argomentativa, ampiezza e omogeneità dei precedenti, coerenza sistematica, vulnerabilità di ciascuna tesi. Non dichiarare una tesi "prevalente" o "vincente": descrivi i pesi e lascia il giudizio.
7. **Vuoti del corpus.** Fattispecie non coperte, gradi o organi assenti, salti temporali, questioni decise senza motivazione sufficiente. Punti che richiederebbero verifica esterna.

Alla fine della fase, la mappa è chiusa. Dillo esplicitamente e proponi `mappa posizione`.

## Gate — Posizione

Chiedi all'utente: quale parte assiste, quale risultato vuole ottenere (domanda o eccezione), in quale grado e rito, e se ci sono elementi di fatto della sua vicenda che ritiene decisivi. Registra tutto in `stato-lavorazione.md`. Da questo momento la mappa non si modifica più: se la strategia rivela un errore nella mappa, si annota come "correzione post-gate" con motivazione, per lasciare traccia del fatto che è avvenuta dopo la dichiarazione della posizione.

## Fase 4 — Strategia

Scrivi `lavoro/strategia.md`. Per la posizione dichiarata:

- **Tesi difensive.** Quali orientamenti del corpus sostengono la posizione, con quale forza, e a quali condizioni di fatto. Per ciascuna: come si argomenta, quali sentenze si citano, quali limiti (sezione F) vanno neutralizzati perché la controparte li userà per distinguere.
- **Fronti d'attacco.** Come si aggrediscono gli orientamenti contrari: distinguishing sulle fattispecie; sfruttamento delle tensioni interne (sezione H); riduzione della portata del principio alla regola effettivamente applicata; contrasti apparenti da far valere come tali e contrasti reali da far pesare; argomenti che una sentenza contraria concede incidentalmente e che possono essere ripresi.
- **Argomenti nuovi.** Costruzioni non attestate in nessuna sentenza ma ricavabili dal corpus: estensione di una ratio a una fattispecie non decisa, combinazione di due orientamenti, rovesciamento di un distinguishing. Vanno etichettati `[costruito]` con l'indicazione delle sentenze da cui derivano e della mossa logica compiuta.
- **Da verificare fuori corpus.** L'elenco di ciò che servirebbe e non c'è: un precedente di legittimità sul punto, l'evoluzione normativa, una norma citata dal giudice il cui testo vigente non è nel corpus. Formulato come domanda di ricerca, pronto per `ricerca-giurisprudenziale-aggiornata`.
- **Ordine di attacco proposto.** Quale argomento va per primo e perché, quale tenere di riserva, quale non usare pur essendo disponibile.

Ogni argomento porta l'etichetta di fondamento. Non è un'omissione se un argomento resta `[da verificare fuori corpus]`: è la skill che fa il suo mestiere.

## Fase 5 — Report unico

Prima di scrivere, esegui `scripts/verifica_citazioni.py <cartella pratica> lavoro/mappa-orientamenti.md lavoro/strategia.md`. Lo script estrae ogni riferimento `(ID, p. N, «incipit»)` e controlla che l'incipit esista nel testo di quell'ID e, dove c'è paginazione, nella pagina indicata. Correggi ogni riferimento non trovato rileggendo l'originale; se il passaggio non esiste, l'affermazione che vi si appoggia va tolta o riformulata come inferenza. Non scrivere il report finché lo script non passa pulito o finché ogni scarto non è spiegato.

Poi scrivi `REPORT-orientamenti-<tema>.md` seguendo `references/struttura-report.md`. È l'unico deliverable: prosa argomentativa continua, senza elenchi puntati e senza tabelle nel corpo, con i riferimenti tra parentesi nel testo. Le schede non si allegano. Se nella cartella esiste `stile-scrittura-legale.md` o un file di stile dello studio, leggilo e applicalo; altrimenti valgono le regole del riferimento.

Chiudi con il rinvio: verifica esterna dei punti "da verificare fuori corpus" con `ricerca-giurisprudenziale-aggiornata`; stress test della strategia con `avvocato-del-diavolo-small`, passandole il report.

## Continuità tra sessioni

`stato-lavorazione.md` (modello in `references/stato-lavorazione.md`) registra fase corrente, ID delle schede completate, quesito, posizione (dopo il gate), correzioni post-gate, problemi aperti. All'inizio di ogni sessione leggilo prima di qualsiasi altra cosa; alla fine di ogni comando aggiornalo. Non rileggere schede o testi già lavorati se non servono al comando in corso.
