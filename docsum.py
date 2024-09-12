import os
import argparse
import chardet
from dotenv import load_dotenv
import fulltext
from groq import Groq
import magic
import re
import sys
from typing import List, Optional



load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def summarize(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Please summarize the following text in a paragraphs.",
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



def _split_docs_with_separator(text: str, separator: str) -> List[str]:
    """
    Split the text using the given separator.

    Args:
        text (str): The text to split.
        separator (str): The character or string used as the separator.

    Returns:
        List[str]: A list of text chunks where each chunk includes the separator.
    """
    # If the separator is not empty, split the text by the separator while keeping it.
    if separator:
        # re.split captures the separator in parentheses, so we can re-attach it to chunks.
        splits = re.split(f"({re.escape(separator)})", text)
        # Combine each chunk with the following separator.
        chunks = [splits[i] + splits[i + 1] for i in range(0, len(splits) - 1, 2)]
        # If there's an odd number of splits, add the last chunk
        if len(splits) % 2 != 0:
            chunks.append(splits[-1])
        return chunks
    else:
        # If no separator is provided, split by individual characters.
        return list(text)

def _merge_splits(splits: List[str], chunk_size: int) -> List[str]:
    """
    Merge text splits into chunks of the specified size.

    Args:
        splits (List[str]): A list of text segments.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        List[str]: A list of chunks, each of size less than or equal to the chunk size.
    """
    docs = []
    current_doc = []  # Holds the current chunk
    total_length = 0  # Tracks the total length of the current chunk

    for s in splits:
        s_len = len(s)
        # If adding the next segment would exceed the chunk size, save the current chunk.
        if total_length + s_len > chunk_size:
            if current_doc:
                # Join the current chunk and append it to the list of documents.
                docs.append(''.join(current_doc))
                current_doc = []  # Reset for the next chunk
                total_length = 0  # Reset length counter

        # Add the current segment to the chunk
        current_doc.append(s)
        total_length += s_len

    # Add the last chunk if it exists
    if current_doc:
        docs.append(''.join(current_doc))

    return docs

def _merge_small_chunks(chunks: List[str], chunk_size: int) -> List[str]:
    """
    Merge smaller chunks with the previous chunk if the combined size is within the chunk size limit.
    Note: Kind of ugly, but hopefully it works.

    Args:
        chunks (List[str]): A list of text chunks.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        List[str]: A list of merged chunks.
    """
    merged_chunks = []
    current_chunk = ""

    for chunk in chunks:
        if len(current_chunk) + len(chunk) <= chunk_size:
            current_chunk += chunk
        else:
            if current_chunk:
                merged_chunks.append(current_chunk)
            current_chunk = chunk

    if current_chunk:
        merged_chunks.append(current_chunk)

    return merged_chunks

def split_docs(text: str, chunk_size: int = 4000, separators: List[str] = None) -> List[str]:
    """
    Recursively split the text into chunks using the provided separators and chunk size.

    Args:
        text (str): The text to split.
        chunk_size (int): The maximum size of each chunk.
        separators (List[str]): A list of separators to split the text. The function will
                                try the separators in order until the text is split.

    Returns:
        List[str]: A list of text chunks, each no longer than the specified chunk size.
    Note: This function and its helpers draws upon the architecture of the
        langchain-text-splitters module which I contribute to.
    """
    default_separators=[
        "\n\n\n\n\n",
        "\n\n\n\n",
        "\n\n\n",
        "\n\n",
        "\n",
        ". ",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ]

    separators = separators or default_separators
    final_chunks = []  # Holds the final chunks of text
    separator = separators[-1]  # Default separator to use if none of the others work

    # Try each separator in order to find one that can split the text
    for i, sep in enumerate(separators):
        if sep == "":  # If empty string is reached, just split by individual characters
            separator = sep
            break
        if sep in text:  # If the separator exists in the text, use it
            separator = sep
            # Set new_separators to all separators after the current one, for recursive use
            new_separators = separators[i + 1:]
            break
    else:
        # If no separator is found, fall back to splitting by characters
        new_separators = []

    # Split the text using the chosen separator
    splits = _split_docs_with_separator(text, separator)

    good_splits = []  # Collect splits that are less than the chunk size
    for s in splits:
        # If a split is smaller than the chunk size, collect it
        if len(s) < chunk_size:
            good_splits.append(s)
        else:
            # If we have collected smaller chunks, merge and append them
            if good_splits:
                final_chunks.extend(_merge_splits(good_splits, chunk_size))
                good_splits = []

            # If the current split is too large, recursively split it using the next separators
            if not new_separators:
                final_chunks.append(s)  # If no more separators, add it as is
            else:
                final_chunks.extend(split_docs(s, chunk_size, new_separators))

    # Merge and append any remaining small chunks
    if good_splits:
        final_chunks.extend(_merge_splits(good_splits, chunk_size))

    # Post-process to merge small chunks
    final_chunks = _merge_small_chunks(final_chunks, chunk_size)

    return final_chunks


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

    if len(file_text) > 20000:
        # Split the document into chunks
        chunks = split_docs(file_text, chunk_size=20000)
        
        # Print the number of chunks
        print(f'Number of chunks: {len(chunks)}')
        
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            print(f'Chunk {i}/{len(chunks)}')
            summary = summarize(chunk)
            print(summary)
            chunk_summaries.append(summary)
        
        # Join the summaries of each chunk
        joined_summaries = " ".join(chunk_summaries)
        print(f'Size of joined summaries: {len(joined_summaries)} characters')
        
        # Summarize the joined summaries
        final_summary = summarize(joined_summaries)
        
        # Print the final summary
        print(final_summary)

    else:
        print(summarize(file_text))