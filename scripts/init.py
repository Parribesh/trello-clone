import os


def create_file(file_path, content=""):
    """Creates a file with optional content."""
    with open(file_path, "w") as f:
        f.write(content)


def create_folder_structure(base_dir):
    """Creates the backend folder structure."""

    # Base directories
    folders = [
        "app",
        "app/api",
        "app/models",
        "app/services",
        "app/utils",
        "app/config",
        "app/schemas",
        "app/tests",
        "app/middlewares",
        "app/db",
        "app/websockets",
        "logs"
    ]

    for folder in folders:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    # Placeholder files
    files = {
        "app/__init__.py": "# Initialize the app module",
        "app/api/__init__.py": "# Initialize the API module",
        "app/api/routes.py": "# Define your API routes here",
        "app/models/__init__.py": "# Initialize the models module",
        "app/models/models.py": "# Define database models here",
        "app/services/__init__.py": "# Initialize the services module",
        "app/services/board_service.py": "# Service logic for boards",
        "app/services/task_service.py": "# Service logic for tasks",
        "app/utils/__init__.py": "# Initialize the utils module",
        "app/utils/helpers.py": "# Helper functions",
        "app/config/__init__.py": "# Initialize the config module",
        "app/config/settings.py": "# Configuration settings",
        "app/schemas/__init__.py": "# Initialize the schemas module",
        "app/schemas/board_schema.py": "# Pydantic schemas for boards",
        "app/schemas/task_schema.py": "# Pydantic schemas for tasks",
        "app/tests/__init__.py": "# Initialize the tests module",
        "app/tests/test_routes.py": "# Write tests for routes",
        "app/middlewares/__init__.py": "# Initialize the middlewares module",
        "app/middlewares/auth_middleware.py": "# Authentication middleware",
        "app/db/__init__.py": "# Initialize the DB module",
        "app/db/database.py": "# Database connection logic",
        "app/websockets/__init__.py": "# Initialize the WebSocket module",
        "app/websockets/connection_manager.py": "# WebSocket connection management",
        "logs/.gitkeep": "# Placeholder to ensure logs folder is in version control",
    }

    for file, content in files.items():
        create_file(os.path.join(base_dir, file), content)


if __name__ == "__main__":
    base_directory = input(
        "Enter the base directory for your backend project: ").strip()
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    create_folder_structure(base_directory)
    print(f"Backend folder structure created in: {base_directory}")
