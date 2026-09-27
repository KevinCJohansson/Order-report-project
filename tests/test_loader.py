from pathlib import Path
import pytest
from src.loader import load_orders

def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_orders(Path("does_not_exist.csv"))