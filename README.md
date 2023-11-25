# fconverter
A python file conversion tool 
`This is a Linux command-line interface (CLI) application that coverts documents from one format to another.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/sky-cyber/fconverter
   ```

2. Navigate to the project directory:

   ```shell
   cd fconverter
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```
4.Install the package:
   ```shell
   pip install .
   ```
   

## Usage

To run the CLI app, use the following command:

```shell
fconverter [options] stdin stdout
```

Replace `[options]` with the appropriate command-line options based on the functionality you want to execute.

## Available Options

- `1`: Word to PDF.
- `2`: PDF to Word.
- `3`: Word to PPT.
- `4`: Word to TXT.
- `5`: PDF to TXT.
- `6`: PPT to Word
- `7`: TXT to Word
## Examples

1. Example command 1:

   ```shell
   fconverter 1 example.docx example.pdf
   ```

  This promt parses 1 as the operation and example.docx as the file(stdin) to be converted to example.pdf (stdout)

Note that to run undertake any conversion you must be in the directory where file to be converted is located, otherwise you definetely sahall encounter an error

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is an open source software.


Feel free to modify and customize this template according to your specific project requirements and add any additional sections or information that you think would be helpful for users.

