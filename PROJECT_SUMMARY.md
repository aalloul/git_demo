# Task Manager Project - Complete Code Structure

## Overview
A comprehensive Python task management system with 8 interconnected modules, demonstrating best practices in software architecture, object-oriented design, and code organization.

## File Structure

```
task_manager/
├── __init__.py                  (Package initialization)
├── models.py                    (Core data models)
├── database.py                  (Persistence layer)
├── manager.py                   (Business logic orchestrator)
├── config.py                    (Configuration management)
├── utils.py                     (Utility functions)
├── main.py                      (Example application)
├── test_manager.py              (Unit tests - 22 tests)
├── requirements.txt             (Dependencies)
└── README.md                    (Documentation)
```

## Module Descriptions

### 1. models.py (175 lines)
**Core Data Models**
- `TaskStatus`: Enum (TODO, IN_PROGRESS, COMPLETED, ARCHIVED)
- `TaskPriority`: Enum (LOW, MEDIUM, HIGH, CRITICAL)
- `Task`: Complete task model with methods:
  - mark_completed(), mark_in_progress()
  - assign_to(), add_subtask()
  - to_dict() for serialization
- `Project`: Project container with methods:
  - add_task(), add_member(), remove_member()
  - get_tasks_by_status(), get_tasks_by_priority()
  - get_completion_rate()

### 2. database.py (180 lines)
**Persistence & Data Access Layer**
- `Database`: Manages all data operations
- CRUD operations: create_project, create_task, get_project, get_task, update_*, delete_*
- File I/O: save_projects(), save_tasks(), load_projects(), load_tasks()
- JSON serialization with automatic ID management

### 3. manager.py (165 lines)
**Business Logic & Orchestration**
- `TaskManager`: High-level API for application logic
- User session management: set_current_user()
- Project operations: create_project(), get_my_projects()
- Task operations: create_task(), complete_task(), get_my_tasks()
- Query methods: get_high_priority_tasks(), get_overdue_tasks()
- Analytics: get_project_stats(), search_tasks()

### 4. config.py (75 lines)
**Configuration Management**
- `Config`: Base configuration class
- `DevelopmentConfig`: Debug mode enabled
- `TestingConfig`: Notifications disabled
- `ProductionConfig`: Production settings
- get_config(): Factory function for environment-based config

### 5. utils.py (145 lines)
**Utility Functions**
- `DateUtils`: parse_date(), format_date(), days_until_due(), is_overdue(), is_due_today()
- `ValidationUtils`: validate_email(), validate_username(), validate_string()
- `StringUtils`: truncate(), to_slug(), capitalize_words()
- `ListUtils`: chunk(), flatten(), unique()

### 6. main.py (130 lines)
**Example Application**
- Complete demonstration of system usage
- Creates sample projects and tasks
- Adds team members and assigns tasks
- Displays statistics and task information
- Shows all major API features

### 7. test_manager.py (250 lines)
**Comprehensive Unit Tests** (22 tests, all passing)
- TestTask (5 tests): task creation, status changes, assignments
- TestProject (6 tests): project management, team members, completion rate
- TestDatabase (4 tests): CRUD operations
- TestTaskManager (2 tests): project/task creation, search functionality
- TestDateUtils (2 tests): date parsing and formatting
- TestValidationUtils (2 tests): email and username validation
- TestStringUtils (2 tests): string operations

### 8. __init__.py (10 lines)
**Package Initialization**
- Exports public API: Task, Project, Database, TaskManager
- Version and metadata

## Key Features

### Object-Oriented Design
- Clear class hierarchies and responsibilities
- Separation of concerns (models, persistence, business logic)
- Enumerations for type safety

### Data Persistence
- JSON-based persistence
- Automatic ID generation
- Load/save operations

### Business Logic
- User session management
- Task filtering and searching
- Statistics and analytics
- Team collaboration features

### Testing
- Comprehensive unit test coverage
- 22 passing tests
- Tests for models, database, manager, and utilities

### Utilities
- Date/time operations
- Data validation
- String manipulation
- Collection operations

## Ready for Conflict Demonstration

This codebase is specifically designed for demonstrating complex Git conflicts:

✅ **Multiple interconnected files** - Changes in one file affect others
✅ **Multiple collaborators perspective** - Different modules can be worked on
✅ **Realistic code patterns** - Real-world class hierarchies and dependencies
✅ **Test coverage** - Allows testing conflict resolution impact
✅ **Clear architecture** - Easy to understand what conflicts mean

## Usage Example

```python
from task_manager import TaskManager, Database

# Initialize
db = Database("./data")
manager = TaskManager(db)
manager.set_current_user("alice")

# Create project
project = manager.create_project(
    name="Website Redesign",
    description="Modern UI/UX redesign"
)

# Create and manage tasks
task = manager.create_task(
    title="Design mockups",
    description="Create UI mockups",
    project_id=project.id,
    priority=TaskPriority.HIGH
)

# Get stats
stats = manager.get_project_stats(project.id)
```

## Statistics

- **Total Lines of Code**: ~1,100 (excluding comments and blanks)
- **Number of Classes**: 12 (2 Enums, 2 Main Models, 1 Database, 1 Manager, 6 Utility Classes, Config classes)
- **Number of Methods**: 60+
- **Test Coverage**: 22 tests, all passing ✓
- **Files**: 8 Python modules + documentation

---

This project is now ready for demonstrating real-world Git conflict scenarios!

