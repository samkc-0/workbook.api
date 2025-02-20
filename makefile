# Define the shell
SHELL := /bin/bash

# Define the script file
TEST_SCRIPT := test_user.sh

# Define the Python environment (if using virtualenv)
VENV := venv/bin/activate

# Run the API test script
.PHONY: test-api
test-api:
	@echo "🚀 Running API test..."
	@chmod +x $(TEST_SCRIPT)
	@./$(TEST_SCRIPT)
	@echo "✅ API test completed."

# Start Django development server
.PHONY: runserver
runserver:
	@echo "🚀 Starting Django development server..."
	@source $(VENV) && python manage.py runserver

# Run Django migrations
.PHONY: migrate
migrate:
	@echo "🚀 Running migrations..."
	@source $(VENV) && python manage.py migrate

# Create a superuser (interactive)
.PHONY: createsuperuser
createsuperuser:
	@echo "🚀 Creating superuser..."
	@source $(VENV) && python manage.py createsuperuser

# Clean up Python cache files
.PHONY: clean
clean:
	@echo "🧹 Cleaning up Python cache files..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete