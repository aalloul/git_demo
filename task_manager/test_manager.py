"""Unit tests for the task manager application."""

import unittest
from datetime import datetime, timedelta
from task_manager.models import Task, Project, TaskStatus, TaskPriority
from task_manager.database import Database
from task_manager.manager import TaskManager
from task_manager.utils import DateUtils, ValidationUtils, StringUtils


class TestTask(unittest.TestCase):
    """Test cases for the Task model."""

    def setUp(self):
        """Set up test fixtures."""
        self.task = Task(
            title="Test Task",
            description="A test task",
            project_id=1,
            priority=TaskPriority.MEDIUM
        )

    def test_task_creation(self):
        """Test task can be created."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, TaskStatus.TODO)
        self.assertEqual(self.task.priority, TaskPriority.MEDIUM)

    def test_mark_completed(self):
        """Test marking task as completed."""
        self.task.mark_completed()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(self.task.completed_at)

    def test_mark_in_progress(self):
        """Test marking task as in progress."""
        self.task.mark_in_progress()
        self.assertEqual(self.task.status, TaskStatus.IN_PROGRESS)

    def test_assign_to_user(self):
        """Test assigning task to a user."""
        self.task.assign_to("alice")
        self.assertEqual(self.task.assigned_to, "alice")

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['status'], "todo")


class TestProject(unittest.TestCase):
    """Test cases for the Project model."""

    def setUp(self):
        """Set up test fixtures."""
        self.project = Project(
            name="Test Project",
            description="A test project",
            owner="alice"
        )

    def test_project_creation(self):
        """Test project can be created."""
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.owner, "alice")
        self.assertIn("alice", self.project.members)

    def test_add_task(self):
        """Test adding task to project."""
        task = Task("Task 1", "Description", 1)
        self.project.add_task(task)
        self.assertEqual(len(self.project.tasks), 1)
        self.assertEqual(task.project_id, self.project.id)

    def test_add_member(self):
        """Test adding team member."""
        self.project.add_member("bob")
        self.assertIn("bob", self.project.members)

    def test_remove_member(self):
        """Test removing team member."""
        self.project.add_member("bob")
        self.project.remove_member("bob")
        self.assertNotIn("bob", self.project.members)

    def test_completion_rate(self):
        """Test project completion rate calculation."""
        task1 = Task("Task 1", "Desc", 1)
        task2 = Task("Task 2", "Desc", 1)
        self.project.add_task(task1)
        self.project.add_task(task2)

        self.assertEqual(self.project.get_completion_rate(), 0.0)

        task1.mark_completed()
        self.assertEqual(self.project.get_completion_rate(), 50.0)

        task2.mark_completed()
        self.assertEqual(self.project.get_completion_rate(), 100.0)


class TestDatabase(unittest.TestCase):
    """Test cases for the Database class."""

    def setUp(self):
        """Set up test fixtures."""
        self.db = Database("./data/test")
        self.db.clear_all()

    def test_create_project(self):
        """Test creating a project."""
        project = self.db.create_project("Test", "Desc", "alice")
        self.assertIsNotNone(project.id)
        self.assertEqual(project.name, "Test")

    def test_create_task(self):
        """Test creating a task."""
        project = self.db.create_project("Test", "Desc", "alice")
        task = self.db.create_task("Task", "Desc", project.id)
        self.assertIsNotNone(task)
        self.assertEqual(task.project_id, project.id)

    def test_get_project(self):
        """Test retrieving a project."""
        project = self.db.create_project("Test", "Desc", "alice")
        retrieved = self.db.get_project(project.id)
        self.assertEqual(project.id, retrieved.id)

    def test_delete_project(self):
        """Test deleting a project."""
        project = self.db.create_project("Test", "Desc", "alice")
        self.assertTrue(self.db.delete_project(project.id))
        self.assertIsNone(self.db.get_project(project.id))


class TestTaskManager(unittest.TestCase):
    """Test cases for the TaskManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.db = Database("./data/test")
        self.db.clear_all()
        self.manager = TaskManager(self.db)
        self.manager.set_current_user("alice")

    def test_create_project(self):
        """Test creating a project through manager."""
        project = self.manager.create_project("Test", "Desc")
        self.assertEqual(project.owner, "alice")

    def test_search_tasks(self):
        """Test searching tasks."""
        project = self.manager.create_project("Test", "Desc")
        self.manager.create_task("Python Task", "Learn Python", project.id)
        self.manager.create_task("JavaScript Task", "Learn JS", project.id)

        results = self.manager.search_tasks("Python")
        self.assertEqual(len(results), 1)


class TestDateUtils(unittest.TestCase):
    """Test cases for DateUtils."""

    def test_parse_date(self):
        """Test parsing date string."""
        date = DateUtils.parse_date("2024-12-25")
        self.assertEqual(date.year, 2024)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 25)

    def test_format_date(self):
        """Test formatting date."""
        date = datetime(2024, 12, 25)
        formatted = DateUtils.format_date(date)
        self.assertEqual(formatted, "2024-12-25")


class TestValidationUtils(unittest.TestCase):
    """Test cases for ValidationUtils."""

    def test_validate_email(self):
        """Test email validation."""
        self.assertTrue(ValidationUtils.validate_email("test@example.com"))
        self.assertFalse(ValidationUtils.validate_email("invalid-email"))

    def test_validate_username(self):
        """Test username validation."""
        self.assertTrue(ValidationUtils.validate_username("user123"))
        self.assertFalse(ValidationUtils.validate_username("ab"))


class TestStringUtils(unittest.TestCase):
    """Test cases for StringUtils."""

    def test_truncate(self):
        """Test string truncation."""
        text = "This is a very long string"
        truncated = StringUtils.truncate(text, max_length=10)
        self.assertEqual(len(truncated), 10)
        self.assertTrue(truncated.endswith("..."))

    def test_to_slug(self):
        """Test converting to slug."""
        slug = StringUtils.to_slug("Hello World Test")
        self.assertEqual(slug, "hello-world-test")


if __name__ == '__main__':
    unittest.main()

