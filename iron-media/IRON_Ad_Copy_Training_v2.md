# IRON Ad-Copy Training v2

Internes Trainingsdokument für Claude · IRON Meta Ads (Seb / Heik) · Stand 08.10.2026

**Vor jeder neuen Ad komplett lesen.** v2 enthält alles Wichtige aus v1 (Feedback-Runden zu 1.2, 1.3, 2.2, 3.1–3.3, 4.1, 4.2, 5.3, 7.2) und ergänzt die Runden zu **2.3** und **4.3**. Zitate von Heik sind leicht von Tippfehlern bereinigt.

---

## 0. Kurz gesagt

Eine Ad hat **einen Angle** und erzählt ihn in einem durchgehenden Gedankengang: Hook → Situation → (Zugeständnis) → Reframe → Lösung → Proof → CTA. Jede Zeile hängt an der vorigen. Jede Behauptung kommt von Seb, aus den Calls, von den CSMs oder aus Heiks Training. Der Hook ist voll mit Wörtern, die nur der ICP versteht, weil Meta die Ad nach den Wörtern ausspielt. Iron kommt erst im Proof, der Pitch ist kurz, den Rest macht die VSL. **250 bis 270 Wörter**, mit `wc -w` gezählt, ein Code-Block, Zeile – Leerzeile – Zeile.

Die 10 Regeln, die ich am häufigsten breche:

1. **Erst den Angle in einem Satz bestätigen lassen, dann schreiben.** Bei 4.3 habe ich zwei komplette Versionen auf einem Glauben gebaut, den die Leads gar nicht haben.
2. **Glauben und Wörter in den Calls nachzählen**, bevor ich sie benutze. Wie viele Leads sagen das wirklich, und mit welchen Worten?
3. **Andromeda: Der Hook muss ICP-Lingo tragen.** Keine Alltagsmetaphern (Laden, Filiale), sonst zeigt Meta die Ad den falschen Leuten.
4. **Klarheit vor Insider-Slang.** Wörter wie "abgegrast" oder "oberste Stufe" erst erklären oder ganz weglassen.
5. **Format = die fertigen Ads im Ad-Scripts-Doc**, nicht die Seb-Transkripte. Transkripte liefern Inhalt und Phrasen, nie das Format.
6. **Eine Idee pro Ad.** Was nicht zum Angle gehört, fliegt raus, auch wenn es stimmt.
7. **Kein KI-Ton:** keine Sinnsprüche, kein Copywriter-Deutsch ("Kaufmodus", "Q1 gewinnst du im Q4"), kein Pathos.
8. **Nichts erfinden.** Abgeleitetes selbst markieren, für Unbekanntes Platzhalter setzen.
9. **Heiks Zeilen wörtlich übernehmen.** Bei Rohentwürfen nur Tippfehler fixen und Lücken in Seb's Worten füllen.
10. **Bei "ist das gut?" nur ein kurzes Urteil plus gezielte Zeilen-Fixes geben.** Nicht die ganze Ad umbauen.

---

## 1. Projekt-Fakten

**Kunde:** Iron Media GmbH, Sebastian "Seb" Szalinski. Closer ist Edis Bajrami ("Eddy"), dazu kommen die CSMs (Account Manager). Ad Copywriter ist Heik.

**ICP:** D2C-Ecom-Brands mit eigenem Produkt und **100 bis 500k Monatsumsatz**, Ziel ist **1 Mio+ im Monat** ("von 7 auf 8 stellig").
- Meist problemlösende Produkte (Health, Body, Haushalt, viele Supplements), Team von solo bis 9 Leuten.
- Meta ist der Hauptkanal, oft machen sie es selbst oder mit einer Agentur oder Freelancern.
- Kennen Seb's YouTube-Content, haben oft schon Kurse gekauft (Ecom House, Dropshipping-Coaching, Skool).
- Budget ist da, Liquidität oft knapp. Q4 ist der Haupthebel.

**Iron-Modell:**
- **Hauptsächlich Done-with-you (DWY), DFY nur manchmal.** Iron sagt genau, was zu tun ist, und schaut bei jedem Schritt drüber.
- Feste Ansprechpartner: Customer Success Manager 1:1, Weekly Call, Slack, Loom-Feedback, Roadmap nach 1, 3, 6 und 12 Monaten.
- Ein kleines Inhouse-Team ist Teil des Modells, Iron hilft mit einem Pool beim Recruiting.
- **Expansion und Internationalisierung sind positiv** (siehe NoMisk). Nie schlechtreden, nur in die richtige Reihenfolge bringen ("erst ab X Umsatz").
- Iron nie wie eine Agentur framen.

**CTA-Ziel:** Jede Ad führt auf die **VSL-Landingpage**, die VSL erklärt den Rest bis zur Callbuchung. In der Ad steht also kein "Call buchen" und keine Leistungsliste.

**Das Offer (Heik, 5.1):** "Wir bringen deine Brand in den nächsten 3 Monaten auf 8 stellig." Wenn ein CTA das Offer zeigen soll, dann dieses Outcome, nicht die Leistungen (Messages, VSL Ads, Funnels). Außerhalb von AG6 nur angedeutet ("dort zeig ich dir, wie wir mit dir…"). In AG6 kommt es direkt.

**Mechanismus-Name:** "Funnel First System" oder "Ugly Funnel System", je nachdem was passt. Innerhalb einer Ad bleibt es ein Name.

**Proof:**
- Belegte Marken: IM8 von David Beckham (von Tag 1), More Nutrition, ESN, Kinobody, The Oodie, Corbo, Ljubav, außerdem Financial Times und Statista ("schnellstwachsender Ecom Growth Partner Europas").
- Unbestätigte Zahlen sind Platzhalter: `[CASE: Brand] von X auf X`, "über X Marken" (Seb sagt 500+, Edis 740+), "30 Brands dieses Jahr auf 8 stellig".
- Heik hat aktuell kein Proof-Sheet, also immer Platzhalter setzen.
- Proof muss zum Mechanismus der Ad passen. Seb's "über 1 Mio Profit an einem einzigen Tag" kam aus einem VIP-Sale an Bestandskunden und passt deshalb nicht zu einem Cold-Traffic-Angle.

**Quellen in diesem Projekt:** 17 Sales Calls (Edis), 3 CSM-Calls (hea-rs, Serotalin, Swiss Tallow), Kern-ICP und ICP-Dossier v2, Pre-Call-FAQ-Skripte, aktuelle VSL, 4 alte Winner und 17 neu gefilmte Seb-Ads, rund 17 YouTube-Videos und Podcasts von Seb, Heiks Meta-Ads-Training sowie die PM- und Ecom-MBA-Skripte als Stilreferenz.

---

## 2. Kampagne & Stand der Ad Groups

