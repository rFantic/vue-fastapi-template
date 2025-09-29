VENV=.venv
PYTHON=${VENV}/bin/python
PIP=${VENV}/bin/pip

.PHONY: install-backend install-frontend build-frontend run dev clean help

help:
	@echo "Targets:"
	@echo "  install-backend   Create virtualenv and install Python deps"
	@echo "  install-frontend  Install front-end npm deps (in front-end/)"
	@echo "  build-frontend    Build front-end with vite into front-end/dist"
	@echo "  run               Build (if needed) and run the FastAPI app with uvicorn"
	@echo "  dev               Run frontend dev server and backend separately for dev"
	@echo "  clean             Remove build artifacts"

# Python backend env
install-backend:
	python3 -m venv ${VENV}
	${PIP} install --upgrade pip
	${PIP} install -r backend/requirements.txt

install-frontend:
	cd front-end && npm install

build-frontend:
	cd front-end && npm run build

run: build-frontend
	# Run uvicorn pointing at backend.app:app
	${PYTHON} -m uvicorn backend.app:app --host 0.0.0.0 --port 8000

dev:
	@echo "Start frontend dev server (port 5173) and backend uvicorn (8000) in separate terminals"
	@echo "Run `cd front-end && npm run dev` in one terminal and `make install-backend && ${PYTHON} -m uvicorn backend.app:app --reload` in another."

clean:
	rm -rf front-end/dist
	rm -rf ${VENV}
