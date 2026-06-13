import json
import pandas as pd
from utils import logger
from config import OUTPUT_FILE, AUDIT_FILE

def write_output(df: pd.DataFrame, audit_log: list) -> str:
    """
    Saves the cleaned dataframe to CSV.
    Saves the audit log to JSON.
    """
    logger.info(f"Writing cleaned data to {OUTPUT_FILE}")
    df.to_csv(OUTPUT_FILE, index=False)

    logger.info(f"Writing audit log to {AUDIT_FILE}")
    with open(AUDIT_FILE, "w") as f:
        json.dump(audit_log, f, indent=2)

    result = f"Saved cleaned CSV to {OUTPUT_FILE} and audit log to {AUDIT_FILE}"
    logger.info(result)
    return result
