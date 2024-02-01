import os
import sys
import pypandoc


def interact(input_file, output_file):
    # create user input/output file type dictioray
    compartibles = ['Markdown', 'reStructuredText', 'LaTeX', 'MediaWiki',
                    'docx', 'odt', 'HTML', 'YAML', 'JSON', 'pdf', 'txt',
                    'pptx', 'xlsx']
    i = 0
    for i in compartibles:
        i += i
    try:
        print(f"\033[34m Compartible file formart are:: \033[0m{i}", end="\n")

        # obtain file extensions to determine file conversion types
        infilename, inextension = os.splitext(input_file)
        outfilename, outextension = os.splitext(output_file)
    except Exception as e:
        print(f"\033[32m Error:{e}\033[0m")

    if inextension == outextension:
        print("Same file conversion type: No operation>\nExiting...")
        sys.exit()
    if inextension in compartibles and outextension in compartibles:
        try:
            pypandoc.convert_file(f"{input_file}", f"{inextension}", outputfile=f"{output_file}")
            print(f"\033[1;95mSuccessfully converted {input_file} to {output_file}\033[0m")
        except Exception as e:
            print(f"Error:Unable to convert {input_file} to {output_file}: {e}")
            with open("conversion.log", "a") as log_file:
                log_file.write(f"Error converting {input_file} to {output_file}: {e}\n")
