import pandas as pd


def get_xlsx2csv_files(input_file, output_file):
    if os.path.isfile(input_file):
        convert_xlsx_to_csv(input_file, output_file)
    elif os.path.isdir(input_file):
        for file in os.listdir(input_file):
            if os.path.isfile(file) and file.endswith('.xlsx') or file.endswith('.xls'):
                input_file = file
                basename, ext = os.path.splitext(input_file)
                output_file = basename + '.csv'
                convert_xlsx_to_csv(input_file, output_file)
            else:
                pass


def convert_xlsx_to_csv(xlsx_file, csv_file):
    try:
        # Load the Excel file
        print(f"Loading file {xlsx_file}:>>>")
        df = pd.read_excel(xlsx_file)
        print("Converting the file::")
        # Save the DataFrame to CSV
        df.to_csv(csv_file, index=False)
        print(f"\033[1;95m Conversion successful for {xlsx_file} to {csv_file}\033[0m")
    except Exception as e:
        print(e)
