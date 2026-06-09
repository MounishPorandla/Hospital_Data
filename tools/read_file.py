import pandas as pd
from utils import logger

def read_file(filepath: str) -> pd.DataFrame:
    logger.info(f"Reading file: {filepath}")

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")
    
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df