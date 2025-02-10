#!/usr/bin/env python3
import uvicorn
from dotenv import load_dotenv
from main import app

load_dotenv()
import os

if __name__ == "__main__":
    uvicorn.run(
            app,
            host="0.0.0.0",
            port=os.getenv("MINDFUL_SERVER_PORT", 8000),
            reload=os.getenv("MINDFUL_SERVER_RELOAD", True),
    )
