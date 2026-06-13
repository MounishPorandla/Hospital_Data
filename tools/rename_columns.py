import pandas as pd
from utils import logger

def rename_columns(df: pd.DataFrame, mapping: dict) -> tuple[pd.DataFrame, str]:
    """
    Renames columns based on a mapping dict.
    mapping = {"pt_nm": "patient_name", "DOB": "date_of_birth"}
    """
    logger.info(f"Renaming columns: {mapping}")

    # only rename columns that actually exist
    valid_mapping = {k: v for k, v in mapping.items() if k in df.columns}
    df = df.rename(columns=valid_mapping)

    result = f"Renamed {len(valid_mapping)} columns: {valid_mapping}"
    logger.info(result)
    return df, result
