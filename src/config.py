from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ReportConfig:
    input_path: Path = Path("data/orders.csv")
    output_path: Path = Path("output")