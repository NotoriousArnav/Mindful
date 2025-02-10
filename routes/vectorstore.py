from fastapi import APIRouter, Depends, HTTPException
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader, PyPDFLoader
from langchain_core.documents.base import Document
from langchain_chroma import Chroma
from pathlib import Path
from typing import List, Optional
from database import db
from security import get_current_user

router = APIRouter(
    prefix="/vectorstore",
    tags=["vectorstore"],
    responses={404: {"description": "Not found"}},
)

embedding_function = OllamaEmbeddings(model="nomic-embed-text")

@router.post("/postnote/{note_id}")
async def post_vectorstore(
        note_id:str,
        user:dict = Depends(get_current_user)
    ):
    note = await db.get_note_by_id(note_id, author=user["email"])
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    vectorstore = Chroma(
        embedding_function=embedding_function,
        persist_directory="./chroma_db",
        collection_name=f"collection-{note.collection}"
    )
    
    try:
        vectorstore.add_documents(
                [
                    Document(
                        page_content=f"""{note.content.content}""",
                        metadata={
                            'note_id': note_id
                        }
                    )
                ]
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to add document to vectorstore"
        )

    return {
        "message": "Document added to vectorstore",
        "note_id": note_id
    }


@router.post("/retrieve")
async def retrieve_vectorstore(
        collection_id:str,
        prompt:str,
        user:dict = Depends(get_current_user)
    ):

    vectorstore = Chroma(
        embedding_function=embedding_function,
        persist_directory="./chroma_db",
        collection_name=f"collection-{collection_id}"
    )

    docs = vectorstore.similarity_search(
        query=prompt,
        k=5
    )

    return docs
