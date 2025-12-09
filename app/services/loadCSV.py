import pandas as pd
import sqlite3
import sys

def import_csv_to_db(conn, file_path: str, table: str) -> int:
    """
    Read a CSV file and insert its rows into a SQLite table.
    Returns the number of rows successfully added.
    """
    print(f"Loading data from {file_path} into '{table}'...")
    try:
        # Load CSV into a DataFrame (first row = headers)
        data_frame = pd.read_csv(file_path)

        # Push DataFrame into the database
        data_frame.to_sql(
            name=table,
            con=conn,
            if_exists="append",
            index=False
        )

        count = len(data_frame)
        print(f"Inserted {count} rows into '{table}'.")
        return count

    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
    except pd.errors.EmptyDataError:
        print(f"The file {file_path} is empty.", file=sys.stderr)
    except pd.errors.ParserError as err:
        print(f"Parsing error: {err}", file=sys.stderr)
    except sqlite3.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    except Exception as err:
        print(f"Unexpected issue: {err}", file=sys.stderr)

    return 0
