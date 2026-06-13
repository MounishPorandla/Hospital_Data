import pandas as pd
from utils import logger

def infer_schema(df: pd.DataFrame) -> dict:
    """
    Looks at column names + sample data and returns a summary
    for the LLM to understand what's in the dataframe.
    """
    logger.info("Inferring schema...")

    schema = {
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "sample": df.head(3).to_dict()
    }

    logger.info(f"Schema inferred: {schema['columns']}")
    return schema