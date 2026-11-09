# OKF in 10 Minuten verstehen

Ein Beispiel-Repo, das zeigt, was das **Open Knowledge Format (OKF)** ist und warum es KI-Assistenten hilft, bei Firmenwissen richtig zu antworten. Keine Vorkenntnisse nötig. Wenn du einen Ordner und eine Textdatei kennst, reicht das.

Das Beispiel ist eine erfundene Fahrradwerkstatt. Sie hat ein Wiki, in dem drei Seiten erklären, was ein „Auftrag" ist – alle drei anders. Du siehst, wie daraus *eine* Definition wird, die ein KI-Assistent lesen kann.

---

## 1. Das Problem in 60 Sekunden

Stell dir vor, du fragst einen KI-Assistenten, der das Firmen-Wiki kennt:

> „Was ist bei uns ein Auftrag?"

Im Wiki stehen drei Seiten dazu. Eine sagt, ein Auftrag beginnt mit dem Kostenvoranschlag. Eine sagt, er beginnt, wenn das Rad in der Werkstatt steht. Die dritte ist von 2023 und sagt, Aufträge werden auf Papier geführt.

Der Assistent nimmt die Textschnipsel, die deiner Frage am *ähnlichsten* klingen, mischt sie zusammen und antwortet flüssig. Die Antwort klingt überzeugend. Sie ist falsch, oder halb richtig, und niemand merkt es.

Das ist kein Fehler des Assistenten. Er hatte nie eine Chance: Nirgends im Wiki steht, welche der drei Seiten gilt.

## 2. Die Idee: ein Glossar neben dem Archiv

Ein neuer Mitarbeiter bekommt am ersten Tag zwei Dinge:

| Das Glossar | Das Archiv |
| --- | --- |
| Zehn Begriffe, kurz erklärt, vom Chef abgenommen | Das ganze Wiki, alle alten Seiten, alle E-Mails |
| „So nennen wir Dinge. Punkt." | „Irgendwo da drin steht es." |
| Klein, stimmt immer | Riesig, stimmt meistens ungefähr |

Niemand käme auf die Idee, nur das Archiv zu geben. Genau das passiert aber, wenn man einem KI-Assistenten nur das Wiki gibt.

**OKF ist das Glossar.** Ein Ordner mit kurzen Textdateien, eine pro Begriff, mit ein paar Zusatzinfos oben drin: Woher kommt die Definition? Wer hat sie geprüft? Bis wann gilt sie?

Das Archiv (das Wiki, die Dokumente) bleibt, wo es ist. Der Assistent liest zuerst das Glossar und erst dann das Archiv.

## 3. So sieht eine OKF-Datei aus

Das ist `okf/begriffe/auftrag.md` aus diesem Repo:

```markdown
---
type: concept
title: Auftrag
description: Eine vom Kunden freigegebene Reparatur mit Nummer, Termin und Preisrahmen
sources:
  - resource: wiki-vorher/Auftragsabwicklung.md
    title: Wiki-Seite Auftragsabwicklung
verified:
  - { by: "human:werkstattleitung", at: 2026-11-09 }
stale_after: 2027-05-09
---

Ein Auftrag ist eine Reparatur, die der Kunde nach dem
[Kostenvoranschlag](kostenvoranschlag.md) freigegeben hat. Er bekommt eine
Nummer, einen [Werkstatt-Termin](werkstatt-termin.md) und einen Preisrahmen.
Nicht gemeint: eine Anfrage am Telefon oder ein Rad, das nur zur Durchsicht
dasteht. Erst die Freigabe macht daraus einen Auftrag.
```

Drei Teile:

1. **Der Kopf** zwischen den `---` Linien. Das sind Metadaten: Was ist das, woher kommt es, wer hat es geprüft, wann läuft es ab. Ein Programm kann das lesen.
2. **Die Definition.** Erster Satz sagt, was es ist. Drei bis fünf Sätze, nicht mehr.
3. **Die Abgrenzung.** Ein Satz, was es *nicht* ist. Das ist oft der wichtigste Satz, weil genau da die Verwechslungen passieren.

Die eckigen Klammern sind Links auf andere Begriffe. So entsteht ein Netz: Ein Assistent, der „Auftrag" liest, findet von dort aus „Kostenvoranschlag" und „Werkstatt-Termin".

## 4. Probier es aus (5 Minuten)

Du brauchst nur einen KI-Chat (ChatGPT, Claude, Gemini, egal welcher).

**Schritt 1: Ohne OKF.** Kopiere den Inhalt der drei Dateien aus `wiki-vorher/` in den Chat und frag:

> „Was ist ein Auftrag? Antworte in einem Satz."

Schau dir die Antwort an. Vermutlich vermischt sie die Seiten oder nimmt die falsche.

**Schritt 2: Mit OKF.** Neuer Chat. Kopiere jetzt zusätzlich `okf/begriffe/auftrag.md` hinein und sag dazu:

> „Die Datei auftrag.md ist die geprüfte Definition. Was ist ein Auftrag? Antworte in einem Satz."

Jetzt kommt die richtige Antwort, und zwar jedes Mal.

**Schritt 3: Die Falle.** Frag im zweiten Chat:

> „Ist ein Rad, das zur Durchsicht dasteht, ein Auftrag?"

Ohne die Abgrenzung im letzten Satz der Datei würde der Assistent hier raten. Mit ihr sagt er Nein.

Das ist der ganze Trick. Nicht mehr Text, sondern *eine* geprüfte Version pro Begriff.

