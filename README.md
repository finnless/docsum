# Document Summarizer - docsum - WIP -  [![](https://github.com/finnless/docsum/workflows/tests/badge.svg)](https://github.com/finnless/docsum/actions/workflows/tests.yml)
## Overview

`docsum.py` is a Python script designed to summarize the content of any given file using a language model API. The script reads the text from the specified file, sends it to the Groq API, and prints a concise summary of the content.

## Requirements

This script is designed to work with **Python 3.11 and below**. Ensure you have Python installed on your machine before proceeding.

### Dependencies

Before running the script, install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

The `libmagic` library is required to run this script. If you encounter an error related to `libmagic`, you can follow these steps based on your operating system:

#### For Ubuntu/Debian:
Install the `libmagic` library:
```bash
sudo apt-get install libmagic1
```

#### For macOS:
Install `libmagic` using Homebrew:
```bash
brew install libmagic
```

## Usage

1. **Prepare the Environment:**
   
   Before running the script, ensure that you have set up your environment variables correctly. You will need to have a `.env` file in the same directory as your script containing your `GROQ_API_KEY`.

   Example `.env` file:

   ```
   GROQ_API_KEY=your_api_key_here
   ```

2. **Run the Script:**

   To summarize a file, use the following command in your terminal:

   ```bash
   python docsum.py <path_to_file>
   ```

   Replace `<path_to_file>` with the path to the file you want to summarize.

   Example:

   ```bash
   python docsum.py example.txt
   ```

3. **Output:**

   The script will print the summarized content of the file directly to the terminal.


## Error Handling

If the specified file cannot be loaded, the script will output an error message and terminate with an exit code of `1`:

```
File "<filename>" could not be loaded. Does the file exist?
```

The exit code `1` indicates that there was an error in opening the file. Ensure that the file path is correct and the file is accessible. If the issue persists, double-check the file permissions and the validity of the file path.


## License

This project is licensed under the MIT License.


