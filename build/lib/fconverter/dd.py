import subprocess
import sys
import os

if os.name == 'posix':  # Check if running on Linux
    # Use subprocess to run the dpkg and grep commands
    result = subprocess.run(['dpkg', '-l', 'libreoffice'], stdout=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Please install libreoffice to use this functionality !")
        sys.exit(1)
