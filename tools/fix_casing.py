import pandas as pd
from utils import logger

def fix_casing(df: pd.DataFrame, name_columns: list, id_columns: list) -> tuple[pd.DataFrame, str]:
    """
    Title-cases name columns (john doe → John Doe)
    Uppercases ID columns (abc123 → ABC123)
    """
    logger.info(f"Fixing casing — names: {name_columns}, IDs: {id_columns}")

    for col in name_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()

    for col in id_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper()

    result = f"Fixed casing for name columns: {name_columns}, ID columns: {id_columns}"
    logger.info(result)
    return df, result