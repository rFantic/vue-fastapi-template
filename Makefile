VENV=.venv

.PHONY: install-frontend build-frontend run clean help

help:
	@echo "Targets:"
	@echo "  install-frontend  Install front-end npm deps (in front-end/)"
	@echo "  build-frontend    Build front-end with vite into front-end/dist"
	@echo "  run               Build (if needed) and run the FastAPI app with uvicorn"
	@echo "  clean             Remove build artifacts"

install-frontend:
	cd front-end && npm install

build-frontend:
	cd front-end && npm run build

run: build-frontend
	uv run fastapi dev

clean:
	rm -rf front-end/dist
	rm -rf ${VENV}
