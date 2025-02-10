from fastapi import APIRouter, Depends, HTTPException
from database import db
from security import get_current_user
from schemas import *
from pprint import pprint
from bson import ObjectId

router = APIRouter()

# Notes

@router.get("/notes", response_model=list[NoteFetch])
async def get_notes(current_user: dict = Depends(get_current_user)):
    return await db.get_notes(author=current_user["email"])

@router.get("/notes/{collection_id}")
async def get_notes_by_collection(collection_id: str, current_user: dict = Depends(get_current_user)):
    __import__('pprint').pprint("Collection ID: " + collection_id)
    return await db.get_notes(collection=collection_id, author=current_user["email"])

@router.get('/notes/{note_id}', response_model=NoteFetch)
async def get_note(note_id: str, current_user: dict = Depends(get_current_user)):
    __import__('pprint').pprint("Note ID: " + note_id)
    data = await db.get_note_by_id(note_id, author=current_user["email"])
    pprint(current_user)
    pprint(data)
    return data

@router.post("/notes")
async def create_note(note_data: Note, current_user: dict = Depends(get_current_user)):
    note_data = NoteCreate(**note_data.model_dump(), author=current_user["email"])
    return await db.insert_note(note_data)

@router.put("/notes/{note_id}")
async def update_note(note_id: str, note_data: Note, current_user: dict = Depends(get_current_user)):
    note_data = NoteCreate(**note_data.model_dump(), author=current_user["email"])
    return await db.update_note(note_id, note_data)

@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.delete_note(note_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully", "note_id": note_id}

# Collections
@router.get("/collections", response_model=list[NoteCollectionFetch])
async def get_collections(current_user: dict = Depends(get_current_user)):
    return await db.get_collections(author=current_user["email"])

@router.get('/collections/{collection_id}', response_model=NoteCollectionFetch)
async def get_collection(collection_id: str, current_user: dict = Depends(get_current_user)):
    return await db.get_collection_by_id(collection_id, author=current_user["email"])

@router.post("/collections")
async def create_collection(collection_data: AbsNoteCollection, current_user: dict = Depends(get_current_user)):
    collection_data = NoteCollectionCreate(**collection_data.model_dump(), author=current_user["email"])
    return await db.insert_collection(collection_data)

@router.put("/collections/{collection_id}")
async def update_collection(collection_id: str, collection_data: NoteCollectionCreate, current_user: dict = Depends(get_current_user)):
    collection_data = NoteCollectionCreate(**collection_data.model_dump(), author=current_user["email"])
    return await db.update_collection(collection_id, collection_data)

@router.delete("/collections/{collection_id}")
async def delete_collection(collection_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.delete_collection(collection_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"message": "Collection deleted successfully", "collection_id": collection_id}
