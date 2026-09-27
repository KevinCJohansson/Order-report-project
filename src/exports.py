import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

def write_reports(reports: dict[str, pd.DataFrame], output_path: Path) -> None:
    """Skapar utdatamappen vid behov och sparar alla rapporter som CSV-filer."""
    output_path.mkdir(parents=True, exist_ok=True)

    for filename, report in reports.items():
        report.to_csv(output_path / filename, index=False)
        logger.info("Saving reports to %s", output_path)
        logger.info("Saved %s", filename)