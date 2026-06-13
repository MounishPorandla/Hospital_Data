import json
import groq
from config import GROQ_API_KEY, MODEL_NAME
from utils import logger

from tools.infer_schema import infer_schema
from tools.rename_columns import rename_columns
from tools.fix_dates import fix_dates
from tools.fix_casing import fix_casing
from tools.flag_nulls import flag_nulls
from tools.write_output import write_output

client = groq.Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """ 
You are a hospital data cleaning agent.
You will be given a summary of a messy hospital CSV file.
Your job is to clean it by calling the available tools in the right order.

Always follow this sequence:
1. infer_schema - understand what columns exist and what they should be
2. rename-columns - fix column names
3. fix_dates - normalise data formats
4. fix-casting - fix name casting
5. flag_nulls - mark missing values
6. write_output - save the cleaned file

Call one tool at a time. Be methodical. 
When generating tool parameters, NEVER insert natural conversation text, comments, or extra commas inside or around the JSON payload tags.
- Open and close your tool function tags cleanly. Do not mutate equal signs or brackets.
You are the detective """

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "infer_schema",
            "description": "Look at column names and asample data, figure out what each column should be named and what typeit is",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
           }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rename_columns",
            "description": "Rename messy column names to clean standard names based on schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "mapping": {
                        "type": "object",
                        "description": "Dictionary of old column name to new column name"
                    }
                },
                "required": ["mapping"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fix_dates",
            "description": "Normalize all date columns to YYYY-MM-DD format",
            "parameters": {
                "type": "object",
                "properties": {
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of column names that contain dates"
                    }
                },
                "required": ["columns"]
            }
        }

    },
    {
        "type": "function",
        "function": {
            "name": "fix_casting",
            "description": "Title-case name columns, uppercase ID columns",
            "parameters": {
                "type": "object",
                "properties": {
                    "name_columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "columns that should be title Cased"
                    },
                    "id_columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": " Columns that should be UPPERCASED"
       
                    }
                },
                "required": ["name_columns", "id_columns"]
            }
        }

    },
    {
        "type": "function",
        "function": {
            "name": "flag_nulls",
            "description": "Find rows with missing required fields and mark them",
            "parameters": {
                "type": "object",
                "properties": {
                    "required_columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Columns that must not be empty"
                    }
                },
                "required": ["required_columns"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_output",
            "description": "Save the cleaned dataframe to CSV and write the audit log",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def dispatch_tool(tool_name: str, tool_args: dict, df, audit_log: list):
    """
    The llM says 'call fix_dates with these args'.
    dispatch_tool actually runs it.
    Think of this as a detective's assistant who executes orders.
    """

    if tool_name == "infer_schema":
        result = infer_schema(df)
        return result, df
    
    elif tool_name == "rename_columns":
        df, result = rename_columns(df, tool_args["mapping"])
        return result, df
    elif tool_name == "fix_dates":
        df, result = fix_dates(df, tool_args["columns"])
        return result, df
    elif tool_name == "fix_casing":
        df, result = fix_casing(df, tool_args["name_columns"], tool_args["id_columns"])
        return result, df
    elif tool_name == "flag_nulls":
        df, result = flag_nulls(df, tool_args["required_columns"])
        return result, df
    elif tool_name == "write_output":
        result = write_output(df, audit_log)
        return result, df
    else:
        return f"Unknown tool: {tool_name}", df

def run_agent(df):
    logger.info("Agent starting...")


    #summarise the data frame for the LLM

    summary = {
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "sample": df.head(3).to_dict()
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here is the hospital data summary: {json.dumps(summary)}. Please clean it."}
    ]
    audit_log = []

    #the loop
    while True:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        message = response.choices[0].message

        #if no tool call - agent is done

        if not message.tool_calls:
            logger.info("Agent finished.")
            logger.info(f"Agent says: {message.content}")
            break

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            logger.info(f"Agent calling tool: {tool_name} with args: {tool_args}")

            #run the actual tool
            result, df = dispatch_tool(tool_name, tool_args, df, audit_log)

            #log it
            audit_log.append({
                "tool": tool_name,
                "args": tool_args,
                "result": str(result)
            })

            #send result back to LLM

            messages.append({"role": "assistant", "content": None, "tool_calls": message.tool_calls})
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return df, audit_log

