# Modello di scheda analitica — `lavoro/schede/Sxx.md`

Compilare ogni voce. Ogni punto delle sezioni B–H porta il livello di certezza tra parentesi quadre: `[espresso]`, `[inferito]`, `[incerto]`. Ogni punto delle sezioni C–H porta il riferimento `(p. N, «incipit letterale»)`; se il testo non è paginato, solo l'incipit. Nessuna informazione esterna al testo.

```markdown
# Sxx — <organo, sez., n./data>

## A. Identificazione
- File:
- Organo, sezione:
- Data e numero:
- Grado e rito:
- Esito (accoglimento/rigetto/cassazione con o senza rinvio/altro):
- Stato del testo: completo / incompleto (dove) / illeggibile (dove)

## B. Fatti giuridicamente rilevanti
Massimo 10 punti. Solo fatti che incidono sulla decisione.
1. … [espresso] (p. N, «…»)

## C. Domande, eccezioni, questioni
- Domanda/e:
- Eccezioni:
- Questione/i di diritto effettivamente decisa/e (distinguere da quelle solo enunciate):

## D. Norme e precedenti richiamati
| Norma / precedente | Funzione nel ragionamento (fondante / di supporto / distinta / citata e disattesa) | Riferimento |
|---|---|---|

## E. Principio e ratio decidendi
- Principio in una frase:
- Sillogismo:
  1. premessa normativa:
  2. qualificazione dei fatti:
  3. regola applicata:
  4. conclusione:
- Necessario alla decisione vs accessorio/obiter (elencare separatamente):

## F. Limiti applicativi
- Presupposti di applicazione:
- Fatti ostativi:
- Onere della prova (chi, che cosa, come assolto o no):
- Profili temporali, procedurali, di competenza:
- Elementi che potrebbero distinguere il precedente:

## G. Citazioni di controllo
I 3–6 passaggi essenziali, in forma breve, con pagina e incipit. Sono quelli che la mappa e il report citeranno.

## H. Tensioni interne alla motivazione
- Principio enunciato più ampio/stretto della regola applicata:
- Argomenti accessori che contraddicono la ratio:
- Fatti qualificati in modo non coerente con la premessa:
- Concessioni incidentali utili alla tesi opposta:
Se assenti: "Nessuna tensione rilevata" (non lasciare vuoto).

## I. Prima collocazione (provvisoria)
Orientamento a cui la sentenza sembra aderire, o "non riconducibile". Da rivedere in fase 3.
```

## La riga di sinossi

Chiusa ogni scheda, aggiungere una riga a `lavoro/sinossi.md`. È il file su cui lavora la fase 3a: deve stare su una riga e bastare a sé per raggruppare, senza riaprire la scheda.

Formato, con il separatore ` · ` tra i campi:

```
Sxx · <organo, sez.> · <n./data> · <grado> · <esito in una parola> · <principio in una frase> · <collocazione provvisoria> · <tensione interna: sì/no>
```

Esempio della forma attesa (i contenuti sono fittizi, servono solo a mostrare la lunghezza dei campi):

```
S07 · Trib. Catania, sez. IV · 1234/2024 · primo grado · rigetto · <regola di diritto in una frase, non più di venticinque parole> · orientamento B · tensione: sì
```

## Avvertenze

- La sezione E chiede il sillogismo "ricostruito": se il giudice non lo esplicita, i passaggi ricostruiti sono `[inferito]`, mai `[espresso]`.
- La sezione H è quella che si tende a saltare. Prima di scrivere "nessuna tensione", rileggere la parte finale della motivazione confrontandola con il principio enunciato all'inizio.
- Se la sentenza decide più questioni, la scheda segue quella pertinente al quesito registrato in `stato-lavorazione.md` e menziona le altre in C senza svilupparle. Se il quesito provvisorio non copre bene la sentenza, non forzarla: annotarlo, perché è un segnale che il quesito va corretto in fase 3.
