import pandas as pd
from utils import logger

def flag_nulls(df: pd.DataFrame, required_columns: list) -> tuple[pd.DataFrame, str]:
    """
    Finds rows where required columns are missing.
    Adds a new column 'has_missing_data' = True/False
    """
    logger.info(f"Flagging nulls in required columns: {required_columns}")

    existing = [col for col in required_columns if col in df.columns]
    df["has_missing_data"] = df[existing].isnull().any(axis=1)

    flagged_count = df["has_missing_data"].sum()
    result = f"Flagged {flagged_count} rows with missing required fields"
    logger.info(result)
    return df, result