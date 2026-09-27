# Reflektion

## 1. Vilka var de viktigaste problemen i originalkoden?
All kod låg i ett enda långt flöde utan funktioner och kördes direkt vid import, vilket gjorde den svår att återanvända och omöjlig att testa. Felhanteringen var ett brett `try/except` som bara skrev ut ett kort meddelande och avslutade programmet som om allt gått bra. Felaktiga värden ersattes utan att det syntes, samma beräkningar upprepades på flera ställen och variabelnamn som `result1` sa lite om innehållet.

## 2. Vilka förändringar förbättrade programmet mest?
Uppdelningen i moduler, eftersom den gjorde varje del lätt att förstå och möjlig att testa var för sig. Loggningen gjorde också stor skillnad, framför allt varningarna när värden ersätts. Tidigare ändrades data utan att någon märkte det, nu syns det i loggen. Felhanteringen är också tydligare: kända fel som tom data eller saknade kolumner ger ett meddelande som säger vad som är fel, och programmet avslutas med felkod.

## 3. Varför valde jag den projektstruktur jag använde?
Varje modul i `src/` motsvarar ett steg i flödet: inläsning, validering, städning, beräkning och export. Då är det lätt att hitta var något händer, och `main.py` blir en kort översikt över hela programmet. `main.py` ligger i projektets rot så att importerna fungerar utan path-hack. Jag flyttade först koden utan att ändra beteendet och kontrollerade att rapporterna blev identiska med originalets innan jag började förbättra, så att jag visste att skillnader berodde på mina ändringar och inte på flytten.

## 4. Var använde jag OOP/dataclass och varför?
`ReportConfig` samlar sökvägarna på ett ställe. Den är `frozen` så att inställningarna inte kan ändras av misstag, och den skickas in som argument så att funktionerna kan köras mot andra filer, till exempel i tester. `ValidationResult` samlar alla valideringsfel så att användaren ser alla problem på en gång i stället för ett i taget. Den har både data och beteende (`add_error`, `is_valid`, `raise_if_invalid`), vilket ger valideringen ett tydligt ansvar och gör det lätt att testa exakt vilka fel som hittades.

## 5. Vad skyddar testerna?
Testerna kontrollerar att ordervärde och rabatt räknas rätt, att returer tolkas korrekt, att sammanfattningarna per kategori och region ger rätt summor, returgrad och sortering, och att ogiltiga värden ersätts. De testar också felscenarier: saknade kolumner och orimliga värden.

## 6. Vad var svårast?
Att förstå exakt vad beräkningarna gjorde och vilka regler som gäller, till exempel att en bok utan pris fick medianpriset för alla produkter. Det var också svårt att bestämma hur ansvaret skulle fördelas mellan modulerna och att se till att beteendet var oförändrat efter omstruktureringen.

## 7. Vad hade jag velat förbättra med mer tid?
Ersätta saknade priser med medianen per kategori och flagga okända värden i returkolumnen i stället för att tolka dem som "ej returnerad". Jag hade också velat bestämma om returnerade ordrar ska räknas som försäljning, använda eller ta bort de oanvända kolumnerna `order_date` och `customer_id`.