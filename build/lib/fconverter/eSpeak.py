import subprocess


def text_to_mp3_fallback(text_file, mp3_file):
    try:
        # Function to check if a command is available
        print('''Checking requirements:espeak &&
                                        ffmpeg''')
        command = ['espeak', 'ffmpeg']
        for _ in command:
            try:
                print(f'''Checking availability of{command}>>''')
                subprocess.check_output([command, "--version"], stderr=subprocess.DEVNULL)
                return True
            except Exception as e:
                print(f"{e}")
            return False
        if True:
            text_file = input("enter text file:")    # Specify the input text file
            # Convert text to speech using eSpeak
            output_wav = "output.wav"
            espeak_command = f"espeak -f {text_file} -w {output_wav}"
            subprocess.run(espeak_command, shell=True)

            # Convert WAV to MP3 using FFmpeg
            mp3_file = "output.mp3"
            ffmpeg_command = f"ffmpeg -i {output_wav} {mp3_file}"
            subprocess.run(ffmpeg_command, shell=True)
            print("Conversion completed!")
        else:
            print('''Either of the packages is missing:\n
            please run:
            >>>sudo apt-get install espeak && sudo apt-get install ffmpeg''')
    except Exception as e:
        print(f"Requested operation faile:\n{e}")
