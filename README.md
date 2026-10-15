# Generative Fashion

## Domanda di ricerca e sintesi progettuale
> **In che misura un modello di IA generativa è in grado di tradurre fedelmente in immagini un look descritto dalla critica di moda, e quanto è in grado di riconoscere i limiti delle proprie traduzioni?**

Il progetto indaga **l'interazione tra il linguaggio specialistico della critica di moda e la generazione visiva**. A partire da tre recensioni di Vogue Italia dedicate a look eterogenei del Met Gala 2026, ho sviluppato una pipeline di web scraping e raffinamento semantico via API (Gemini Pro), necessaria per isolare i dettagli descrittivi dell'abito e superare i vincoli di sicurezza del modello. Utilizzando i testi purificati come prompt, ho generato un corpus di 60 immagini (20 per ciascun look in sessioni indipendenti) e definito una griglia analitica su cinque dimensioni (coerenza, palette, silhouette, materiali e styling). Infine, ho sottoposto le immagini a un **processo di autovalutazione da parte dello stesso LLM**, incrociando i suoi punteggi con i miei per misurare la fedeltà visiva, l’eventuale compiacenza del modello e i bias ricorrenti emersi (dalla normalizzazione delle forme insolite alla standardizzazione fisiognomica).

---

## Obiettivi
* **Valutazione della fedeltà visiva:** misurare la corrispondenza delle immagini generate rispetto ai look originali (silhouette, palette cromatica, resa dei materiali, volumi).
* **Mappatura delle asimmetrie semantiche:** individuare quali aspetti dei look reali vengono interpretati più facilmente e quali risultano difficili da tradurre.
* **Confronto valutativo:** mettere a confronto il giudizio umano con l’autovalutazione del modello per verificare l'eventuale presenza di sovrastima delle immagini prodotte.
* **Analisi critica dei bias e dei limiti:** riflettere sulla tendenza all'appiattimento dei canoni estetici (bodyshape standardizzato, età, etnia) e sulla frammentazione/superficialità interpretativa tipica dell'IA generativa.

---
