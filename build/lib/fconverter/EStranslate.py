import os
from googletrans import Translator


def translate_book(input_file, output_file):
    # Create a translator object
    translator = Translator(service_urls=['translate.google.com'])

    try:
        # Get the total number of characters in the input file
        total_chars = os.path.getsize(input_file)

        # Open the input file for reading
        with open(input_file, 'r', encoding='utf-8') as file:
            # Read the content of the input file
            content = file.read()

            # Initialize the translated content
            translated_content = ""

            # Initialize the progress counter
            progress = 0

            # Translate the content to Kiswahili
            for i, char in enumerate(content):
                # Translate each character
                translated_char = translator.translate(char, dest='sw').text

                # Append the translated character to the translated content
                translated_content += translated_char

                # Update the progress counter
                progress = (i + 1) / total_chars * 100

                # Print the progress
                print(f"Progress: {progress:.2f}%\r", end='')

            # Open the output file for writing
            with open(output_file, 'w', encoding='utf-8') as output:
                # Write the translated content to the output file
                output.write(translated_content)
        print("\nTranslation completed successfully!")
        print(f"Translated content::>{translated_content}")

    except FileNotFoundError:
        print("Input file not found!")

    except Exception as e:
        print("An error occurred during translation:", str(e))


# Specify the input and output file paths
input_file = input("Enter file with the text to be translated:>>")
output_file = input("Enter ouput file name>> ")

# Call the translate_book function
translate_book(input_file, output_file)
