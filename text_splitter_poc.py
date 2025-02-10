import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load your text file
file_path = 'path/to/your/textfile.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Number of characters per chunk
    chunk_overlap=150,  # Number of overlapping characters between chunks
    separators=["\n\n", "\n", " ", ""]
)

# Split the text into chunks
chunks = text_splitter.split_text(text)

# Display the number of chunks and the first chunk as an example
print(f"Number of chunks created: {len(chunks)}")
print(f"First chunk:\n{chunks[0]}")

