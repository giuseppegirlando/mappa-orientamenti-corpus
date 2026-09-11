---
name: mappa-orientamenti-corpus
description: "Ricostruisce le tesi giurisprudenziali su un quesito da un CORPUS CHIUSO di sentenze fornite dall'utente (PDF o testo), senza fonti esterne, e — dopo la mappa neutra e un gate sulla posizione difesa — propone tesi difensive e fronti d'attacco etichettati per fondamento. Lavora su cartella, per fasi separate con arresto dopo ciascuna, con un unico report finale in prosa argomentativa. ESEGUIRE solo su richiesta espressa: quando l'utente scrive 'corpus', 'mappa-orientamenti-corpus', o un comando 'corpus ...' (corpus avvia, corpus stato, corpus schede tutte, corpus rifai Sxx). PROPORRE, senza eseguire nulla, quando l'utente carica o indica una raccolta di sentenze e chiede di ricostruire orientamenti, contrasti o tesi a confronto: in quel caso rispondere normalmente e aggiungere una riga che segnala l'esistenza della skill e chiede se avviarla. Non avviare mai la lavorazione per sola inferenza dal contesto."
---

# Mappa orientamenti su corpus chiuso

Skill creata dall'Avv. Giuseppe Girlando (Studio Legale Girlando, Catania), versione 1.2 del 9 settembre 2026.

Novità della 1.2 rispetto alla 1.1, ricavate dal primo uso reale su un corpus di 32 sentenze: schede prodotte in parallelo da subagenti e senza arresto tra i lotti; controllo citazioni anticipato a fine fase 2 e fine fase 3b; gate che raccoglie anche i fatti e i documenti della causa; divieto di inferire alcunché dai nomi dei file; stato di lavorazione tenuto asciutto; punti di taglio consigliati tra sessioni.

## Che cosa fa e perché è costruita così

Un avvocato che ha raccolto venti o trenta sentenze su un tema ha bisogno di due cose che si ostacolano a vicenda: una fotografia onesta di come la giurisprudenza si divide, e una strategia per la propria parte. Se la strategia arriva prima, la fotografia viene scattata a favore; se la fotografia viene dichiarata "vincente" per una tesi, la strategia deve poi smentirla. Per questo la skill lavora in due tempi separati da un gate: prima la mappa cieca, poi la posizione, poi la strategia.

La seconda ragione strutturale è il perimetro. Il corpus è chiuso: la skill non cerca nulla fuori dai file forniti e non attinge a conoscenza propria su norme, massime o precedenti. Ma il corpus l'ha selezionato l'utente, quindi "chiuso" non vuol dire "completo": ogni conclusione va detta come conclusione *sul corpus*, e i vuoti vanno dichiarati. Quando la strategia ha bisogno di qualcosa che nel corpus non c'è, la skill lo segna come "da verificare fuori corpus" e si ferma: la verifica esterna e lo stress test avvengono dopo, con altre skill (`ricerca-giurisprudenziale-aggiornata`, `avvocato-del-diavolo-small`).

