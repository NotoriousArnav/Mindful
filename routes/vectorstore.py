from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader, PyPDFLoader, WebBaseLoader
from langchain_core.documents.base import Document
from langchain_chroma import Chroma
from pathlib import Path
from typing import List, Optional
from database import db
import bs4
from llm import llm
from security import get_current_user
from io import BytesIO

router = APIRouter(
    prefix="/vectorstore",
    tags=["vectorstore"],
    responses={404: {"description": "Not found"}},
)

embedding_function = OllamaEmbeddings(model="nomic-embed-text")

@router.post("/posttext/{collection_id}")
async def post_text_vectorstore(
        collection_id:str,
        file:UploadFile,
        user:dict = Depends(get_current_user)
    ):

    vectorstore = Chroma(
        embedding_function=embedding_function,
        persist_directory="./chroma_db",
        collection_name=f"collection-{collection_id}"
    )

    if not file.content_type == "text/plain": # text
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )


    file_contents = await file.read()
    lines = file_contents.decode('utf-8').split('\n')

    
    # Upload the text file to the Database
    object_id = await db.db.files.insert_one({
        'user': user["email"],
        'collection': collection_id,
        'filename': file.filename,
        'content': file.file.read()
    })

    Metadata = {
        'collection_id': collection_id,
        'filename': file.filename,
        'object_id': str(object_id.inserted_id),
    }

    documents = [Document(
        page_content=line,
        metadata=Metadata
    ) for line in lines]
    print(documents)

    try:
        vectorstore.add_documents(documents)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to add document to vectorstore"
        )

    return {
        "message": "Document added to vectorstore",
        "collection_id": collection_id
    }

@router.post("/posturl/{collection_id}")
async def post_url_vectorstore(
        collection_id:str,
        url:str,
        bs4_strainer_args:dict,
        user:dict = Depends(get_current_user)
    ):

    vectorstore = Chroma(
        embedding_function=embedding_function,
        persist_directory="./chroma_db",
        collection_name=f"collection-{collection_id}"
    )

    loader = WebBaseLoader(
        web_paths=[url],
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                **bs4_strainer_args
            )
        )
    )
    documents = [
            [
                Document(
                    page_content=line,
                    metadata={
                        'collection_id': collection_id,
                        **doc.metadata

                    }
                )
                for line in doc.page_content.split('\n')
            ] 
            for doc in loader.load()
        ]
    
    docs = []

    for d in documents:
        docs.extend(d)

    try:
        vectorstore.add_documents(docs)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Failed to add document to vectorstore"
        )

    return {
        "message": "Document added to vectorstore",
        "collection_id": collection_id
    }

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


@router.post("/retrieve/{collection_id}")
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
        # No limit
        limit=None
    )

    return docs

@router.post("/agentask/{collection_id}")
async def askagent(
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
        # No limit
    )

    messages = [
        (
            "system",
            """You are a Intelligent AI."""
        ),
        (
            "user",
            prompt
        ),
        (
            "system",
            f"Vector DB Result: {docs}"
        ),

    ]

    result = llm.invoke(messages)
    print(result)
    return {
        "sources": docs,
        "result": result.content
    }


