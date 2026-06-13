# 🏥 Hospital Data Cleaning Agent

An intelligent data cleaning pipeline powered by Groq LLMs and Python Pandas.

## Project Architecture
- `agent.py`: Pipeline orchestration CLI entry point.
- `agent_loop.py`: Core decision engine loop using JSON tool calling schemas.
- `tools/`: Atomic code components managing individual pandas transformations.
- `utils.py`: Diagnostic logging system configurations.

## Getting Started
1. Install dependencies: `pip install pandas groq python-dotenv`
2. Create a `.env` file containing your `GROQ_API_KEY`.
3. Run the pipeline: `python agent.py`