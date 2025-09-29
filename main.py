from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from routes import router as api_router

app = FastAPI(title="medical-crawl static host")

DIST_DIR = os.path.join(os.path.dirname(__file__), ".", "front-end", "dist")
DIST_DIR = os.path.normpath(DIST_DIR)

app.include_router(api_router, prefix="/api", tags=["api"])
app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="static")