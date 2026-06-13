import pandas as pd
from utils import logger

def read_file(filepath: str) -> pd.DataFrame:

    file_name = filepath.name if hasattr(filepath, "name") else str(filepath)
    logger.info(f"Reading file: {file_name}")

    if file_name.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file type: {file_name}")
    
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df
