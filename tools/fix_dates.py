import pandas as pd
from utils import logger

def fix_dates(df: pd.DataFrame, columns: list) -> tuple[pd.DataFrame, str]:
    """ 
    Normalises date columns to YYYY-MM-DD format.
    Handles messy formats like 01/05/1990, May 1 1990, 1990.01.05 etc.
    """
    logger.info(f"Fixing dates in columns: {columns}")
    fixed = []

    for col in columns:
        if col not in df.columns:
            continue
        try:
            parsed = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
            if parsed.notna().any():
                df[col] = parsed.dt.strftime("%Y-%m-%d")
                fixed.append(col)
            else:
                logger.warning(f"Skipping column {col}: no parseable dates found")
        except Exception as e:
            logger.warning(f"Could not fix dates in column {col}: {e}")

    result = f"Fixed date format in columns: {fixed}"
    logger.info(result)
    return df, result