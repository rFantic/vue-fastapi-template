from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="medical-crawl static host")

DIST_DIR = os.path.join(os.path.dirname(__file__), ".", "front-end", "dist")
DIST_DIR = os.path.normpath(DIST_DIR)

if os.path.isdir(DIST_DIR):
    app.mount("/", StaticFiles(directory=DIST_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
else:
    @app.get("/")
    def not_built():
        return {"error": "frontend not built yet. Run `npm run build` inside front-end to generate dist."}
