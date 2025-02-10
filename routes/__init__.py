from fastapi import APIRouter
from .notes import router as notes_router
from .vectorstore import router as vectorstore_router

router = APIRouter()

router.include_router(notes_router)
router.include_router(vectorstore_router)