Heiks System: 1 CBO, 1 Broad-Adset, 5–8 Ads (Post-IDs), jede Ad hat einen Job in der Purchase Journey, 3 Creatives pro Ad (Flexible) = 3 verschiedene Angles für denselben Job. **Creatives derselben Ad Group dürfen sich nicht gleich anhören.** Sie werden in derselben Post-ID gegeneinander ausgespielt.

| AG | Job | Creatives (Stand 08.10.) |
|---|---|---|
| 1 Problem | Status quo | 1.1 gefilmt · 1.2 fertig · 1.3 im alten Chat in Arbeit (Status bei Heik prüfen) |
| 2 Q4 Opportunity | Reason why now | 2.1 gefilmt · 2.2 fertig · **2.3 fast fertig** (siehe §8) |
| 3 Mechanism | Mechanismus etablieren | 3.1 gefilmt (Purple Ocean) · 3.2 fertig (Tafel) · 3.3 fertig |
| 4 Reframe | Falschen Glauben brechen | 4.1 fertig · 4.2 fertig · **4.3 fertig** (siehe §9) |
| 5 Gegen die Szene | Common Advice/Beliefs, nicht konkrete Firmen | **5.1 fertig** (Creative Volume, siehe §9b) · 5.2 gefilmt · 5.3 fertig |
| 6 Straight Offer | Zusammenarbeit direkt pitchen | 6.1 gefilmt (Main Stage) · 6.2 gefilmt (Voller Kalender) · 6.3 offen |
| 7 Case Studies | Proof | 7.1 gefilmt · 7.2 fertig (Straight Flex) · 7.3 offen |
| 8 Objection Handling | Einwände | 8.1 · 8.2 · 8.3 **Entwurf** (Keine Zeit · Klappt's bei uns? · Individuell oder Kurs?), Logik aus den Pre Call FAQ Videos |

**AG8 Objection Handling (Heik, 8.1):** Die Ads behandeln Einwände gegen das **Skalieren an sich** ("ich hab nicht genug Zeit, um auf 8 stellig zu gehen", "dafür muss ich viele neue Leute einstellen"), **nicht** Einwände gegen Iron als Produkt. Also keine Roadmap/CSM/Feedback-Abläufe als Antwort, sondern Seb's Reframe zum Glauben (YT 07: Founder im "Managing Modus", Zeit in Sachen, "die die Nadel nicht bewegen", lean Teams; YT 10: 8 stellig mit Founder + 1 Google Mitarbeiter + 2–3 Creative Freelancern; YT 02: "lean Killer Teams von unter 10 Leuten, die achtstellig sind"). Iron und der Mechanismus kommen erst als Lösung bzw. Proof.

**Reihenfolge der offenen Creatives:** AG8 Feedback → 6.3 → 7.3 → 8.1 → 8.2 → 8.3. 1.3 vorher klären.

### Schon benutzt, also nicht wiederholen

**Hook-Typen:**
- 1.2: "Der mit Abstand häufigste Grund…"
- 1.3: "Meistens sind es so 2, 3 winning ads…", die Lage chronologisch erzählt
- 2.2: "Q4 macht die einen… reich… und die anderen broke…"
- 2.3: "Jeder in der Ecom Szene weiß, dass Q4…"
- 3.3: "Real talk… Jeder in der Ecom Szene labert…"
- 4.1: Zitat-Hook mit dem Glauben der Brands
- 4.2: "Hör auf, neue Ads zu launchen… Nein, jetzt mal ohne Spaß…"
- 4.3: "Ich finds so funny wie so viele Ecom Brands denken, dass sie: '…'"
- 5.3: "Jeder in der Ecom Szene will dir… verkaufen"
- 5.1: Frage-Hook mit Zahl: "Wie viele Creatives brauchst du WIRKLICH pro Woche, um von 300k auf 1 Million im Monat zu kommen?"
- 7.2: Selbst-Flex
- Gesperrt: **"Jeder in der Ecom Szene…" ist dreimal benutzt.**

**Freie Hook-Typen:** "Hart gesagt…" (Seb's alter Winner), "Was dir keine Agentur sagt…", der Plan als Szene ("Jeden Monat eine neue Sorte… dann…"), Call-out mit Rückgang ("schon mal 300k, jetzt 150"), Zahlen-Paradox.

**CTAs:**
- 1.2: "schau dir an, wie wir mit Ugly Funnels genau das bei deiner Brand umsetzen können"
- 1.3: "schau dir an, wie wir dir so ein System aufbauen können"
- 2.2: "check ab, wie wir bei Iron dir dabei helfen können"
- 2.3: "da siehst du, wie wir das mit dir noch vor Black Friday aufbauen"
- 3.3: "check ab, wie wir das bei deiner Brand aufsetzen würden"
- 4.1: "schau dir an, wie wir deine Creative Strategy und deinen Funnel aufbauen würden"
- 4.2: "check ab, wie wir das bei Iron mit dir umsetzen würden"
- 4.3: "dort erklär ich dir, wie wir mit dir erst mal den Rest vom DACH Raum holen"
- 5.1: "Klick mal auf die Ad hier und ich zeig dir genau wie wir dir dabei helfen werden" (**fast wie 7.2**)
- 5.3: "check das Video ab, was ich gedreht habe…"
- 7.2: "ich zeig dir genau, wie wir dir dabei helfen und wie eine Zusammenarbeit mit uns aussieht"

**Qualifier:**
- 2.2: "wenn du deine Brand dieses Q4 von 7 auf 8 stellig skalieren willst…"
- 2.3: "wenn du dein Ecom Brand in Q4 von 7 auf 8 stellig skalieren willst…" (**fast identisch mit 2.2, gleiche Ad Group, offen**)
- 4.1: "bevor du den nächsten Media Buyer einstellst…"
- 4.2: "wenn du von 7 auf 8 stellig willst, ohne jede Woche 300 neue Ads rauszuhauen…"
- 4.3: "bevor du das nächste Produkt launchst oder in ein neues Land gehst…"
- 5.1: "falls du deine Ecom Brand von 7 auf 8 stellig skalieren willst… Ohne hunderte neue Ads immer ins Leere zu launchen…" (**gleicher Aufbau wie 4.2**)

**Authority- und Case-Zeilen:**
- 1.2: "…in meiner Firma Iron, die by the way allein dieses Jahr schon 30 Marken auf 8 stellig…"
- 2.2: "Genau das machen wir in meiner Firma Iron Media den ganzen Tag" plus 3 Rapid-Fire-Cases
- 2.3 und 4.3: "Genau so ist/haben wir [CASE] in meiner Firma Iron…", **zweimal derselbe Aufbau, nächste Ads anders**
- 4.2: über 500 Marken, IM8 von Tag 1, FT/Statista
- 5.1: "Wir haben mit meiner Firma Iron allein dieses Jahr schon 30 Brands von 7 auf 8 stellig gebracht…" mitten in der Ad als Beweis gegen den Glauben, unten nur kurz "So haben wir [CASE]… mit X Ads die Woche"
- 5.3: "Und das sag ich dir nicht einfach so…"
- 7.2: Case-Salve
- Noch frei: ~~"Woher ich das weiß?"~~ (Heik, 3.2: **keine Fragen** als Authority-Zeile, lieber "Und das weiß ich so genau, weil…"), die Marken-Liste (More Nutrition, ESN…), "Ich weiß, das klingt großkotzig… ist aber die Realität".

**Seb's Funnel-Seiten (aus YT, nicht nur Advertorial und Listicle):** "Jede Awareness Stufe braucht die richtige Page." Kalt: Longform Page oder Advertorial, die aufklärt. Für mehr Scale ein Listicle davor. Mitte: Vergleichsseite, auch fürs Retargeting. Warm: Shortform Offer Page, die Einwände killt. Am Ende eine Checkout Page mit Upsells und Downsells, dazu Quiz Funnels und Presell Pages. Name in Ads: lieber **"Ugly Funnels"** (Heik, 8.2).

**Mechanismus-Formulierungen (nicht wörtlich wiederholen):**
- 2.2: "Vorne VSL Ads statt nur ein paar UGCs… dahinter ein fettes Listicle oder Advertorial… Cold Traffic Offer, das schon vorne über 100 € AOV holt… Upsells und Downsells…"
- 2.3: "VSL Ads, die auch kalten Leuten in 3 bis 5 Minuten erklären… Listicle oder Advertorial statt der Produktseite… sieht hässlich aus, konvertiert aber wie Sau… Cold Traffic Offer mit über 100 € AOV schon bei der ersten Bestellung"
- 4.3: "VSL Ads, die erst mal über das Problem reden… Advertorial statt der Produktseite… Cold Traffic Offer, das auch für jemanden Sinn macht, der dich heute zum ersten Mal sieht"
- 5.3: "5 Minuten Video Ad, 10 Minuten Advertorial, 5 Minuten Einwandbehandlung, Checkout…"

---

## 3. Bauplan einer Ad

1. **Hook (1–2 Zeilen):** Direkt rein, mit ICP-Lingo (Ecom Brand, 100 bis 500k im Monat, 7 auf 8 stellig, DACH Raum, Meta, CPA, Bundle…) und dem Glauben oder Problem. Polarisierend, aber wahr. Keine Annahme über den Zuschauer. Ein "Wenn…"-Call-out ist okay, "dann machst du höchstwahrscheinlich X" nicht.
2. **Situation:** In den Worten der Leads und chronologisch, so wie sie es erleben.
3. **Zugeständnis (stark):** "Klar hast du vielleicht schon…", "Klar kann das reichen…", "Versteh mich nicht falsch… machen wir auch… aber erst ab X".
4. **Reframe:** Was eigentlich stimmt, mit einer Brücke ("Aber…", "Dabei…", "Weil…").
5. **Lösung:** Klein machen ("einfach", "eigentlich ziemlich simpel"), dann konkret in Seb's Worten: VSL Ads mit 3 bis 5 Minuten, Advertorial oder Listicle statt Produktseite, Cold Traffic Offer über 100 € AOV, Upsells und Downsells. Danach eine "Heißt…"-Zeile mit dem nüchternen Warum.
6. **Proof:** Iron frühestens hier, oder beiläufig ("die by the way…"). Die Case-Zeile beantwortet am besten direkt den Glauben aus dem Hook (4.3: "nur im DACH Raum und ohne ein einziges neues Produkt").
7. **CTA:** Ein Qualifier, der den Hook spiegelt ("Also… bevor du / wenn du…"), dann ein direkter Klick ("Klick auf die Ad… da siehst du / dort erklär ich dir, wie wir mit dir…"). Jedes Mal anders.

**Je nach Ad Group:**
- **Opportunity-Ads (AG2) brauchen Stakes.** Was passiert, wenn man nicht handelt? Das muss zum Nutzen des Mechanismus führen. In 2.3 kann die Konkurrenz mehr spenden; der Payoff dreht das um: "auf einmal bist du derjenige, der mehr auf seine Ads spenden kann".
- **Reframe-Ads (AG4) dürfen den Glauben nicht verteufeln, wenn Iron das selbst macht.** Stattdessen die Reihenfolge oder eine Schwelle setzen ("machen wir auch, aber erst ab X Umsatz").
- **Lieber Chancen-Framing als Problem-Framing:** "du kannst auch einfach… damit öffnet sich ein extrem großer Markt" statt "du nimmst das Problem mit".

---

## 4. Format & Lieferung

- **Ein Code-Block, Zeile – eine Leerzeile – Zeile.** Nie zwei Leerzeilen, auch wenn der `.txt`-Export der Doc so aussieht.
- **"…" am Zeilenende**, wenn der Gedanke weitergeht, und mitten in der Zeile als Sprechpause.
- **Keine Filming Ideas, Alt-Hooks, Regie-Kommentare oder Titel im Block**, außer Heik will sie.
- Zahlen als Ziffern, Fachbegriffe ohne Bindestrich ("Direct Response Funnel", "8 stellig", "KI Videos").
- **Nach dem Block kurz bleiben:** was sich geändert hat, woher es kommt, was abgeleitet ist und was offen ist. Kein Roman.
- **Länge 250–270 Wörter, vorher mit `wc -w` zählen.** Wenn Heik Zeilen hinzufügt, gleiche ich in meinen Teilen aus. Wird es trotzdem zu lang, schlage ich vor, welche seiner Zeilen redundant ist, ändere sie aber nicht selbst.

---

## 5. Sprache, Voice & Andromeda

**Seb-Voice:** "halt", "einfach", "eigentlich ziemlich simpel", "ehrlich gesagt", "So, hier ist das Ding…", "Heißt,…", "by the way", "ballern", "konvertiert wie Sau", "scheiß egal", "Woher ich das weiß?", "Ich weiß, das klingt großkotzig… ist aber die Realität", dazu Selbstironie.

**Status-Attitüde hat Heik in 4.3 selbst gesetzt:** "Ich finds so funny…" und "100 bis 500k Monatsumsatz sind baby numbers…". Das ist dieselbe Haltung wie bei Seb's "Rookie Numbers" im alten Winner. So entsteht Intrigue: mit Haltung und Status, nicht mit Bildern oder Witzen.

**Andromeda (aus Heiks Training):** Meta liest jedes Wort und zeigt die Ad den Leuten, zu denen die Wörter passen.
- Darum steht im Hook nur, was nur der ICP versteht: Ecom Brand, Monatsumsatz, 7 auf 8 stellig, DACH Raum, Meta, CPA, Creatives, Winner, Bundle, Sorte, Produktseite, VSL Ad, Advertorial.
- **Verboten sind Alltagsmetaphern** ("Laden in der Innenstadt", "Filiale", "Schaufenster") und branchenfremde Beispiele (Wasserfilter). Heik dazu: "das komplett quatsch… Meta nimmt die Ad und packt es in front of wer auch immer dazu relaten wird".

**Was nicht nach Seb klingt:**

| Ich habe geschrieben | Heik | Besser |
|---|---|---|
| "Der komplette Markt ist im Kaufmodus", "zücken die Kreditkarte", "Q1 gewinnst du im Q4" | "terrible lingo" | Szenen in Seb's Worten: "hauen ihr Weihnachtsgeld raus", "fertig ist der Black Friday" |
| Fließtext-Absätze wie in den YT-Transkripten | "bro was hast du getan" | Das Format der Doc-Ads |
| "alles abgegrast" (dreimal) | "ich weiß gar nicht, was du meinst, ich brauch viel mehr clarity" | Klartext: "Leute, die zwar dein Produkt brauchen, aber noch nicht aktiv danach suchen" |
| "Immer wenn wir mit Ecom Brands reden, wollen fast alle als Nächstes dasselbe…" | "zu langweilig" | Glauben als Zitat mit Attitüde: "Ich finds so funny wie so viele Ecom Brands denken, dass sie: '…'" |
| "…der teuerste Fehler, den du machen kannst" (gegen Expansion) | baut es selbst um | "geil, machen wir auch… aber erst ab X Umsatz" |
| "Ganz ehrlich… das Volumen war nie das Problem" | "klingt super AI" (4.2) | Szene: "Und ich so… ey, du kannst auch 1.000 Ads launchen." |

**Nuance zu "nicht X, sondern Y":** Verboten ist es als KI-Sinnspruch. Als schlichte Aussage des Angles behält Heik es ("nicht nur deren Zielgruppe… sondern einfach der komplette Markt"). Szenen-Zeilen wie "Produktbild, Preis und Warenkorb Button… und ist direkt wieder weg" dürfen ähnlich wie in anderen Ads klingen. Niemals wiederholen darf ich Hook-Typ, CTA und Authority-Zeile.

---

## 6. Den Glauben und die Wörter in den Calls prüfen

**Vorgehen:** Lead-Zeilen nach Schlüsselwörtern durchsuchen (grep). Dann pro Brand zählen, mit welchen exakten Worten und in welchem Segment (Rückgang, Stagnation, schnell wachsend) sie das sagen. Heik fragt das jedes Mal ("reden die echt so?").

**Ergebnisse bisher:**

| Wort / Glaube | Wer sagt es wirklich | Folgerung |
|---|---|---|
| "gläserne Decke" | **niemand** (steht nur im FAQ-Skript) | nicht benutzen |
| "Decke" | 2 von 17: Marcus ("an der Decke gekommen bei Meta"), Caro ("eine Decke erreicht") | nur als Nebenzeile |
| "Plateau / stagnieren / steht man an" | Caro, Marcus, Jakob | für Stagnation okay |
| "Zielgruppe durch" | wörtlich nur Caro | trägt keinen Hook |
| "abgegrast" | Isabella (Zitat ihres Media Buyers) | unklar, nicht benutzen |
| Rückgang ("war schon mal mehr") | 7 von 10 ICP: Tom, Isabella, Kacper, Jakob… | stärkste Situation, aber Schluss = Winner/System/Inhouse |
| neue Produkte als nächster Schritt | Isabella (jeden Monat neue Sorte), Tom (Smart Wallet "in der Hoffnung"), Kacper (Relaunch), Caro (Menopause), Selurewear (Katalog) | passt zu 4.3 |
| neue Länder/Märkte | Caro (Internationalisierung, Frankreich), Sanja ("neuer Markt"), FreeSoul, Aloa | passt zu 4.3 |

**Wichtig:** Situation und Glaube müssen aus demselben Segment kommen. Brands mit Rückgang schließen auf neue Winner, ein System oder Inhouse. Expansion denken vor allem Brands, die stagnieren oder schnell wachsen. Einen Call-out mit Rückgang und einen Expansions-Glauben nicht in einer Ad mischen.

---

## 7. Heiks Arbeitsweise und Umgang mit Feedback

- **Heik schreibt oft selbst einen Rohentwurf** mit Tippfehlern und Platzhaltern wie "blabla", "case study", "CTA". Meine Aufgabe:
  - seine Zeilen wörtlich übernehmen, nur Tippfehler fixen
  - die Lücken in Seb's Worten füllen
  - Flow und Länge sichern
  - danach die ganze Ad liefern
- **Bei "mach weiter" setze ich genau an seiner letzten Zeile an**, mit einer Brücke, und bleibe in seiner Logik.
- **Bei "ist das gut?"** gebe ich ein kurzes Urteil und maximal 3–4 konkrete Fixes mit dem genauen Zeilentext. Kein Komplettumbau. Er unterbricht, wenn ich zu viel mache.
- **Bei einer Flow-Frage zwischen zwei Zeilen** beantworte ich die unausgesprochene Frage dazwischen (z. B. "wo geht der Besucher hin?") und achte auf die Grammatik der Folgezeile (Singular/Plural). Am besten biete ich 2 Varianten an.
- **Flags nenne ich einmal.** Wenn er sie behält, ist das entschieden (z. B. Hook-Typ-Wiederholung, englische Wörter, eine Zeile mit Annahme). Nicht erneut ansprechen.
- **Bei Angle-Unklarheit** (z. B. durchgestrichener Titel) biete ich erst 2–3 Angle-Optionen mit Belegen aus den Calls an, er wählt, dann schreibe ich.
- **"Kein People-Pleasing":** objektiv bleiben, aber nicht jedes Mal neu bauen. Wenn ich nach seinem Feedback eine Version komplett neu mache, nimmt er oft lieber die vorige als Basis (siehe 2.3, V5).

---

**Brain Dump ≠ Copy (Heik, 8.1):** Wenn Heik Stichpunkte in Kleinschreibung mit Tippfehlern schickt ("die denken die haben keine zeit… logistik blablabla… kein system"), ist das die **Gliederung**, nicht der Text. Dann die Logik übernehmen und in Seb's Voice neu formulieren, mit Flow von Zeile zu Zeile. 1:1 übernehmen nur seine ausformulierten Ad-Zeilen (mit "…", Großschreibung, ganzen Sätzen). Und **1 Main Idee pro Ad**: kein Sammeln von Seb-Zitaten, nur was den einen Gedanken trägt.

**Edit-Durchgang (Heik, 1.2): Flow ist Priorität Nummer 1.** Kürzen heißt: echte Wiederholungen und doppelte Erklärungen raus. Gesprochene Verbindungsstücke bleiben drin ("Das Problem ist…", "Klar kann das reichen…", "Und so weiter.", "by the way"). Die Ad muss laut ausgesprochen geil klingen. Lieber 250 Wörter mit Flow als 210 abgehackte. Und beim Kürzen den Inhalt nicht verschieben: Das Problem in 1.2 ist "alles nur auf die Produktseite schicken", nicht "die Produktseite".

**"…" vs. Punkt (Heik, 1.2):** Wenn die nächste Zeile denselben Satz oder dieselbe Idee weiterführt, endet die Zeile mit "…", nicht mit einem Punkt. Beispiel: "da kaufen halt nur die Leute, die eh schon wissen, dass sie dein Produkt wollen…" / "Und von denen gibt's halt nur eine begrenzte Anzahl." Ein Punkt nur, wenn danach ein neuer Gedanke anfängt.

**Ein Gedanke nicht über viele Zeilen ziehen (Heik, 1.3):** Der Hook-Gedanke ("2, 3 Winner → brennen aus → kopieren → jede Version schlechter → keiner weiß warum") stand auf 5 Zeilen. Das wirkt langgezogen. Ein Gedanke bekommt eine Zeile, höchstens 2. Die "…"-Regel heißt nicht, einen Satz in viele Zeilen zu zerlegen. Sie gilt, wenn eine Zeile einen neuen Schritt bringt und der Gedanke trotzdem weiterläuft.

**Sprechbar schreiben (Heik hat 1.3 laut gelesen und ist gestolpert):** Stolperfallen sind ein Personenwechsel mitten im Block (wir → du), Passiv ("wird weitergebaut"), Zahlen dicht hintereinander ("2, 3 Ads… 3, 4 Angles"), "z.B." (liest sich laut schlecht), "?…" nach Fragen und Aufzählungen mit 4 Punkten. Lösung: eine Person pro Block, aktiv, höchstens 3 parallele Punkte, Zahlen nicht stapeln, "also" statt "z.B.".

**Kongruenz im Mechanismus (Heik, 1.3):** Nicht 2 Konzepte nebeneinanderstellen, die nicht auseinander folgen ("Winner weiterbauen mit neuen Hooks" und "mehrere Angles/Gründe"). Ein Begriff zieht sich als Kette durch: Grund des Winners finden → auf diesem Grund neue Ads bauen (neue Hooks, Bilder, Creators) → nächsten Grund finden → jeder Grund bekommt seinen Funnel. Fachwörter wie "Angle" durch das ersetzen, was sie meinen ("Grund, warum Leute kaufen"), und mit einem Beispiel belegen.

**Zeilenanfänge variieren (Heik, 2.3):** Nicht mehrere Zeilen hintereinander mit "Und" anfangen ("und und und"). Und auch nicht dasselbe Wort in 2 aufeinanderfolgenden Zeilen ("vorbereitet sind… / vorbereitest"). Beim Edit die ersten Wörter jeder Zeile untereinander lesen.

**"Kürzer" heißt nicht Telegrammstil (Heik, 5.3):** Wenn Heik "kürzer" sagt, fliegt Inhalt raus (ein Punkt der Aufzählung, eine doppelte Info), aber die Verbindungswörter bleiben: "Weil die Leute da…", "und erst dann…", "Und so… auf einmal". Abgehackt: "Erst 5 Minuten Video Ad… dann 10 Minuten Advertorial… dann Checkout." Richtig: "Weil die Leute da erst 5 Minuten deine Video Ad schauen… dann 10 Minuten das Advertorial lesen… und erst dann im Checkout landen."

## 8. Case Study 2.3 "Im Q4 kauft der ganze Markt" (AG2)

| V | Was ich gemacht habe | Heiks Reaktion | Lektion |
|---|---|---|---|
| 1 | kurze Zeilen mit "…", aber Copywriter-Deutsch ("Kaufmodus", "zücken die Kreditkarte", "Q1 gewinnst du im Q4"), ca. 330 Wörter, plus Filming Idea, 2 Alt-Hooks und ein langer Begründungsblock | "terrible lingo… mimick wie Seb redet, unsere jetzigen Ads, die Länge auch" | Lingo und Länge wie die Doc-Ads, keine Zusatz-Romane |
| 2 | Fließtext-Absätze wie die YT-Transkripte, 2 Min plus Kurzversion, Makkaroni-Witz | "Code-Format… bro was hast du getan… schau, wie lang unsere Ads sind, die Paragraphs, die '...'" | **"Unsere Ads" sind die Doc-Skripte.** Überkorrektur |
| 3 | Code-Block im Doc-Format, aber 2 Leerzeilen | "ich will 1" | genau 1 Leerzeile |
| 4 | wie V3 mit 1 Leerzeile | (danach kam Training v1) | Heik nahm später genau diese Szenen-Zeilen als Basis |
| 5 | nach Training v1 komplett neu, strikt nach Regeln (neuer Hook, Reframe "Dabei…", "Woher ich das weiß?"), 269 Wörter | ignoriert, schreibt eigene Version auf Basis von V4 | Regeln nicht überdehnen: gute Szenen nicht killen, nur weil sie 1.2 oder 2.2 ähneln |
| 6 | seine Zeilen 1:1, fortgesetzt ab "schleunigst…": 3 Sachen, Payoff-Flip, Case, CTA, 269 Wörter, 3 Flags | übernimmt fast alles, ändert Hook-Flow und CTA auf "von 7 auf 8 stellig", behält alle Flags | Weiterschreiben in seiner Logik trifft. CTA lieber mit Wachstumsframe als "mehr als nur Stammkunden" |
| 7 | "ist das gut?" → ich fing an, alles umzubauen | unterbricht, fragt nur nach dem Flow zwischen 2 Zeilen | gezielt antworten |
| 8 | 2 Brücken-Varianten mit "die Brands" im Plural, damit "…können als du" passt | Entscheidung offen | Flow-Fix = Zwischenschritt + Grammatik |

**Seine Logik für 2.3 (Vorlage für Opportunity-Ads):** Opportunity (Q4 beste Zeit, der ganze Markt kauft) → Paradox (die meisten sind nicht vorbereitet) → Lücke (Setup nur für Warme: "UGCs… Produktseite… 20 % Rabatt drauf und fertig ist der Black Friday") → Stakes (die Konkurrenz spendet mehr und nimmt dich auseinander) → Fix (3 Sachen in Seb's Worten) → Payoff, der die Stakes umdreht → Case → CTA.

**Stand 2.3:** seine letzte Version mit 291 Wörtern plus Brücke. Offen:
1. Brücke Variante 1 ("Und kauft dann bei den Brands, die genau auf diese Leute vorbereitet sind… / Und wenn du dich jetzt nicht schnell darauf vorbereitest, nehmen die dich im Q4 absolut auseinander…") oder Variante 2
2. Länge (mit Brücke ca. 300 Wörter, Vorschlag: "Das holt halt die paar Leute ab…" streichen)
3. Der Qualifier ist fast identisch mit 2.2
4. Grammatik: "Was sie halt nicht checken, [ist,] dass…", "deine Ecom Brand", "im Q4"

---

## 9. Case Study 4.3 "Neues Produkt/Expansion → Mehr Bewusstseinsstufen treffen" (AG4)

| V | Was ich gemacht habe | Heiks Reaktion | Lektion |
|---|---|---|---|
| 1 | Den Titel habe ich als "ohne Expansion" gelesen und mir einen eigenen Glauben genommen: "Media Buyer sagt, ihr habt alles abgegrast". "Abgegrast" stand dreimal drin | "dieses abgegrast… weiß gar nicht, was du meinst, ich brauch viel mehr clarity" | Lead-Slang ist nicht automatisch klar. Bei unklarem Titel erst den Angle bestätigen |
| 2 | "abgegrast" raus, dafür ein Wasserfilter-Beispiel (Kästen schleppen) | "ne ich mag den Ansatz nicht" | erfundenes Beispiel aus einer fremden Branche; richtig war, danach 3 Angle-Optionen anzubieten |
| – | 3 Optionen (Zielgruppe durch / Produkt erklärt sich selbst / CPA steigt) | wählt 1: "dann sei aber auch upfront" | den Glauben direkt in den Hook |
| 3 | Upfront-Hook "denken, sie sind mit ihrer Zielgruppe durch… dabei nur ein kleines Stück erreicht" | "mehr Intrigue, Sebastian Style, nicht crazy fun" | Intrigue ist Haltung, nicht nur Aussage |
| 4 | Hook mit 10 % und "Und das Witzige ist…" | "reden die echt von Zielgruppe? Oder von mehr Produkten, expandieren, andere Länder als DACH?" | **Ich hatte Option 1 als "die meisten Belege" verkauft, dabei war es nur Caro.** Vorher zählen |
| 5 | Neu auf "neues Produkt / neues Land": "Immer wenn wir mit Ecom Brands reden, wollen fast alle als Nächstes dasselbe…" | "zu langweilig" | beschreibender Einstieg = langweilig |
| 6 | Metaphern-Hook "Laden in der Innenstadt… zweite Filiale… Schaufenster" | "komplett quatsch… Meta packt es in front of wer dazu relatet… wir brauchen Lingo, das nur unser ICP checkt" | **Andromeda-Regel verletzt** (steht in seinem eigenen Training) |
| 7 | ICP-Lingo-Hook "an der Decke bei Meta… teuerster Fehler" | "reden viele Prospects von gläserner Decke?" | nein, "Decke" sagen nur 2 von 17. Jede Hook-Phrase nachzählen |
| – | 5 Alternativen für die ersten 4 Zeilen | zu Option 1 (Rückgang): "ist das deren Schlussfolgerung, zu expandieren?" | nein, Rückgang führt zu Winner, System oder Inhouse. Segmente nicht mischen |
| 8 | – | **Heik schreibt den Hook selbst:** "Ich finds so funny wie so viele Ecom Brands denken, dass sie: 'Neue Produkte launchen oder in andere Länder expandieren müssen…' … das machen wir auch… aber erst ab X Umsatz… 100 bis 500k sind baby numbers… nicht mal ansatzweise den ganzen DACH Raum abgedeckt" | Vorlage für Reframe-Hooks: Glauben als Zitat + Seb-Attitüde + Status ("baby numbers") + Iron-konforme Schwelle |
| 9 | meine Fortsetzung mit "Weil…", "Heißt, wenn du jetzt… verkaufst du da auch wieder nur an die…" | schreibt den Rest selbst als Skelett: "Klar hast du vielleicht schon viele angesprochen… aber du kannst auch einfach andere Bewusstseinsstufen… Leute targeten, die zwar dein Produkt brauchen, aber noch nicht aktiv danach suchen… extrem großer weiterer Markt, ohne was Neues zu launchen… Funnel System mit VSL Ads blabla / case study / CTA" | Zugeständnis plus Chancen-Framing schlägt mein Problem-Framing. Der Fachbegriff fällt direkt, mit Klartext-Erklärung dahinter |
| 10 | Skelett gefüllt: Mechanismus, "Heißt, du verdienst auf einmal an Leuten, die bisher an jeder deiner Ads vorbeigescrollt sind", Case "nur im DACH Raum und ohne ein einziges neues Produkt", Qualifier und CTA rund um DACH | **übernommen**, er hat nur die Zeilen 2 und 3 zusammengezogen | fertig |

**Finale 4.3 (266 Wörter):**

```
Ich finds so funny wie so viele Ecom Brands denken, dass sie:

“Neue Produkte launchen oder in andere länder expandieren müssen, um von 7 auf 8-stellig zu gehen”.

Versteh mich nicht falsch… neue Produkte und Länder sind geil, das machen wir mit unseren Brands auch, wie z.B. X Y und Z.

Aber das machen wir erst ab X Umsatz…

100 bis 500k Monatsumsatz sind baby numbers…

Damit hast du nicht mal Ansatzweise den ganzen Dach Raum und deine Zielgruppe abgedeckt.

Klar hast du vielleicht schon viele angesprochen, die gerade in dem Moment auf der Suche nach deinem Produkt sind…

Aber du kannst auch einfach versuchen, andere Bewusstseinsstufen anzusprechen.

Leute targeten, die zwar dein Produkt brauchen, aber noch nicht aktiv danach suchen.

Damit öffnet sich ein extrem großer weiterer Markt für dich, ohne was Neues zu launchen…

Und dafür brauchst du einfach ein Funnel System… mit VSL Ads, die erst mal über das Problem reden, das dein Produkt löst.

Dahinter statt der Produktseite ein Advertorial, das erklärt, warum genau dein Produkt dieses Problem löst…

Und ein Cold Traffic Offer, das auch für jemanden Sinn macht, der dich heute zum ersten Mal sieht.

Heißt, du verdienst auf einmal an Leuten, die bisher an jeder deiner Ads vorbeigescrollt sind.

Genau so haben wir in meiner Firma Iron [CASE: Brand] von X auf X im Monat gebracht… nur im DACH Raum und ohne ein einziges neues Produkt.

Also… bevor du das nächste Produkt launchst oder in ein neues Land gehst…

Klick auf die Ad… dort erklär ich dir, wie wir mit dir erst mal den Rest vom DACH Raum holen.
```

Offen: die Platzhalter "X Y und Z", "ab X Umsatz" und ein Case, der im DACH Raum ohne neues Produkt gewachsen ist.

---

## 9b. Case Study 5.1 "Creative Volume" (AG5)

| # | Was ich geliefert habe | Heiks Reaktion | Lektion |
|---|---|---|---|
| 1 | Hook Influencer vs. AI, mit dem Unterton "AI Videos funktionieren nicht" | "was sind Sebs thoughts on KI Videos?" | Seb ist pro AI. Erst Sebs Haltung prüfen, dann den Gegner wählen |
| 2 | Start mit "AI Ads sind grad am rasieren…", Zeilen wie "weniger Ads" und "rasieren nur das Ad Budget" | "komm schneller zum Punkt… ERST NACHDEM man die Winning Ad gefunden hat kommt AI" | AI kommt nach dem Winner. Nach dem Hook sofort zur Sache |
| 3 | Seb-Anekdote "das haben wir auch mal gemacht… ganze Nächte lang…" | "komplett ohne Sinn" | Keine erfundenen Seb-Storys |
| 4 | – | **Heik dreht die Ad:** Hauptidee Creative Volume, weil die Konkurrenz das predigt und Prospects es glauben. AI nur als Mittel. Er schreibt die ersten 9 Zeilen | Bei Ads gegen die Szene ist der Gegner der Glaube, nicht das Werkzeug |
| 5 | Fortsetzung: dieselbe Message → dieselben Leute, neue Message für neue Gruppe (Seb Ad 11, IM8 Gruppen), eigener Funnel pro Gruppe, AI erst nach dem Winner, "Heißt, 5 Ads mit 5 neuen Messages schlagen 100…", Case | **Body 1:1 übernommen.** Meine 2 Kürzungen auf 270 Wörter hat er nicht übernommen | Flow schlägt Wortzahl. Seine finale Ad hat 276 Wörter |
| 6 | CTA "im Video zeig ich dir, wie wir rausfinden, welche Leute deine Brand noch nicht erreicht" | "CTA mal mehr das Offer, etwas weniger super direkt als Straight Offer Ad" | – |
| 7 | CTA mit Leistungen ("Messages finden… VSL Ads und Funnels bauen") | "nein man, Offer ist auf 8 stellig bringen in den nächsten 3 Monaten" | Offer = Outcome, keine Leistungsliste |
| 8 | CTA "wie wir mit dir deine Brand in den nächsten 3 Monaten auf 8 stellig bringen" | schreibt den CTA selbst | siehe unten |

**Sein CTA (Vorlage für "Offer andeuten" außerhalb von AG6):**
1. Qualifier mit dem Outcome: "falls du deine Ecom Brand von 7 auf 8 stellig skalieren willst…"
2. Eine "Ohne"-Zeile mit dem Schmerz dieser Ad: "Ohne hunderte neue Ads immer ins Leere zu launchen…"
3. Ein schlichter Klick ohne Mechanismus und ohne Zeitversprechen: "Klick mal auf die Ad hier und ich zeig dir genau wie wir dir dabei helfen werden."

Das Offer steckt im Outcome des Qualifiers, nicht im Klick-Satz.

**Finale 5.1 (276 Wörter):**

```
Wie viele Creatives brauchst du WIRKLICH pro Woche, um von 300k auf 1 Million im Monat zu kommen?

Weil wenn du der Ecom Szene Glauben schenkst, sinds 50, 100 oder sogar mehr…

Am besten gleich mit AI gebaut oder mit dutzenden echten Creators.

Und genau das machen gerade die meisten Brands zwischen 100 und 500k im Monat…

Was auch der Grund ist, warum sie es nicht schaffen, auf 1 Mio im Monat zu skalieren.

Ich meine, lass uns mal Folgendes anschauen…

Wir haben mit meiner Firma Iron allein dieses Jahr schon 30 Brands von 7 auf 8 stellig gebracht…

Und meistens haben dafür 3 bis 5 Ads die Woche völlig gereicht.

Weil solange jede dieser Ads wirklich neue Leute erreicht, kannst du easy mal 200k auf nur eine Ad profitabel spenden.

Und genau da liegt der Fehler bei den 100 Ads… wenn alle dieselbe Message haben, zeigt Meta sie halt immer denselben Leuten.

Neue Leute erreichst du nur mit einer neuen Message… bei einem Supplement z.B. einmal für Leute im Gym… einmal für Darmprobleme… einmal fürs Abnehmen.

Jede davon mit eigener VSL Ad und eigenem Funnel dahinter… sonst hält keine Ad 200k Adspend aus.

Und erst wenn da ein Winner steht, machst du daraus mit AI 15 Varianten.

Heißt, 5 Ads mit 5 neuen Messages schlagen 100 Ads mit derselben.

So haben wir [CASE: Brand] von X auf X im Monat gebracht… mit X Ads die Woche.

Also… falls du deine Ecom brand von 7 auf 8 stellig skalieren willst…

Ohne hunderte neue ads immer ins Leere zu launchen…

Klick mal auf die Ad hier und ich zeig dir genau wie wir dir dabei helfen werden.
```

Offen: "30 Brands dieses Jahr", "3 bis 5 Ads die Woche", "200k auf eine Ad" bestätigen, Case mit wenigen Ads pro Woche. Qualifier ähnelt 4.2, Klick-Zeile ähnelt 7.2.

---

## 10. Die Muster (v1: 1–12, neu: 13–22)

**Aus v1 (kurz):**
1. Zu viele Ideen in einer Ad.
2. Eigene Logik schreiben, als hätte Seb sie gesagt.
3. Iron zu früh pitchen.
4. Harte Schnitte zwischen Zeilen.
5. KI-Sätze.
6. Hooks wörtlich kopieren statt das Prinzip zu übernehmen.
7. Feedback zu wörtlich nehmen und überkorrigieren.
8. Annahmen über den Zuschauer.
9. Hooks, die für den ICP nicht stimmen.
10. Fachbegriffe als Labels statt so zu erzählen, wie Seb es macht.
11. Pitch als Leistungsliste, CTA und Authority-Zeile immer gleich.
12. Angle verfehlt den Job oder widerspricht dem Iron-Modell.

**Neu aus 2.3 und 4.3:**

13. **Falsche Referenz für "unsere Ads".** Gemeint sind die fertigen Skripte im Ad-Scripts-Doc (Format, Länge, Lingo). Seb-Transkripte sind nur die Quelle für Inhalt und Phrasen.
14. **Überkorrektur in die Gegenrichtung.** Aus "terrible lingo" wurde Fließtext, aus Training v1 eine sterile Neuversion. Erst verstehen, was gemeint ist. Im Zweifel die letzte Version nehmen, die Heik akzeptiert hat, und nur das Kritisierte fixen.
15. **Den Angle nicht bestätigt.** Bei unklarem oder geändertem Titel erst Optionen vorlegen.
16. **Den Glauben nicht gezählt.** Behauptungen wie "die meisten Belege" oder "fast alle sagen" nur mit echten Zahlen aus den Calls.
17. **Situation und Glaube aus verschiedenen Segmenten gemischt** (Rückgang plus Expansion).
18. **Unklarer Lead-Slang** ("abgegrast") oder abstrakte Begriffe ("oberste Stufe") ohne Klartext.
19. **Andromeda vergessen:** Alltagsmetaphern und branchenfremde Beispiele im Hook ziehen die falsche Zielgruppe.
20. **Langweilige Beschreibung statt Haltung.** "Immer wenn wir reden…" ist kein Hook. Besser: Seb-Attitüde, Status, Glauben als Zitat.
21. **Problem-Framing, wo Chancen-Framing besser trägt** ("du kannst auch einfach… damit öffnet sich…").
22. **Zu viel Arbeit auf eine kleine Frage.** "ist das gut?" oder eine Flow-Frage brauchen eine kurze, gezielte Antwort.

---

## 11. VoC Hook-Bank (wörtlich aus den Calls)

**Rückgang:**
- Tom: "Ich war eine Zeit lang nicht unter 3.000-€-Tagen. Jetzt bin ich bei 2.000-€-Tagen… fühlt sich schon wieder ziemlich schlecht an. Man gewöhnt sich da sehr schnell dran."
- Isabella: "im August sind wir halt echt so abgestürzt"
- Kacper: "letztes Jahr 500, 600.000 € im Monat… ab Oktober extreme Performance-Probleme, auf Meta, auf Google, überall"
- Jakob: "Frühjahr 250.000… viele alte Winning Creatives sind ausgebrannt"

**Winner und System:**
- Tom: "Ich mache und tue. Aber die Ad ist immer schlechter als die vorige." und "kein System, wo ich konstant Winner finden kann"
- Sanja: "Es ist immer das Gleiche, nur wir tweaken es ein bisschen… immer die gleichen Angles"
- Sanja: "hätten wir diese Influencerin nicht gefunden… Katastrophe"
- Isabella: "Spray and Pray… nur Schießen in den Wald… repliziert und nachgeschossen"
- Patrick: "quick and dirty… ein richtiges System fehlt"
- Caro: "keine richtige Strategie zum Skalieren, sondern ganz viele Einzelparts"
- Jakob: "immer die gleichen Leute bespiele… ganz kleines Stück vom Kuchen"

**Media Buyer und Agentur:**
- Isabella: "unser Media Buyer hat gesagt, wir haben schon alles abgegrast, und daran glaube ich in keinster Weise… ich kann ihm nicht widersprechen… nur ein volles Canva-Board"
- Isabella: "ich mag diese Abhängigkeit nicht"
- Kacper: "unzählige Male in Agenturen angesprochen, nie umgesetzt"
- Marcus: "Die Agentur macht eigentlich nur Meta schalten"

**Bottleneck und Team:**
- Isabella: "Okay, ich bin das Bottleneck. Der Tag hat auch nur 24 h."
- Tom: "stundenlang in CapCut"
- Caro: "kündigen die Mitarbeiter, lassen sich krankschreiben, und dann hängt das alles auf uns"
- Isabella: "Wen brauchen wir fürs nächste Level?"
- Metabolae: "We know this, but we don't have the structure for it."

**Kurs oder individuell:**
- Patrick: "Baut ihr mir die Strategie individuell, oder kriege ich Dokumente, Videos, wo ich mir das selbst erarbeiten muss?" und "Das ist deine Liste. Das ist dein Fahrplan. Mach mal."
- Tom: "noch nie jemanden gehabt, der sich das angeschaut hat"

**Expansion:**
- Isabella: "jeden Monat eine weitere Sorte"
- Tom: "neues Produkt… in der Hoffnung"
- Caro: "über Internationalisierung überlegt… jede Agentur hatte ihre eigene Meinung"
- Sanja: "neuer Markt"

**Q4 und Angst:**
- Isabella: "Was wir nicht machen können, ist jetzt dippen oder langsamer werden"
- Sanja: "Risiko, in der High Season Agenturen zu wechseln" und "die Kohle nicht verbrennen"
- Patrick: "50 % vom Umsatz in Q4"

**Geld:**
- Isabella: "Wenn wir 120k machen, kommen wir bei einem Nuller raus"
- Seb (VSL): "Geld, das wirklich auf dem Konto landet und nicht nur die nächste Warenfinanzierung rollt"

**CSM-Wissen (hea-rs):** "problem aware is way way bigger than the other awareness stages", "very cheap traffic for problem aware", Taboola ist gut für Unaware und Problem Aware. Die CSMs machen für jedes Produkt und jedes Land eine "Market Awareness Research".

---

## 12. Checkliste vor dem Abschicken

- [ ] Ist der Angle in einem Satz bestätigt (oder von Heik vorgegeben)?
- [ ] Kommt der Glaube aus den Calls, ist er gezählt und mit Lead-Worten belegt? Stammen Situation und Glaube aus demselben Segment?
- [ ] Trägt der Hook ICP-Lingo (Andromeda)? Keine Alltagsmetapher, kein fremdes Beispiel?
- [ ] Ist der Hook polarisierend, wahr, mit Intrigue durch Haltung, und ist der Hook-Typ noch frei?
- [ ] Ist alles klar? Kein Slang ohne Erklärung, Fachbegriffe direkt erklärt?
- [ ] Eine Idee, Zugeständnis und Reframe vor der Lösung, Chancen-Framing, wo es passt?
- [ ] Hängt jede Zeile an der vorigen (Brückenwörter), habe ich die Ad im Kopf laut gelesen?
- [ ] Mechanismus in Seb's Worten und nicht wörtlich aus anderen Ads?
- [ ] Iron erst im Proof, Authority- oder Case-Zeile neu, passt der Proof zum Mechanismus?
- [ ] CTA: Qualifier spiegelt den Hook, direkter Klick, neu formuliert, kein Duplikat innerhalb der Ad Group?
- [ ] Iron-Modell: DWY, Expansion positiv, keine Agentur-Framing?
- [ ] 250–270 Wörter mit `wc -w`?
- [ ] Ein Code-Block, 1 Leerzeile, keine Kommentare, Heiks Zeilen wörtlich?
- [ ] Antwort danach kurz: Änderungen, Quellen, Abgeleitetes, Offenes?
