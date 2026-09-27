# Orderrapport

Ett Python-program som läser in orderdata från en CSV-fil, städar och validerar datan och skapar rapporter över försäljning och returer.

Programmet skapar fyra rapporter i mappen `output/`:

`overview.csv` Total försäljning, antal ordrar och antal returer

`sales_by_category.csv` Försäljning och returgrad per produktkategori

`sales_by_region.csv` Försäljning och returgrad per region

`returns_by_category.csv` Returer per produktkategori, sorterat på returgrad

# Miljö
- **Python:** 3.14.5
- **Pandas:** 3.0.6
- **Pytest:** 9.1.1

## Hur man kör projektet:

```bash
# klona projektet
git clone https://github.com/KevinCJohansson/Order-report-project.git

# Skapa och aktivera virtuell miljö
python -m venv . venv
# Windows PowerShell
.venv\Scripts\Activate

# macOs\ Linux
# source .venv/bin/activate

# installera beroenden
python -m pip install -r requirement.txt
```

```bash
python main.py
```

Rapporterna sparas i `output/`, som skapas automatiskt om den saknas. Körningen loggas både i terminalen och i `order_report.log`.

## Köra testerna

```bash
python -m pytest
```

## Projektstruktur

```
├── main.py              # Startpunkt, loggning och felhantering
├── requirements.txt
├── order_report.log     # Loggfil för programmet
├── data/
│   └── orders.csv       # Indata
├── output/              # Rapporter (skapas vid körning)
├── src/
│   ├── config.py        # Sökvägar
│   ├── loader.py        # Läser in CSV-filen
│   ├── validation.py    # Kontrollerar kolumner och värden
│   ├── cleaning.py      # Städar och standardiserar data
│   ├── reports.py       # Beräkningar och rapporter
│   └── exports.py       # Sparar rapporterna
└── tests/               # Tester med pytest