import logging
import sys

from src.cleaning import clean_orders
from src.config import ReportConfig
from src.exports import write_reports
from src.loader import load_orders
from src.reports import build_reports
from src.validation import validate_columns, validate_values

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    """Loggar både till terminalen och till en fil."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("order_report.log", encoding="utf-8"),
        ],
    )

def main() -> int:
    setup_logging()
    config = ReportConfig()
    logger.info("Starting order report")

    try:
        data = load_orders(config.input_path)
        validate_columns(data)
        data = clean_orders(data)
        validate_values(data).raise_if_invalid()
        reports = build_reports(data)
        write_reports(reports, config.output_path)

    except (FileNotFoundError, ValueError) as error:
        logger.error("The report could not be completed: %s", error)
        return 1
    except Exception:
        logger.exception("Unexpected error")
        return 1

    logger.info("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())