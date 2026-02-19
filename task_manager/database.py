"""Database module for persisting task and project data."""

import json
import os
from typing import List, Optional, Dict, Any
from .models import Task, Project, TaskStatus, TaskPriority
from datetime import datetime


class Database:
    """Manages persistence of tasks and projects to JSON files."""

    def __init__(self, data_dir: str = "./data"):
        """Initialize the database with a data directory."""
        self.data_dir = data_dir
        self.projects_file = os.path.join(data_dir, "projects.json")
        self.tasks_file = os.path.join(data_dir, "tasks.json")
        self._ensure_data_dir()
        self.projects: Dict[int, Project] = {}
        self.tasks: Dict[int, Task] = {}
        self._next_project_id = 1
        self._next_task_id = 1

    def _ensure_data_dir(self) -> None:
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)

    def create_project(
        self,
        name: str,
        description: str,
        owner: str
    ) -> Project:
        """Create and store a new project."""
        project = Project(
            name=name,
            description=description,
            owner=owner,
            project_id=self._next_project_id
        )
        self.projects[project.id] = project
        self._next_project_id += 1
        self.save_projects()
        return project

    def create_task(
        self,
        title: str,
        description: str,
        project_id: int,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> Optional[Task]:
        """Create and store a new task."""
        if project_id not in self.projects:
            return None

        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            priority=priority,
            task_id=self._next_task_id
        )
        self.tasks[task.id] = task
        self.projects[project_id].add_task(task)
        self._next_task_id += 1
        self.save_tasks()
        return task

    def get_project(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by ID."""
        return self.projects.get(project_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID."""
        return self.tasks.get(task_id)

    def get_all_projects(self) -> List[Project]:
        """Get all projects."""
        return list(self.projects.values())

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())

    def update_project(self, project_id: int, **kwargs) -> Optional[Project]:
        """Update project fields."""
        project = self.get_project(project_id)
        if not project:
            return None

        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)

        self.save_projects()
        return project

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task fields."""
        task = self.get_task(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key) and key != 'id':
                setattr(task, key, value)

        self.save_tasks()
        return task

    def delete_project(self, project_id: int) -> bool:
        """Delete a project and its tasks."""
        if project_id not in self.projects:
            return False

        project = self.projects[project_id]
        for task in project.tasks:
            if task.id in self.tasks:
                del self.tasks[task.id]

        del self.projects[project_id]
        self.save_projects()
        self.save_tasks()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.project_id in self.projects:
            project = self.projects[task.project_id]
            project.tasks = [t for t in project.tasks if t.id != task_id]

        del self.tasks[task_id]
        self.save_projects()
        self.save_tasks()
        return True

    def save_projects(self) -> None:
        """Save projects to JSON file."""
        data = {
            'projects': [project.to_dict() for project in self.projects.values()],
            'last_id': self._next_project_id - 1
        }
        with open(self.projects_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def save_tasks(self) -> None:
        """Save tasks to JSON file."""
        data = {
            'tasks': [task.to_dict() for task in self.tasks.values()],
            'last_id': self._next_task_id - 1
        }
        with open(self.tasks_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def load_projects(self) -> bool:
        """Load projects from JSON file."""
        if not os.path.exists(self.projects_file):
            return False

        try:
            with open(self.projects_file, 'r') as f:
                data = json.load(f)
                self._next_project_id = data.get('last_id', 0) + 1
                # Projects loading logic would go here
            return True
        except (json.JSONDecodeError, IOError):
            return False

    def load_tasks(self) -> bool:
        """Load tasks from JSON file."""
        if not os.path.exists(self.tasks_file):
            return False

        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
                self._next_task_id = data.get('last_id', 0) + 1
                # Tasks loading logic would go here
            return True
        except (json.JSONDecodeError, IOError):
            return False

    def clear_all(self) -> None:
        """Clear all data from memory."""
        self.projects.clear()
        self.tasks.clear()
        self._next_project_id = 1
        self._next_task_id = 1
