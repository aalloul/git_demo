"""Data models for the task manager application."""

from enum import Enum
from datetime import datetime
from typing import Optional, List


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskPriority(Enum):
    """Enumeration of task priorities."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Task:
    """Represents a single task in the system."""

    def __init__(
        self,
        title: str,
        description: str,
        project_id: int,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: Optional[datetime] = None,
        task_id: Optional[int] = None
    ):
        """Initialize a new task."""
        self.id = task_id
        self.title = title
        self.description = description
        self.project_id = project_id
        self.priority = priority
        self.status = TaskStatus.TODO
        self.due_date = due_date
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.assigned_to: Optional[str] = None
        self.subtasks: List['Task'] = []

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def mark_in_progress(self) -> None:
        """Mark the task as in progress."""
        self.status = TaskStatus.IN_PROGRESS

    def assign_to(self, user_name: str) -> None:
        """Assign the task to a user."""
        self.assigned_to = user_name

    def add_subtask(self, subtask: 'Task') -> None:
        """Add a subtask to this task."""
        self.subtasks.append(subtask)

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_id': self.project_id,
            'priority': self.priority.name,
            'status': self.status.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'assigned_to': self.assigned_to,
            'subtasks': [st.to_dict() for st in self.subtasks]
        }

    def __repr__(self) -> str:
        """String representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value})"


class Project:
    """Represents a project containing multiple tasks."""

    def __init__(
        self,
        name: str,
        description: str,
        owner: str,
        project_id: Optional[int] = None
    ):
        """Initialize a new project."""
        self.id = project_id
        self.name = name
        self.description = description
        self.owner = owner
        self.created_at = datetime.now()
        self.tasks: List[Task] = []
        self.members: List[str] = [owner]
        self.archived = False

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        task.project_id = self.id
        self.tasks.append(task)

    def add_member(self, member_name: str) -> None:
        """Add a team member to the project."""
        if member_name not in self.members:
            self.members.append(member_name)

    def remove_member(self, member_name: str) -> None:
        """Remove a team member from the project."""
        if member_name in self.members and member_name != self.owner:
            self.members.remove(member_name)

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status."""
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Get all tasks with a specific priority."""
        return [task for task in self.tasks if task.priority == priority]

    def get_completion_rate(self) -> float:
        """Get the percentage of completed tasks."""
        if not self.tasks:
            return 0.0
        completed = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        return (completed / len(self.tasks)) * 100

    def to_dict(self) -> dict:
        """Convert project to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner,
            'created_at': self.created_at.isoformat(),
            'members': self.members,
            'tasks': [task.to_dict() for task in self.tasks],
            'archived': self.archived,
            'completion_rate': self.get_completion_rate()
        }

    def __repr__(self) -> str:
        """String representation of the project."""
        return f"Project(id={self.id}, name='{self.name}', owner='{self.owner}')"

