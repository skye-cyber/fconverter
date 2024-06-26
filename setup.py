from setuptools import setup

setup(
    name='fconverter',
    version='1.5',
    author="Wambua aka Bullet Angel",
    packages=["fconverter"],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            "fconverter=fconverter:main"],
    },
    python_requires='>=3.6',
    install_requires=[
        'argparse',
        'pdfminer.six',
        'python-docx',
        'python-pptx',
        'gTTS',
        'pypandoc',
        'pydub',
        'requests',
        'Pillow',
        'pandas',
        'opencv-python',
        'pytesseract',
        'PyPDF2',
        'requests'
        # 'ffmpeg'
    ],
    include_package_data=True,
    license="MIT",
    keywords=['fconverter', "file-conversion"],
    classifiers=[
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPi",
    ],
)
