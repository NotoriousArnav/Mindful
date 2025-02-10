from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader, PyPDFLoader
from langchain_core.documents.base import Document
from langchain_chroma import Chroma
from pathlib import Path
from typing import List, Optional

def find_files_with_extensions(directory: str, extensions: List[str]) -> List[Path]:
    """
    Recursively search for files with specified extensions in a given directory.

    Args:
        directory (str): The root directory to start the search from.
        extensions (List[str]): A list of file extensions to search for (e.g., ['.html', '.pdf']).

    Returns:
        List[Path]: A list of Paths to the files matching the specified extensions.
    """
    # Convert the directory to a Path object
    root_dir:Path = Path(directory)
    # Use rglob to recursively search for files with the given extensions
    matching_files:List[Path] = [file for file in root_dir.rglob('*') if file.suffix in extensions]
    return matching_files


def load_documents_from_directory(directory: str) -> List[Document]:
    """
    Load all HTML and PDF files from the specified directory and convert them into LangChain Document objects.

    Args:
        directory (str): The root directory to start the search from.

    Returns:
        List[Document]: A list of Document objects containing the content and metadata of the files.
    """
    # Define the file extensions to search for
    file_extensions:list[str] = [
            '.html', '.pdf'
    ]

    # Find all files with the specified extensions
    matching_files = find_files_with_extensions(directory, file_extensions)

    documents = []

    for file_path in matching_files:
        if file_path.suffix == '.html':
            # Load HTML file using UnstructuredHTMLLoader
            loader = UnstructuredHTMLLoader(str(file_path))
            print(f"Loaded HTML file: {file_path}")
        elif file_path.suffix == '.pdf':
            # Load PDF file using PyPDFLoader
            loader = PyPDFLoader(str(file_path))
            print(f"Loaded PDF file: {file_path}")
        else:
            continue

        # Load the document and append to the list
        loaded_docs = loader.load()
        documents.extend(loaded_docs)

    return documents


def embed_documents_in_database(directory: str, database_path: Optional[str] = None):
    """
    Load documents from a directory, generate embeddings, and store them in a Chroma database.

    Args:
        directory (str): The directory containing the HTML and PDF files.
        database_path (Optional[str]): Path to store the Chroma database. Defaults to './chroma_db'.
    """
    if database_path is None:
        database_path = './chroma_db'

    # Load documents
    documents = load_documents_from_directory(directory)

    # Initialize embeddings and Chroma DB
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_db = Chroma(
            collection_name="documents",
            embedding_function=embeddings,
            persist_directory=database_path
    )

    # Add documents to the vector DB
    vector_db.add_documents(documents)
    print(f"Successfully embedded {len(documents)} documents into the database at '{database_path}'.")

if __name__ == "__main__":
    embed_documents_in_database("evaluation_files")
