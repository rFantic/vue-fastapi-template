Development README

This project contains a Vite front-end in `front-end/` and a small FastAPI backend in `backend/` that serves the built `front-end/dist` directory.

Quick start (Linux/macOS):

1) Install backend Python deps and frontend npm deps:

   make install-backend
   make install-frontend

2) Build the frontend into `front-end/dist`:

   make build-frontend

3) Run the backend (it will serve the built dist):

   make run

Dev mode (run frontend dev server and backend reload):

- In one terminal run:

  cd front-end && npm run dev

- In another terminal run:

  make install-backend
  .venv/bin/python -m uvicorn backend.app:app --reload --port 8000

Notes:
- The backend expects `front-end/dist/index.html` to exist for production serving.
- If you change the frontend, re-run `make build-frontend` before `make run` or use the dev flow above.
