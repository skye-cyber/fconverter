import pandas as pd


def convert_xlsx_to_csv(xlsx_file, csv_file):
    # Load the Excel file
    print(f"Loading file {xlsx_file}:>>>")
    df = pd.read_excel(xlsx_file)
    print("Converting the file::")
    # Save the DataFrame to CSV
    df.to_csv(csv_file, index=False)
    print(f"\033[1;95m Conversion successful for {xlsx_file} to {csv_file}\033[0m")
