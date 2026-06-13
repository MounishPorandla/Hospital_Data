import sys
from tools.read_file import read_file
from agent_loop import run_agent
from config import INPUT_FILE
from utils import logger

def main():
    # get file path from command line or use default
    filepath = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE

    logger.info(f"Starting hospital data cleaning agent on: {filepath}")

    # step 1: read the file into a dataframe
    df = read_file(filepath)

    # step 2: run the agent loop
    cleaned_df, audit_log = run_agent(df)

    logger.info(f"Done. {len(cleaned_df)} rows cleaned.")
    logger.info(f" Audit log has {len(audit_log)} entries.")

if __name__ == "__main__":
    main()

