"""Task Manager Application - A simple task management system."""

__version__ = "1.0.0"
__author__ = "Development Team"

from .models import Task, Project
from .database import Database
from .manager import TaskManager

__all__ = ["Task", "Project", "Database", "TaskManager"]

