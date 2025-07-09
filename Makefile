up:
	@echo "Starting services..."
	docker compose --env-file .env up -d --build

down:
	@echo "Stopping services..."
	docker compose down

lint:
	@echo "Checking linting and formatting..."
	flake8 app/ && black --check app/ && isort --check-only app/

format:
	@echo "Formatting code..."
	black app/ && isort app/

test:
	@echo "Launching tests..."
	python3 -m pytest --cov=app --cov-report=term tests/ -v

makemigrations:
ifeq ($(msg),)
	$(error Please provide a message with 'msg="..."')
endif
	@echo "Creating database migrations..."
	alembic revision --autogenerate -m "$(msg)"

migrate:
	@echo "Running database migrations..."
	alembic upgrade head

healthcheck:
	@echo "Checking service up..."
	curl -f http://localhost:8000/health || exit 1

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache

req:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

req-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

req-del:
	@echo "Removing dependencies..."
	pip uninstall -r requirements-dev.txt -y
