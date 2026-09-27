from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_orders(input_path: Path) -> pd.DataFrame:
    """Läser in orderdata från en CSV-fil."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    logger.info("Reading data from %s", input_path)
    data = pd.read_csv(input_path)
    logger.info("Read %d rows", len(data))
    return data