Il perimetro chiuso riguarda le **fonti giuridiche**, non i **fatti della causa**. I fatti (testo della clausola, atto d'acquisto, note di trascrizione, contratto di locazione, foro) sono materiale della parte e la strategia senza di essi resta generica: si raccolgono al gate, come descritto più avanti.

## Come si entra: un solo comando

L'utente non deve ricordare una sintassi. Basta la parola `corpus`, o il nome della skill.

**Ogni volta che la skill viene invocata, la prima cosa che fa è questa, sempre, senza eccezioni:**

1. legge `lavoro/stato-lavorazione.md` (se manca, siamo all'inizio);
2. dice in due righe a che punto è la lavorazione e qual è la fase successiva;
3. chiede conferma e si ferma.

Non esegue nulla prima della conferma. Se lo stato manca del tutto, la fase proposta è l'avvio (fase 1). Se l'utente ha già confermato nel messaggio stesso ("corpus, vai con le schede"), esegue quella fase e poi si ferma.

Le fasi si eseguono una per volta. Non concatenare mai due fasi, neppure se l'utente scrive "vai avanti fino alla fine": in quel caso spiega che i punti di arresto servono a correggere il tiro (quesito, raggruppamenti, schede, mappa) prima che l'errore si propaghi, e chiedi quale fase eseguire. L'unico arresto interno a una fase che la 1.2 elimina è quello tra i lotti di schede: dentro la fase 2 si va fino in fondo, salvo anomalie.

I file di `lavoro/` sono leggibili dall'utente in ogni momento: `inventario.md`, `sinossi.md`, ogni scheda, `mappa-orientamenti.md` e `strategia.md` sono passaggi intermedi da rivedere, non scatole nere. Se l'utente corregge un file intermedio, la fase successiva parte dalla sua versione.

## Comandi

| Comando | Effetto |
|---|---|
| `corpus` | Legge lo stato, dice dove si è, propone la fase successiva, si ferma |
| `corpus avvia [cartella dei pdf]` | Crea la struttura, raccoglie i file, estrae i testi, fase 1 |
| `corpus stato` | Come `corpus`, ma senza proporre nulla |
| `corpus schede tutte` | Fase 2 completa, tutti i lotti in parallelo, senza arresti intermedi (è il comportamento predefinito della fase 2) |
| `corpus schede S11-S20` | Fase 2 limitata a un intervallo di ID (utile per spezzare la fase su due sessioni) |
| `corpus rifai S07` | Rifà o completa una singola scheda |

Tutto il resto si dice a parole. Se l'utente descrive l'obiettivo in linguaggio naturale, individua la fase corrispondente dallo stato di lavorazione, proponila e aspetta; non saltare fasi.

## Dove stanno i file

La skill è pensata per **Cowork con una cartella di pratica sul disco**. È l'unico ambiente in cui la continuità tra sessioni funziona, perché `lavoro/` e `stato-lavorazione.md` restano su disco tra una conversazione e l'altra.

**Un Progetto non va bene e non va proposto come alternativa.** Un Progetto conserva istruzioni e knowledge, non il filesystem: ogni conversazione riparte da un container vuoto e i file intermedi si perdono. Inoltre le sentenze caricate come knowledge di progetto vengono recuperate per estratti, non lette integralmente: questo viola la regola 1 e produrrebbe citazioni di passaggi mai letti per intero. Se l'utente propone questa strada, spiegaglielo e riportalo alla cartella.

In chat (claude.ai) i file caricati stanno in `/mnt/user-data/uploads/` e il filesystem si azzera tra una conversazione e l'altra: la skill può lavorare solo entro una sessione. Con 20–30 sentenze la sessione non basta. Dillo subito e proponi Cowork; per corpus fino a 5–6 sentenze la chat regge, ma il lavoro non è ripristinabile.

## Sessioni: quando spezzare

Una sessione unica su 30 sentenze arriva a fine lavoro con il contesto compattato e la parte iniziale della conversazione non più consultabile. Punti di taglio consigliati, da proporre all'utente all'inizio della fase 1:

- **Due sessioni** (consigliato, con le schede in parallelo): sessione A = fase 1 + fase 2; sessione B = fase 3a, 3b, gate, 4, 5.
- **Tre sessioni** se il corpus supera le 40 sentenze o le schede vengono fatte in sequenza: A = fase 1 + schede S01–S(n/2); B = schede restanti; C = dal 3a alla fine.

Per riprendere: nuova conversazione Cowork sulla stessa cartella, parola `corpus`, conferma della fase proposta. Tutto ciò che serve alla ripresa deve stare in `stato-lavorazione.md`; quello che non è scritto lì è perduto.

## Regole inderogabili

1. Usa soltanto il testo delle sentenze presenti in `lavoro/testi/`. Non citare norme, massime, precedenti o dottrina che non compaiano in quel testo. Se una norma è citata dal giudice, la si riporta come citazione del giudice, non come conoscenza propria.
2. Ogni affermazione sul contenuto di una sentenza porta un riferimento nel formato rigido `(Sxx, p. N, «primi 10-15 parole del passaggio»)`. Se il testo non ha paginazione, si omette la pagina ma non le caporali né l'ID. Il formato vale **dalle schede in poi**, non solo nel report: parafrasi tra virgolette alte, citazioni "prima il testo poi il riferimento", o riferimenti senza caporali sfuggono allo script di controllo e si scoprono solo in fase 5, quando costano di più. L'incipit deve essere letterale: serve al controllo automatico.
3. Gli ID li assegna lo script, non il modello. Sono scritti in `lavoro/mappa-id.tsv` e coincidono con il nome dei file in `lavoro/testi/` (`S01.txt`, `S02.txt` …). Non rinominarli, non riassegnarli, non inventarne di nuovi.
4. Distingui sempre fatti rilevanti, domanda, decisione, ratio decidendi, argomenti concorrenti, obiter e precedenti richiamati. Non attribuire a una sentenza un principio che non sia ricavabile dal suo testo; non uniformare decisioni diverse per comodità espositiva.
5. Ogni punto di ogni scheda porta un livello di certezza: *espresso* (il giudice lo dice), *inferito* (si ricava dal ragionamento), *incerto* (il testo lo consente ma non lo impone).
6. Ogni argomento della fase strategica porta un'etichetta di fondamento: `[attestato]` (una sentenza del corpus lo dice), `[costruito]` (ricavato per estensione, distinzione o contraddizione da sentenze del corpus, con indicazione di quali), `[da verificare fuori corpus]` (richiede fonti che nel corpus non ci sono; la skill lo formula come ipotesi e non lo sviluppa).
7. Se un file è illeggibile, incompleto o privo del passaggio necessario, dichiaralo nell'inventario e nella scheda. Non si riempie con quello che "probabilmente" dice.
8. Quando individui un contrasto, verifica se è reale o se dipende da differenze di fattispecie, disciplina applicabile, domanda, eccezioni, prova, rito o tempo. Un contrasto apparente vale quanto uno reale, ma va chiamato con il suo nome.
9. La posizione difesa non si chiede e non si assume prima che la mappa sia chiusa. Se l'utente la dichiara spontaneamente all'inizio, prendine nota in `stato-lavorazione.md` come "posizione dichiarata anticipatamente" e non usarla fino al gate. Il *quesito* e la *provenienza del corpus* non sono la posizione difesa: quelli si chiedono subito.
10. **I nomi dei file non sono informazioni.** Un'annotazione nel nome ("++ importante", il nome della pratica, un asterisco) segnala al più che l'utente ha giudicato quella sentenza rilevante. Non dedurne mai che la sentenza riguardi la causa dell'utente, che l'utente ne sia parte, che penda un termine di impugnazione o altro. Se il dubbio è reale, si fa una domanda secca e si prosegue; non si aprono "urgenze", non si calcolano termini, non si cambia l'ordine del lavoro. La skill non calcola scadenze: è fuori perimetro.
11. Nulla di ciò che accade nella conversazione (deviazioni, correzioni, falsi allarmi, malfunzionamenti di hook) entra nel report. Il report descrive il corpus e la strategia, non la lavorazione.
12. Terminologia tecnico-giuridica italiana; prosa nel report finale (vedi `references/struttura-report.md`).

## Struttura della cartella di lavoro

```
<cartella pratica>/
├── input/sentenze/            ← i file forniti dall'utente (PDF, docx, txt, md)
├── lavoro/
│   ├── testi/S01.txt … S30.txt   ← testo estratto con marcatori di pagina [[p.N]]
│   ├── mappa-id.tsv           ← ID → file, formato, pagine, stato (lo scrive lo script)
│   ├── inventario.md
│   ├── sinossi.md             ← una riga per sentenza, alimentata dalla fase 2
│   ├── schede/S01.md … S30.md
│   ├── note-lavorazione.md    ← osservazioni di merito emerse durante le schede (v. fase 2)
│   ├── scheda-fatti.md        ← fatti e documenti della causa, raccolti al gate
│   ├── mappa-orientamenti.md  ← mappa neutra (bozza di lavoro)
│   ├── strategia.md           ← bozza di lavoro dopo il gate
│   └── stato-lavorazione.md   ← breve: stato, non diario
└── REPORT-orientamenti-<tema>.md   ← unico deliverable
```

Tutto ciò che sta in `lavoro/` è strumentale: serve alla continuità tra sessioni e al controllo, non va consegnato. Il deliverable è un solo file.

## Fase 1 — Avvio e inventario

Esegui `python3 scripts/prepara_corpus.py <cartella pratica>`. Lo script:

- crea `input/sentenze/` e `lavoro/testi/` se non esistono;
- raccoglie in `input/sentenze/` i file di sentenza che trova al primo livello della cartella di pratica (così l'utente può limitarsi a buttare i PDF in una cartella qualsiasi); con `--da <cartella>` li prende invece da lì; con `--no-raccogli` non sposta niente;
- verifica le dipendenze di estrazione e dice in chiaro che cosa manca, invece di fallire un file alla volta;
- assegna gli ID in ordine alfabetico di nome file, **conservando quelli già assegnati** se `mappa-id.tsv` esiste (i file aggiunti dopo prendono ID successivi, nessuno slitta);
- converte ogni file in `lavoro/testi/Sxx.txt`, con marcatori `[[p.N]]` per i PDF nativi, senza marcatori per docx/txt/md;
- scrive `lavoro/mappa-id.tsv` con ID, file, formato, pagine, caratteri, stato, anteprima.

Se un PDF risulta privo di testo (scansione), segnalalo e chiedi all'utente se vuole l'OCR o preferisce sostituire il file; non procedere a OCR di propria iniziativa su trenta file.

Poi chiedi all'utente tre cose, prima di leggere il merito:

- **il quesito**, anche provvisorio. Serve subito: l'inventario raggruppa per tema e le schede, quando una sentenza decide più questioni, devono sapere quale seguire. Registralo in `stato-lavorazione.md` come "quesito provvisorio", dichiaratamente rivedibile in fase 3. Se l'utente non sa ancora formularlo, fanne tu una versione dall'inventario e chiedi conferma.
- **come è stato formato il corpus**: ricerca su banca dati (con quale query), sentenze citate dalla controparte, materiale del cliente, raccolta mista. Non è la posizione difesa e non tocca il gate, ma è l'unico dato che permette di dire nel report quanto pesa la fotografia. Il criterio di selezione è il bias più forte del metodo e va dichiarato.
- **in quante sessioni vuole lavorare** (v. "Sessioni: quando spezzare"). Registra la scelta nello stato.

Infine, leggendo solo l'apertura e la chiusura di ciascun testo (intestazione, dispositivo), compila `lavoro/inventario.md`: una riga per sentenza con l'ID assegnato dallo script, organo e sezione, data e numero, grado, esito, nome del file originale, stato del testo, e un'ipotesi di raggruppamento tematico rispetto al quesito provvisorio. Segnala duplicati (stessa sentenza in due file, o stessa decisione in gradi diversi). Non sintetizzare ancora il merito: l'inventario serve a sapere con che cosa si lavora, e a decidere se il corpus è quello giusto prima di investire trenta schede.

Chiudi la fase dicendo quante sentenze sono lavorabili, quali problemi ci sono, quali raggruppamenti hai ipotizzato. Aspetta conferma prima delle schede.

## Fase 2 — Schede

Una scheda per sentenza, nel formato di `references/scheda-sentenza.md`. Il testo integrale di una sentenza si legge solo per fare la sua scheda, mai tutte insieme.

**Esecuzione in parallelo (predefinita).** Dividi gli ID in lotti di 5–8 e affida ogni lotto a un subagente (strumento Agent, tipo general-purpose), tutti lanciati nello stesso turno. Ogni subagente riceve nel prompt: la cartella pratica; gli ID del suo lotto; il quesito provvisorio; l'istruzione di leggere per intero `references/scheda-sentenza.md` e poi, un ID per volta, `lavoro/testi/Sxx.txt`; le regole 1, 2, 4, 5, 7, 10 di questa skill riportate testualmente; il tetto di lunghezza (una scheda sta tra 5 e 9 KB: oltre, si sta riassumendo la sentenza invece di schedarla); l'obbligo di scrivere `lavoro/schede/Sxx.md`, di **non** toccare `sinossi.md` né `stato-lavorazione.md`, e di restituire al termine, come proprio messaggio finale, le righe di sinossi dei suoi ID e un elenco di anomalie (file fuori tema, incompleto, sentenza collegata a un'altra del corpus, tensione interna rilevante). Dai al subagente solo ciò che gli serve: non la conversazione, non le altre schede.

La sessione principale, ricevuti i risultati: scrive `lavoro/sinossi.md` in ordine di ID; scrive le anomalie e le osservazioni di merito in `lavoro/note-lavorazione.md` (non nello stato); esegue `python3 scripts/verifica_citazioni.py <cartella> lavoro/schede/*.md` e fa rifare (`corpus rifai Sxx`, anche via subagente) le schede con scarti; aggiorna `stato-lavorazione.md` con la sola riga "Completate: …". Il controllo citazioni sulle schede è la novità che evita di scoprire in fase 5 gli incipit non letterali.

**Nessun arresto tra i lotti.** Ci si ferma dentro la fase 2 solo se: un testo risulta illeggibile o troncato; una sentenza appare fuori tema o duplicata; un subagente non ha restituito una scheda. In quei casi si chiede all'utente e si riprende. Se l'utente preferisce l'esecuzione sequenziale nella sessione principale (corpus piccolo, o vuole leggere le schede man mano), lo dice: allora si lavora a lotti di cinque, si aggiorna lo stato a fine lotto, ma senza chiedere conferma tra un lotto e l'altro.

Due parti della scheda meritano attenzione speciale perché sono quelle che la fase 4 userà di più:

- la sezione **F, limiti applicativi**: presupposti, fatti ostativi, onere della prova, profili temporali e di rito, elementi che potrebbero distinguere il precedente. È il materiale del distinguishing.
- la sezione **H, tensioni interne**: punti in cui la motivazione dice una cosa e ne applica un'altra, in cui il principio enunciato è più largo o più stretto della regola applicata, in cui un argomento accessorio contraddice la ratio dichiarata. Queste tensioni non sono contrasti tra sentenze: stanno dentro una sola motivazione, e sono spesso il fronte d'attacco migliore. Se non ce ne sono, scrivilo.

Chiudi la fase con: numero di schede, esito dello script, anomalie, e la proposta di passare alla 3a (o di chiudere la sessione, se era previsto il taglio qui).

## Fase 3 — Mappa neutra

Presuppone tutte le schede. Riprendi il quesito provvisorio fissato in fase 1: se alla luce delle schede va corretto, riformulalo e chiedi conferma prima di procedere, perché una mappa su un quesito sbagliato è inutile. Registra la versione definitiva in `stato-lavorazione.md`.

Lavora in due tempi, per non caricare tutto insieme:

- **3a, raggruppamento.** Leggi solo `lavoro/sinossi.md` e `lavoro/note-lavorazione.md` e forma i raggruppamenti per tesi. Mostrali all'utente in forma di elenco (ID per gruppo, regola in una frase) e fermati se chiede correzioni.
- **3b, mappa.** Un gruppo per volta, aprendo solo le schede di quel gruppo, e chiudendo la sezione di quel gruppo prima di aprire il successivo. **Non aprire tutte le schede in un turno solo**: trenta schede sono 400 KB e saturano il contesto prima della strategia. Se i gruppi sono più di quattro, affida a un subagente per gruppo la stesura della sezione "Le tesi" di quel gruppo (input: le schede del gruppo, i testi per la rilettura, il formato rigido dei riferimenti) e riserva alla sessione principale le sezioni trasversali (2–7 sotto). Per ogni passaggio che citi rileggi il punto nel testo originale in `lavoro/testi/` (cerca l'incipit): la scheda è una mediazione, la citazione va sull'originale.

Scrivi `lavoro/mappa-orientamenti.md` con questo contenuto, in questo ordine:

1. **Le tesi.** Per ciascun orientamento: regola di diritto in una frase; sentenze aderenti; ricostruzione fattispecie → questione → norma → interpretazione → presupposto → conclusione → effetto; ratio decisiva; onere della prova; limiti. Le sentenze che non aderiscono chiaramente a nessuna tesi vanno in una categoria propria, non forzate.
2. **Le ragioni sotto le tesi.** Che cosa muove davvero ciascun orientamento: un'esigenza sistematica, una lettura testuale, una preoccupazione di effetti pratici, un precedente ritenuto vincolante. È qui che si capisce se due tesi sono conciliabili.
3. **Contrasti.** Reali; apparenti (e da che cosa dipendono: fatti, rito, domanda, prova, disciplina intertemporale); mutamenti nel tempo; tensioni interne alle singole motivazioni raccolte dalle sezioni H.
4. **Punti di incontro.** Ciò su cui tutte le tesi concordano, anche implicitamente. Sono i punti che nessuna strategia può contestare.
5. **Spazi di conferma e confutazione.** Per ogni tesi: quali elementi del corpus la rafforzerebbero se ripresi, quali la indeboliscono, quali fattispecie non ha mai affrontato.
6. **Persuasività nel corpus.** Forza argomentativa, ampiezza e omogeneità dei precedenti, coerenza sistematica, vulnerabilità di ciascuna tesi. Non dichiarare una tesi "prevalente" o "vincente": descrivi i pesi e lascia il giudizio.
7. **Vuoti del corpus.** Fattispecie non coperte, gradi o organi assenti, salti temporali, questioni decise senza motivazione sufficiente. Punti che richiederebbero verifica esterna. Qui va richiamato anche il criterio di formazione del corpus registrato in fase 1.

Chiusa la stesura, esegui `python3 scripts/verifica_citazioni.py <cartella> lavoro/mappa-orientamenti.md` e correggi gli scarti sull'originale prima di dichiarare la mappa chiusa. Poi dillo esplicitamente e proponi il gate.

## Gate — Posizione e fatti

Chiedi all'utente, in una sola volta e con domande chiuse dove possibile:

1. quale parte assiste; quale risultato vuole ottenere (domanda o eccezione); in quale grado e rito;
2. **il foro** (Tribunale o Corte d'Appello) davanti a cui si va: è obbligatorio, perché decide quale giurisprudenza di merito del corpus è "locale" e quale è solo persuasiva. Se l'utente non risponde, si richiede una seconda volta prima di procedere;
3. **i fatti che la mappa ha indicato come discriminanti tra le tesi** — la skill li elenca esplicitamente, uno per uno, ricavandoli dalla mappa (per esempio: testo esatto della clausola; come il regolamento è richiamato nell'atto d'acquisto; se e quando è stato trascritto; se il convenuto è proprietario o conduttore; titolarità di tutte le unità) — e chiede all'utente di rispondere per ciascuno oppure di indicare i documenti della cartella pratica da cui ricavarli (atto d'acquisto, regolamento, note di trascrizione, contratto di locazione, visure). Quei documenti si leggono: sono fatti della causa, non fonti giuridiche, e non violano il perimetro chiuso. Ciò che l'utente non sa e non documenta resta "fatto non accertato" e la strategia lo tratta in alternativa.

Registra tutto in `lavoro/scheda-fatti.md` (fatti accertati, con il documento da cui provengono; fatti non accertati) e il riassunto in `stato-lavorazione.md`. Da questo momento la mappa non si modifica più: se la strategia rivela un errore nella mappa, si annota come "correzione post-gate" con motivazione, per lasciare traccia del fatto che è avvenuta dopo la dichiarazione della posizione.

## Fase 4 — Strategia

Scrivi `lavoro/strategia.md`. Per la posizione dichiarata e i fatti della scheda-fatti:

- **Tesi difensive.** Quali orientamenti del corpus sostengono la posizione, con quale forza, e a quali condizioni di fatto. Per ciascuna: come si argomenta, quali sentenze si citano, quali limiti (sezione F) vanno neutralizzati perché la controparte li userà per distinguere. Il precedente-guida va scelto tenendo conto del foro: una sentenza di merito di un'altra Corte non è un pilastro davanti a un Tribunale di un distretto diverso, e va presentata come persuasiva, con una pronuncia di legittimità a fianco quando il corpus la offre.
- **Fronti d'attacco.** Come si aggrediscono gli orientamenti contrari: distinguishing sulle fattispecie; sfruttamento delle tensioni interne (sezione H); riduzione della portata del principio alla regola effettivamente applicata; contrasti apparenti da far valere come tali e contrasti reali da far pesare; argomenti che una sentenza contraria concede incidentalmente e che possono essere ripresi.
- **Argomenti nuovi.** Costruzioni non attestate in nessuna sentenza ma ricavabili dal corpus: estensione di una ratio a una fattispecie non decisa, combinazione di due orientamenti, rovesciamento di un distinguishing. Vanno etichettati `[costruito]` con l'indicazione delle sentenze da cui derivano e della mossa logica compiuta. Un "argomento costruito" è una proposizione che si può scrivere in un atto: un avvertimento ("non usare la tesi X") o una ripetizione della tesi principale non lo sono e stanno altrove.
- **Da verificare fuori corpus.** L'elenco di ciò che servirebbe e non c'è: un precedente di legittimità sul punto, l'evoluzione normativa, una norma citata dal giudice il cui testo vigente non è nel corpus. Formulato come domanda di ricerca, pronto per `ricerca-giurisprudenziale-aggiornata`.
- **Ordine di attacco proposto.** Quale argomento va per primo e perché, quale tenere di riserva, quale non usare pur essendo disponibile.

Ogni argomento porta l'etichetta di fondamento. Non è un'omissione se un argomento resta `[da verificare fuori corpus]`: è la skill che fa il suo mestiere.

## Fase 5 — Report unico

Prima di scrivere, esegui `python3 scripts/verifica_citazioni.py <cartella pratica> lavoro/mappa-orientamenti.md lavoro/strategia.md`. Se le fasi 2 e 3b hanno fatto il loro controllo, qui gli scarti dovrebbero essere pochi. Correggi ogni riferimento non trovato rileggendo l'originale (lo script indica il passaggio più vicino, se ne trova uno); se il passaggio non esiste, l'affermazione che vi si appoggia va tolta o riformulata come inferenza. Non scrivere il report finché lo script non passa pulito o finché ogni scarto non è spiegato.

Poi scrivi `REPORT-orientamenti-<tema>.md` seguendo `references/struttura-report.md`. È l'unico deliverable: prosa argomentativa continua, senza elenchi puntati e senza tabelle nel corpo, con i riferimenti tra parentesi nel testo. Le schede non si allegano. Il report non racconta la lavorazione (regola 11). Se nella cartella esiste `stile-scrittura-legale.md` o un file di stile dello studio, leggilo e applicalo; altrimenti valgono le regole del riferimento.

Rilancia lo script sul report finito: le citazioni possono cambiare in riscrittura.

Chiudi la fase con tre cose:

1. l'offerta di esportare il report in `.docx` (skill `docx` o `legal-it:esporta-documento`), perché il deliverable finisce in un atto e il markdown è un formato di passaggio;
2. il rinvio a `ricerca-giurisprudenziale-aggiornata` per i punti "da verificare fuori corpus";
3. il rinvio ad `avvocato-del-diavolo-small` per lo stress test della strategia, passandole il report.

## Continuità tra sessioni

`stato-lavorazione.md` (modello in `references/stato-lavorazione.md`) registra fase corrente, quesito provvisorio e definitivo, provenienza del corpus, piano delle sessioni, ID delle schede completate, posizione (dopo il gate), correzioni post-gate, esito dell'ultimo controllo citazioni, problemi aperti. **È uno stato, non un diario**: deve stare in una pagina. Le osservazioni di merito emerse durante le schede (contrasti scoperti, collegamenti tra sentenze, dubbi di pertinenza) vanno in `lavoro/note-lavorazione.md`, che la fase 3a legge; nello stato resta al più una riga di rinvio. L'intestazione "Fase corrente" si aggiorna a ogni chiusura di fase: uno stato che dice "fase 4 in corso" quando la 5 è conclusa fa ripartire male la sessione successiva.

All'inizio di ogni sessione leggilo prima di qualsiasi altra cosa; alla fine di ogni comando aggiornalo. Non rileggere schede o testi già lavorati se non servono al comando in corso.

## Ambiente e modello

- Se è attivo un hook di controllo citazioni di altri plugin (per esempio `citation-gate` del plugin legal-it), può segnalare come "non verificate" norme che compaiono solo perché citate dal giudice, o riferimenti fantasma di turni precedenti. Non si chiama `cite_law()` per soddisfarlo: le norme sono riportate come citazioni del giudice (regola 1). Si risponde con una riga e si va avanti; se scatta ripetutamente sullo stesso falso positivo, si consiglia all'utente di disattivare l'hook per la durata della lavorazione.
- Il collo di bottiglia non è il modello ma il contesto: le schede in parallelo e la mappa per gruppi contano più della scelta del modello. Se si vuole comunque differenziare: modello veloce per i subagenti delle schede (lavoro strutturato su un template), modello più capace per 3b, 4 e 5, dove contano sintesi e precisione delle citazioni.
