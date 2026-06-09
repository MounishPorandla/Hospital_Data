import os 
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-70b-8192"

INPUT_FILE = "data/hospital_sample.csv"
OUTPUT_FILE = "data/hospital_cleaned.csv"
AUDIT_FILE = "data/audit_log.json"