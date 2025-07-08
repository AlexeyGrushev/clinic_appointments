up:
	@echo "Starting services..."
	docker compose up -d --build

down:
	@echo "Stopping services..."
	docker compose down

lint:
	@echo "Checking linting and formatting..."
	flake8 app/ && black --check app/ && isort --check-only app/

format:
	@echo "Formatting code..."
	black app/ && isort app/

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