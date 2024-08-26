import os
import argparse
from dotenv import load_dotenv
import fulltext
from groq import Groq
import sys




parser = argparse.ArgumentParser(description="Summarize any file.")
parser.add_argument(
    'filename',
    help='Path to the file to summarize.'
)
args = parser.parse_args()

if args.filename:
    file_text = fulltext.get(args.filename, None)
    if not file_text:
        print(f'File "{args.filename}" could not be loaded. Does the file exist?')
        sys.exit(1)


load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Please summarize the following text in a few paragraphs.",
        },
        {
            "role": "user",
            "content": file_text,
        },
        {
            "role": "assistant",
            "content": "Here is a summary of the text:\n\n",
        },
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)
