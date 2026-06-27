from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

TRAIN_DIR = DATA_DIR / "train_pairs" / "pair_1"
DIRTY_TRAIN_CSV = TRAIN_DIR / "dirty.csv"
CLEAN_TRAIN_CSV = TRAIN_DIR / "clean.csv"

INPUTS_DIR = DATA_DIR / "inputs"
OUTPUTS_DIR = DATA_DIR / "outputs"

PROMPTS_FILE = ROOT / "prompts.txt"