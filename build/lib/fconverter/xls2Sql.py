import pandas as pd
import sqlite3


def get_word2pdf_files(input_file, output_file):
    if os.path.isfile(input_file):
        convert_xlsx_to_database(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            if os.path.isfile(file) and file.endswith('.xlsx') or file.endswith('.xls'):
                input_file = file
                basename, ext = os.path.splitext(input_file)
                output_file = basename + '.sql'
                convert_xlsx_to_database(input_file, output_file)
            else:
                pass


def convert_xlsx_to_database(xlsx_file, db_file, table_name):
    # Read the Excel file into a pandas DataFrame
    print(f"Reading {xlsx_file}...")
    df = pd.read_excel(xlsx_file)
    print("Initializing conversion procedure>>>")
    print("Connected to sqlite3 database::")
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file)
    print("Creating database table::\n")
    # Insert the DataFrame into a new table in the database
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Successfully converted \033[32m{xlsx_file}\033[0m to \033[32{db_file}\033[0m")
    # Close the database connection
    conn.close()
