# Task Manager Application

A comprehensive task management system built in Python with multiple interconnected modules.

## Project Structure

```
task_manager/
├── __init__.py          # Package initialization
├── models.py            # Data models (Task, Project, TaskStatus, TaskPriority)
├── database.py          # Database persistence layer
├── manager.py           # High-level task manager orchestrator
├── config.py            # Configuration management
├── utils.py             # Utility functions (date, validation, string operations)
├── main.py              # Application entry point with example usage
└── test_manager.py      # Unit tests
```

## Features

### Core Models
- **Task**: Represents individual tasks with properties like title, description, priority, status, and due dates
- **Project**: Groups tasks together with team member management
- **TaskStatus**: Enumeration for task states (TODO, IN_PROGRESS, COMPLETED, ARCHIVED)
- **TaskPriority**: Enumeration for task priorities (LOW, MEDIUM, HIGH, CRITICAL)

### Database Operations
- Create, read, update, and delete projects and tasks
- Persist data to JSON files
- Load/save operations with error handling

### Task Management Features
- Create and organize projects with team members
- Assign tasks to team members
- Track task status and completion
- Search tasks by keyword
- Generate project statistics (completion rate, task counts)
- Filter tasks by status, priority, and assignee

### Utilities
- **DateUtils**: Date parsing, formatting, and due date calculations
- **ValidationUtils**: Email and username validation
- **StringUtils**: String operations (truncation, slug generation, capitalization)
- **ListUtils**: List operations (chunking, flattening, deduplication)

## Installation

```bash
# No external dependencies required for basic functionality
# Install development dependencies if needed
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from task_manager import TaskManager, Database

# Initialize
db = Database("./data")
manager = TaskManager(db)
manager.set_current_user("alice")

# Create project
project = manager.create_project(
    name="My Project",
    description="Project description"
)

# Create task
task = manager.create_task(
    title="My Task",
    description="Task description",
    project_id=project.id,
    priority=TaskPriority.HIGH
)

# Manage tasks
manager.complete_task(task.id)
manager.assign_task(task.id, "bob")

# Get statistics
stats = manager.get_project_stats(project.id)
print(f"Completion: {stats['completion_percentage']}%")
```

### Run Example Application

```bash
python task_manager/main.py
```

### Run Tests

```bash
python -m unittest task_manager/test_manager.py
```

## Configuration

The application supports multiple environments:
- **Development**: Debug enabled, local data directory
- **Testing**: Notifications disabled, test data directory
- **Production**: Debug disabled, system data directory

```python
from task_manager.config import get_config

config = get_config("development")
```

## API Overview

### TaskManager Methods
- `create_project(name, description, owner)`: Create new project
- `create_task(title, description, project_id, priority)`: Create new task
- `get_my_projects()`: Get current user's projects
- `get_my_tasks()`: Get current user's tasks
- `get_high_priority_tasks()`: Get urgent tasks
- `get_overdue_tasks()`: Get tasks past due date
- `complete_task(task_id)`: Mark task as completed
- `assign_task(task_id, user_name)`: Assign task to user
- `get_project_stats(project_id)`: Get project statistics
- `search_tasks(keyword)`: Search by keyword

## Testing

Comprehensive unit tests included for:
- Task and Project models
- Database operations
- Task Manager functionality
- Utility functions

Run tests with:
```bash
python -m unittest task_manager/test_manager.py -v
```

## License

MIT License

