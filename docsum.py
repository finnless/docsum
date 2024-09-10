import os
import argparse
import chardet
from dotenv import load_dotenv
import fulltext
from groq import Groq
import magic
import re
import sys


load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def summarize(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Please summarize the following text in a few paragraphs.",
            },
            {
                "role": "user",
                "content": text,
            },
            {
                "role": "assistant",
                "content": "Here is a summary of the text:\n\n",
            },
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def find_split_point(subtext, max_length, separators):
    """
    Find the best split point in the text based on the given separators and max_length.

    Parameters:
        subtext (str): The input text to be split.
        max_length (int): The maximum allowed length of each chunk.
        separators (list): A list of regular expressions for valid split points.

    Returns:
        int: The index of the best split point, or None if no valid split point is found.
    """
    for sep in separators:
        matches = [m.start() for m in re.finditer(sep, subtext)]
        valid_splits = [i for i in matches if i < max_length]
        if valid_splits:
            return valid_splits[-1]  # Return the last valid split point

    return None


def split_docs(text, max_length=10000):
    '''
    Split input text into smaller chunks so that an LLM can process. 
    Splits around every 10,000 characters. Splits on what appears to be new sections 
    by finding section separators in order of preference: newlines and periods.
    
    Parameters:
        text (str): The input text to be split.
        max_length (int): Maximum length of each chunk (default is 10,000 characters).
    
    Returns:
        list: A list of split text chunks.
    '''
    
    separators = [r"\n", r"\. "]  # Handling newlines and periods

    def split_once(subtext):
        """
        Split the text once, at the best split point, if possible.
        Returns a list of one or two chunks.
        """
        print(f"Processing: {subtext[:30]}... (length: {len(subtext)})")
        
        if len(subtext) <= max_length:
            print(f"Returning chunk: {subtext}")
            return [subtext]

        # Find the best place to split
        split_point = find_split_point(subtext, max_length, separators)

        if split_point is not None:
            # Handle newlines
            if subtext[split_point] == '\n':
                # Find the end of the next line
                next_newline = subtext.find('\n', split_point + 1)
                if next_newline != -1 and next_newline - split_point <= max_length:
                    split_point = next_newline  # Extend to include the next line
            
            # Handle periods: Extend to the end of the sentence (after the period)
            elif subtext[split_point:split_point+2] == '. ':
                next_period = subtext.find('. ', split_point + 1)
                if next_period != -1 and next_period - split_point <= max_length:
                    split_point = next_period + 2  # Include the full sentence after period

            print(f"Splitting at index {split_point}: {subtext[:split_point]} | {subtext[split_point:]}")
            # Split at the best point found, return two chunks only
            return [subtext[:split_point].strip(), subtext[split_point:].strip()]
        
        # Fallback to hard split at max_length if no valid split point is found
        print(f"Hard splitting at {max_length}: {subtext[:max_length]} | {subtext[max_length:]}")
        return [subtext[:max_length].strip()] + split_once(subtext[max_length:].strip())

    return split_once(text)


def extract_text(filename):
    """
    A function that extracts text given a filepath
    """
    # Use python-magic to detect the MIME type based on file content
    # This is to avoid sending text files to fulltext because it strips
    # newlines which may be needed downstream
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(filename)

    # Detect the encoding of the file
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
        charenc = result['encoding']

    # Process based on MIME type
    if mime_type.startswith('text'):
        # If the file is raw text
        with open(filename, 'r', encoding=charenc) as f:
            content = f.read()
    else:
        # If the file is not raw text
        with open(filename, 'r', encoding=charenc) as f:
            content = fulltext.get(f, None, name=filename)

    return content


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Summarize any file.")
    parser.add_argument(
        'filename',
        help='Path to the file to summarize.'
    )
    args = parser.parse_args()

    if args.filename:
        file_text = extract_text(args.filename)
        if not file_text:
            print(f'File "{args.filename}" could not be loaded. Does the file exist?')
            sys.exit(1)


    # TODO: Handle large documents

    # if len(file_text) > 20,000:


    print(summarize(file_text))

