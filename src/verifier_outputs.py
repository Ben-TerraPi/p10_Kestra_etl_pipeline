from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
REPORT_FILE = OUTPUT_DIR / "rapport_chiffre_affaires.xlsx"
PODIUM_PREMIUM_FILE = OUTPUT_DIR / "vins_premium.csv"
PODIUM_ORDINARY_FILE = OUTPUT_DIR / "vins_ordinaires.csv"


def verify_outputs() -> None:
    """Vérifie la présence des fichiers de sortie et les volumes attendus."""
    required_files = [REPORT_FILE, PODIUM_PREMIUM_FILE, PODIUM_ORDINARY_FILE]
    missing_files = [str(path) for path in required_files if not path.exists()]
    assert not missing_files, f"Missing output files: {missing_files}"

    premium_count = len(pd.read_csv(PODIUM_PREMIUM_FILE))
    ordinary_count = len(pd.read_csv(PODIUM_ORDINARY_FILE))

    assert premium_count == 30, f"Expected 30 premium wines, got {premium_count}"
    assert ordinary_count == 684, f"Expected 684 ordinary wines, got {ordinary_count}"

    print(f"Validation OK: premium={premium_count}, ordinaires={ordinary_count}")


if __name__ == "__main__":
    verify_outputs()