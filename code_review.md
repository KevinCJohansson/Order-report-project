# Kodgranskning av order_report.py

## Utgångsläge
Scriptet läser `data/orders.csv` och genererar fyra rapporter till `output/`.

## Granskningsfynd

### Fynd 1 - Programmet körs vid import

**Observation:** Koden ligger direkt på modulnivå, vilket gör att hela flödet körs vid import.

**Konsekvens:** En import läser data och skriver filer som en sidoeffekt. Det gör att delar av koden inte kan återanvändas, och testverktyg som pytest kör hela programmet redan när modulen importeras.

**Förslag:** Flytta logiken till en funktion `main()` och anropa den bara när filen körs direkt, med `if __name__ == "__main__": main()`.

### Fynd 2 - Bred och otydlig felhantering

**Observation:** Hela programmet ligger i ett enda `try` - `except`.

**Konsekvens:** Den enda faktiska valideringen kontrollerar om rätt kolumner finns. Övriga fel som uppstår senare fångas av den breda `except`, som avbryter programmet där felet sker. Detta kan leda till att vissa rapporter skapas medan andra inte gör det. Felmeddelanden ger inte tydlig information om vad som var fel, och traceback saknas, vilket gör felsökning svår.

**Förslag:** Bygg en robustare felhantering som fångar specifika fel och ger tydliga felmeddelanden om vad som gått fel. Skapa rapporterna först när samtliga beräkningar har lyckats, så att inga halvfärdiga rapporter skapas. Traceback hanteras genom loggning, se fynd 3.

### Fynd 3 - Utskrifter med print istället för loggning

**Observation:** Programmet använder `print` för all utskrift, både för statusmeddelanden och för fel.

**Konsekvens:** Det blir svårt att skilja vanlig information från varningar och fel. Utskrifterna sparas inte heller någonstans, vilket gör det svårt att i efterhand se vad som skett vid en körning. Vid fel saknas traceback, vilket försvårar felsökningen.

**Förslag:** Ersätt `print` med `logging`. Använd olika nivåer för information, varningar och fel, och logga fel tillsammans med traceback. Spara loggen i en separat fil.

### Fynd 4 - Utdatamappen skapas aldrig

**Observation:** Rapporterna sparas i mappen `output`, men programmet varken skapar mappen eller kontrollerar att den finns.

**Konsekvens:** Saknas mappen kan programmet inte skapa några rapporter.

**Förslag:** Skapa utdatamappen i början av programmet om den inte redan finns.

### Fynd 5 - All logik ligger i ett och samma flöde

**Observation:** Inläsning, validering, datastädning, beräkningar och filskrivning ligger i ett enda block i en och samma fil, utan någon uppdelning.

**Konsekvens:** Delarna kan inte ändras, återanvändas eller testas var för sig.

**Förslag:** Dela upp koden i moduler där varje modul har sitt eget ansvarsområde, och låt `main()` styra flödet.

### Fynd 6 - Duplicerad kod och otydliga namn

**Observation:** Samma logik för gruppering, beräkning av returgrad och sortering upprepas flera gånger. Variabelnamn som `result1`, `result2` och `data` säger väldigt lite om innehållet.

**Konsekvens:** Ändringar måste göras på flera ställen, vilket ökar risken för fel. Otydliga namn gör koden svårläst.

**Förslag:** Bryt ut den upprepade logiken till en gemensam funktion och använd mer beskrivade namn.

### Fynd 7 - Otydliga beräkningar och bristande validering av data

**Observation:** Utöver kolumnkontrollen valideras inte indatan. Saknade och felaktiga värden ersätts med standardvärde utan motivering.

**Konsekvens:** Rapporterna kan visa felaktiga siffror som ser korrekta ut. T.ex. är böcker mycket billigare än de andra kategorierna, så om en bok saknar pris får den istället medianpriset för alla produkter, vilket med största sannolikhet ger ett missvisande resultat.

**Förslag:** Validera indatan så att orimliga värden upptäcks, och välj standardvärden som passar datan bättre, t.ex. medianpriset inom samma kategori istället för medianpriset för alla produkter.
När ett värde ersätts bör det också loggas så att man kan se det i efterhand.