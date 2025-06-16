---
title: "Wie erstelle ich einen neuen Artikel für die Webseite des Göttinger Klimabündnis"
subtitle: "Ein paar Tips zur Erstellung von Artikeln von der Redaktion"
date: 2021-04-10T12:50:34+01:00
abstract: "Auf dieser Seite wird erklärt, wie ein neuer Artikel für die Webseite des Göttinger Klimabündnis erstellt wird"
image: "img/banner/post-bg-coffee.jpeg"
draft: false
---

# Wie erstelle ich einen neuen Artikel
## Hilfe bei der Formatierung für die Webseite des Göttinger Klimabündnis

Im folgenden gibt es ein paar Tipps, wie ihr Posts formatieren solltet, damit
sie auf den Webseiten des Göttinger Klimabündnis optimal dargestellt werden,
und wie die Arbeit der Redaktion entlastet werden kann. 

Natürlich garantiert eine ordentliche Formatierung zwar nicht die
Veröffentlichung, aber ohne eine solche sinkt die Wahrscheinlichkeit dafür
drastisch.

Eine genauere Beschreibung mit Beispielen lässt sich
[auf dieser externen Seite](https://demo.hedgedoc.org/features?both)
finden.

## Der Header

Jeder Post muss mit ein paar Metadaten versehen werden, damit er sinnvoll in
die Webseiten einsortiert werden kann. 

### Der Header für Artikel

Zum Beispiel hat dieser Artikel den
folgenden Header:

```
---
title: "Wie erstelle ich einen neuen Artikel für die Webseite des Göttinger Klimabündnis"
subtitle: "Ein paar Tips zur Erstellung von Artikeln von der Redaktion"
date: 2021-04-10T12:50:34+01:00
abstract: "Auf dieser Seite wird erklärt, wie ein neuer Artikel für die Webseite des Göttinger Klimabündnis erstellt wird"
draft: true
categories: [ "Hilfe" ]
---
```

* ***title:*** Titel des Artikels (max. 80 Zeichen)
* ***subtitle:*** Untertitel des Artikels (max. 120 Zeichen)
* ***date:*** das Erscheinungs-Datum, Format: jjjj-mm-ttTHH:MM:SS+0A:00 , wobei A die Abweichung von Universal-Time ist (Sommerzeit +2h, Winterzeit +1h).
* ***abstract:*** eine kurze Zusammenfassung des Textes (max. 200 Zeichen)
* ***categories:*** eine Liste von Stichwörtern oder Kategorien die zu dem Artikel passen.

### Der Header für Veranstaltungen

Hier werden zusätzlich noch weitere Daten, wie der Veranstaltungsort usw. gebraucht:

```
---
title:         "Klimaschutz-Tage Göttingen 2021"
subtitle:      "den Rahmen für die Klimaschutz-Tage bietet die Stadt Göttingen"
date:          2021-06-18T12:30:00+02:00
etime:         2021-06-18T21:00:00+02:00
author:        "Klimaschutz Göttingen"
place:         "Goettingen"
locURL:        "https://klimaschutz.goettingen.de/staticsite/staticsite.php?menuid=267&topmenu=14"
---
```
* ***date:*** ist hier Datum und Beginn der Veranstaltung, nicht das Erscheinungs-Datum wie zuvor
* ***etime:*** ist hier Datum und ungefähre Ende der Veranstaltung
* ***author:*** gibt den Veranstalter an, und 
* ***place:*** den Veranstaltungsort
* ***locURL:*** kann für weiterführende Links zu anderen Seiten verwendet werden.

Mindestens vorhanden sein müssen Titel und das Datum mit der Uhrzeit, aber
normalerweise reicht das natürlich als Information für die Besucher nicht
aus. Dann muss entweder mit ***locURL:*** auf die externe Seite verlinkt
werden, oder die notwendigen Infos müssen im Header oder im Text stehen.
  
### Titel, Untertitle, Zusammenfassung und Datum

sind oben hinreichend beschrieben.

### Stichwörter oder Kategorien

Diese werden im Block Themen gesammelt, gegebenenfalls auch in ausgewählten
Themen aus der Kopfleiste des Webseite.

Die Liste der Kategorien wird mit eckigen Klammern umschlossen, jede der
Kategorien ist mit Anführungszeichen umschlossen und durch Kommas von den
anderen getrennt.

Die derzeitige Liste der verfügbaren Kategorien ist:
* Hilfe
* Bauen, Wohnen
* Energie
* Gesundheit
* Mobilität
* Pressemitteilung
* Monitoring, Controlling

Aber dies ist im Moment noch weitgehend frei gestaltbar und wird später überarbeitet.

## Der Textteil des Artikels mithilfe von Markdown

Um eine möglichst einfache und plattform-unabhängige Darstellung von Texten zu
ermöglichen, wurde eine spezielle Beschreibungsform für die Textformattierung
eingeführt, mit der zum Beispiel Überschriften, Einrückungen, Spiegelstriche,
Hervorhebungen oder Absätze markiert, 
aber auch zum Beispiel Links auf andere
Stellen im Text oder im Netz erstellt und auch Fotos eingebunden werden
können.

Der volle Umfang dessen, was damit dargestellt werden kann, lässt sich zum
Beispiel [auf dieser Seite](https://demo.hedgedoc.org/features?both) sowohl in
einer Darstellung des ursprünglichen Markup-Textes links, als auch in der
entsprechend formatierten Form rechts finden.

Die wichtigsten Themen seien hier im Folgenden kurz behandelt:


### Überschriften

werden durch '#'s am Anfang der Zeile festgelegt. Beispiel:

```
# Wie erstelle ich einen neuen Artikel 
## Hilfe bei der Formatierung für die Webseite des Göttinger Klimabündnis
### Überschriften
```

### Absätze
Ein neuer Absatz entsteht immer dann, wenn im Text eine Leerzeile vorkommt.

### Fett, Schräg, Durchgestrichen

Texttypen wie **Fett**, __fett__, *schräg*, oder ~~durchgestrichen~~ können
mit bündig vor oder hintan gestellten Zeichen im laufenden Text ausgewählt werden, wie in:

```
**Fett**, __fett__, *schräg*, oder ~~durchgestrichen~~
```

Unterstreichungen sind nicht möglich.

### Spiegelpunkte

Spiegelpunkte brauchen einen eigenen Absatz, müssen also eine Leerzeile
darüber und darunter haben. 
Gestaffelte Spiegelstriche werden

- durch
   - die
   * Nutzung
      * von
   * Minuszeichen oder Sternen
- mit

Einrückungen durch drei Leerzeichen erzeugt, wie zum Beispiel mit

```

- durch
   - die
   * Nutzung
      * von
   * Minuszeichen oder Sternen
- mit

```

### Nummerierungen

1. Nummerierungen
   1. können
   2. auch
2. eingerückt
   1. werden

```

1. Nummerierungen
   1. können
   2. auch
2. eingerückt
   1. werden

```



### Einrückungen

Einrückungen eignen sich zum Beispiel gut für die Markierung wörtlicher Rede.

> Sie brauchen ebenfalls einen eigenen Absatz, müssen also eine Leerzeile
darüber und darunter haben und können durch das größer-Zeichen am Anfang der
ersten Zeile des Absatzes erreicht werden,

wie in: 

```

> Sie brauchen ebenfalls einen eigenen Absatz, müssen also eine Leerzeile
darüber und darunter haben und können durch das größer-Zeichen am Anfang der
ersten Zeile des Absatzes erreicht werden,

```
### Links

Links auf andere Stellen im Text oder im Netz lassen sich
durch einen Textteil in eckigen Klammern und der Hyperlink-Referenz
in runden Klammern erzeugen, wie zum Beispiel im Hinweis für die
weiterführenden Beispielen
[auf dieser externen Seite](https://demo.hedgedoc.org/features?both)
, das wie folgt dargestellt wird:

```
[auf dieser externen Seite](https://demo.hedgedoc.org/features?both)
```

Alle Links auf diesen Web-Seiten führen immer zur Öffnung eines neuen
Browser-Fensters.

### Fotos

Fotos lassen sich ähnlich wie Links einfügen, brauchen allerdings ein
vorangestelltes "!" ![Beispiel](/img/banner/2019-05-13-deutsches-theater-nachts.jpg) und müssen
auf ein Bild im Netz verweisen. Dies wird zum Beispiel wie folgt angegeben:

```
... vorangestelltes "!" ![Beispiel](/img/2019-05-13-deutsches-theater-nachts.jpg) und
müssen ...
```
Der Text zwischen den eckigen Klammern wird genutzt, wenn das Bild vom Browser
im Netz nicht gefunden wird.

Die Größe eines Fotos 
{{< figure src="/img/banner/2019-05-13-deutsches-theater-nachts.jpg" alt="Beispiel" width="250px" >}}
kann mittels einer Angabe wie zum Beispiel der folgenden eingestellt werden:

```
{ {< figure src="/img/banner/2019-05-13-deutsches-theater-nachts.jpg" alt="Beispiel" width="250px"
>} }
```

**Wichtig:** 
Ein solches Bild kann bei entsprechedner Referenz zwar irgendwo liegen, 
aber dann ist unbedingt das **Copyright** zu
beachten. Das bedeutet, dass hier, wenn überhaupt Bilder aus externen Quellen
genutzt werden, **nur gemeinfreie Bilder**, i.a. mit einer entsprechenden
Quellenangabe, angegeben werden können.

Beim **Einfügen von eigenen Bildern** in Texte müssen diese Bilder mit and
die Redaktion übermittelt werden, zum Beispiel als Anhang einer Mail. Der Name des Bildes
sollte dann in den runden Klammern eingetragen sein. Wenn es eigene
Copyright-Ansprüche gibt, müssen diese im Text klargemacht werden.

### Tabellen 

Tabellen

|          | tic | tac | toe |
|----------|:---:|:---:|:---:|
| du       |  x  |     |  x  |
| *bist*   |  o  |  o  |     |
| **dran** |     |  o  |  x  |

brauchen ebenfalls einen eigenen Absatz und können wie folgt erzeugt werden
(':' für Mittelsatz):

```
|          | tic | tac | toe |
|----------|:---:|:---:|:---:|
| du       |  x  |     |  x  |
| *bist*   |  o  |  o  |     |
| **dran** |     |  o  |  x  |
```

Ulrich Schwardmann

Göttingen, den 10.4.2021

*uScw*
