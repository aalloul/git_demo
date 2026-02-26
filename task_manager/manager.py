"""Main task manager module for orchestrating task and project operations."""

from typing import List, Optional
from .models import Task, Project, TaskStatus, TaskPriority
from .database import Database


class TaskManager:
    """High-level manager for tasks and projects."""

    def __init__(self, database: Optional[Database] = None):
        """Initialize the task manager with a database."""
        self.db = database or Database()
        self.current_user: Optional[str] = None

    def set_current_user(self, user_name: str) -> None:
        """Set the current logged-in user."""
        self.current_user = user_name

    def create_project(
        self,
        name: str,
        description: str,
        owner: Optional[str] = None
    ) -> Project:
        """Create a new project."""
        owner = owner or self.current_user or "Unknown"
        return self.db.create_project(name, description, owner)

    def create_task(
        self,
        title: str,
        description: str,
        project_id: int,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> Optional[Task]:
        """Create a new task in a project."""
        task = self.db.create_task(title, description, project_id, priority)
        if task and self.current_user:
            task.assign_to(self.current_user)
        return task

    def get_my_projects(self) -> List[Project]:
        """Get all projects owned by the current user."""
        if not self.current_user:
            return []
        return [
            p for p in self.db.get_all_projects()
            if p.owner == self.current_user
        ]

    def get_my_tasks(self) -> List[Task]:
        """Get all tasks assigned to the current user."""
        if not self.current_user:
            return []
        return [
            t for t in self.db.get_all_tasks()
            if t.assigned_to == self.current_user
        ]

    def get_high_priority_tasks(self) -> List[Task]:
        """Get all high priority tasks."""
        return [
            t for t in self.db.get_all_tasks()
            if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]
            and t.status != TaskStatus.COMPLETED
        ]

    def get_overdue_tasks(self) -> List[Task]:
        """Get all tasks that are overdue."""
        from datetime import datetime
        now = datetime.now()
        return [
            t for t in self.db.get_all_tasks()
            if t.due_date and t.due_date < now
            and t.status != TaskStatus.COMPLETED
        ]

    def add_team_member_to_project(
        self,
        project_id: int,
        member_name: str
    ) -> bool:
        """Add a team member to a project."""
        project = self.db.get_project(project_id)
        if not project:
            return False
        project.add_member(member_name)
        self.db.save_projects()
        return True

    def assign_task(self, task_id: int, user_name: str) -> bool:
        """Assign a task to a user."""
        task = self.db.get_task(task_id)
        if not task:
            return False
        task.assign_to(user_name)
        self.db.save_tasks()
        return True

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        task = self.db.get_task(task_id)
        if not task:
            return False
        task.mark_completed()
        self.db.save_tasks()
        return True

    def get_project_stats(self, project_id: int) -> Optional[dict]:
        """Get statistics about a project."""
        project = self.db.get_project(project_id)
        if not project:
            return None

        total_tasks = len(project.tasks)
        completed_tasks = len(project.get_tasks_by_status(TaskStatus.COMPLETED))
        in_progress = len(project.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        todo_tasks = len(project.get_tasks_by_status(TaskStatus.TODO))

        return {
            'project_id': project_id,
            'project_name': project.name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress,
            'todo_tasks': todo_tasks,
            'completion_percentage': project.get_completion_rate(),
            'team_size': len(project.members)
        }

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description."""
        keyword_lower = keyword.lower()
        return [
            t for t in self.db.get_all_tasks()
            if keyword_lower in t.title.lower()
            or keyword_lower in t.description.lower()
        ]

    def search_tasks_by_tag(self, tag: str) -> List[Task]:
        """Search tasks by tag."""
        return [
            t for t in self.db.get_all_tasks()
            if tag in t.tags
        ]

    def archive_project(self, project_id: int) -> bool:
        """Archive a project."""
        project = self.db.get_project(project_id)
        if not project:
            return False
        project.archived = True
        self.db.save_projects()
        return True

    def unarchive_project(self, project_id: int) -> bool:
        """Unarchive a project."""
        project = self.db.get_project(project_id)
        if not project:
            return False
        project.archived = False
        self.db.save_projects()
        return True

    def log_task_time(self, task_id: int, hours: float) -> bool:
        """Log actual hours spent on a task."""
        task = self.db.get_task(task_id)
        if not task:
            return False
        task.set_actual_time(hours)
        self.db.save_tasks()
        return True

    def delete_project(self, project_id: int) -> bool:
        """Delete a project."""
        return self.db.delete_project(project_id)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        return self.db.delete_task(task_id)