## 5. Mach dein eigenes Konzept

Nimm einen Begriff aus deinem Alltag, deiner Schule, deinem Verein, deiner Firma, bei dem Leute aneinander vorbeireden. „Hausaufgabe", „Training", „Sprint", „Ticket", „fertig".

1. Kopiere `okf/begriffe/_vorlage.md` und benenne sie um, zum Beispiel `ticket.md`.
2. Fülle den Kopf aus. `type: concept` kannst du lassen. Bei `sources` schreibst du, woher deine Definition kommt (eine Wiki-Seite, ein Handbuch, „Gespräch mit Chef am 9.11.").
3. Schreib die Definition. Erster Satz: Was ist es. Dann zwei bis vier Sätze mehr.
4. Schreib den Satz „Nicht gemeint: …". Denk an die Fälle, wo Leute sich streiten.
5. Setz einen Link auf einen anderen Begriff, falls es einen gibt.
6. Lass jemanden draufschauen, der sich auskennt. Wenn die Person sagt „ja, stimmt", trägt sie sich in `verified` ein. Vorher bleibt das Feld leer.
7. Trag den Begriff in `okf/begriffe/index.md` ein, damit man ihn findet.

Prüfen, ob alles stimmt:

```
python scripts/pruefen.py
```

Das Skript sagt dir, wenn ein Feld fehlt, ein Link ins Leere zeigt oder ein Begriff nicht im Index steht.

## 6. Wann gehört ein Begriff ins OKF?

Nicht jeder. Zwei Fragen, beide mit Ja:

- Braucht der Assistent den Begriff bei fast jeder Frage?
- Richtet eine falsche Antwort Schaden an?

„Auftrag" in einer Werkstatt: ja und ja. „Farbe der Werkstatt-Shirts": nein und nein, das bleibt im Wiki.

Die Falle ist, zu viel reinzuschreiben. Dann wird das OKF das zweite Wiki, das keiner pflegt. Zehn richtige Begriffe sind mehr wert als fünfzig halbe.

## 7. Was die Felder im Kopf bedeuten

| Feld | Was es sagt | Pflicht? |
| --- | --- | --- |
| `type` | Was für eine Datei das ist: `concept` (Begriff), `rule` (Regel), `index` (Inhaltsverzeichnis) | Ja, laut Spezifikation das einzige Pflichtfeld |
| `title` | Der Name des Begriffs | Empfohlen |
| `description` | Ein Satz, der auch im Index steht | Empfohlen |
| `sources` | Woher die Definition kommt | Empfohlen |
| `verified` | Wer hat geprüft, dass es stimmt, und wann. `human:` davor heißt: ein Mensch, kein Programm | Empfohlen |
| `stale_after` | Datum, ab dem jemand nochmal draufschauen sollte | Empfohlen |
| `status` | `active` oder `draft` (noch nicht geprüft) | Optional |

Warum das wichtig ist: Ein Wiki weiß nicht, ob eine Seite noch stimmt. Eine OKF-Datei trägt das Datum, ab dem sie alt ist, selbst mit sich. Ein kleines Skript kann jeden Morgen nachsehen, welche Dateien abgelaufen sind, und jemandem Bescheid sagen.

## 8. Für Entwickler: Wie ein Assistent das benutzt

Zwei Wege, und in der Praxis beide:

**Direkt lesen.** Vor der eigentlichen Suche prüft der Assistent, ob die Frage einen Begriff aus `okf/begriffe/index.md` trifft. Treffer: Datei lesen, als geprüfte Quelle in den Kontext geben. Das ist deterministisch, gleiche Frage, gleiche Definition.

**Ingestieren.** Die OKF-Dateien kommen zusätzlich in den normalen Such-Index (RAG, Vektordatenbank, was auch immer). Saubere, kurze Markdown-Dateien ergeben bessere Chunks als Wiki-Exporte, und die Kopf-Felder (`verified`, `stale_after`) landen als Metadaten am Chunk. Damit kann man geprüfte Treffer beim Suchen höher gewichten.

Warum beide: Nur direkt lesen verpasst Fragen, in denen der Begriff nicht wörtlich vorkommt. Nur ingestieren lässt die Definition gegen zehntausend andere Chunks antreten, und die alte Wiki-Seite kann gewinnen, weil sie der Frage ähnlicher klingt.

OKF ersetzt die Suche nicht. Es ist die Schicht für die Handvoll Dinge, die der Assistent sicher wissen muss.

## 9. Was in diesem Repo liegt

```
wiki-vorher/           drei Wiki-Seiten, wie man sie in jeder Firma findet
okf/
  index.md             Einstieg
  begriffe/
    index.md           alle Begriffe, ein Satz pro Zeile
    _vorlage.md        zum Kopieren
    auftrag.md
    kostenvoranschlag.md
    werkstatt-termin.md
  regeln/
    index.md
    abholung.md        eine Regel statt eines Begriffs
  log.md               wer hat wann was geändert
scripts/
  pruefen.py           prüft, ob alle Dateien vollständig sind
```

## 10. Weiterlesen

- Die Spezifikation von Google Cloud: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- OKF und RAG, wie sie zusammenpassen: https://geotoolbox.ai/blog/okf-vs-rag

Dieses Repo ist ein Lernbeispiel. Die Fahrradwerkstatt ist erfunden. Nimm alles, ändere alles, keine Bedingungen (siehe `LICENSE`).
