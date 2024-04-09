import os
import sys
import subprocess
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def interact(input_file, output_file):
    # create user input/output file type dictioray
    compartibles = ['epub', 'doc', 'csv',
                    'docx', 'odt', 'html', 'json', 'pdf', 'txt',
                    'pptx', 'xlsx', 'xhtml', 'xml']
    try:
        logger.info("\033[33m Compartible file formart are::\033[0m", end=" ")
        for i in compartibles:
            logger.info(f"\033[35m{i}\033[0m", end=",")

        # obtain file extensions to determine file conversion types
        infilename, inextension = os.splitext(input_file)
        outfilename, outextension = os.splitext(output_file)
    except Exception as e:
        logger.error(f"\033[32m Error:{e}\033[0m")

    if inextension == outextension:
        logger.info("\033[33mSame file conversion type: No operation>\033[0m\nExiting...")
        sys.exit()
    if inextension in compartibles.lower() and outextension.lower() in compartibles:
        # Check whether running on unix-based sytem
        if os.name == 'posix':
            try:
                subprocess.run(['soffice', '--convert-to', f'{outextension}', f'{input_file}', f'{output_file}'])
                logger.info(f"\033[1;95mSuccessfully converted {input_file} to {output_file}\033[0m")
            except Exception as e:
                logger.error(f"Unable to convert {input_file} to {output_file}: {e}")
                logger.inf("Please make sure that soffice is installed in your system")
                with open("conversion.log", "a") as log_file:
                    log_file.write(f"Error converting {input_file} to {output_file}: {e}\n")
        # if the system is not unix based exit
        else:
            logger.info('This conversion only works for unix-based systems at the moment.')
            sys.exit
