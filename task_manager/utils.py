"""Utility functions for the task manager application."""

from datetime import datetime, timedelta
from typing import List
import re


class DateUtils:
    """Utilities for date operations."""

    @staticmethod
    def parse_date(date_string: str) -> datetime:
        """Parse a date string in format YYYY-MM-DD."""
        try:
            return datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_string}")

    @staticmethod
    def days_until_due(due_date: datetime) -> int:
        """Calculate days until a due date."""
        delta = due_date - datetime.now()
        return delta.days

    @staticmethod
    def is_overdue(due_date: datetime) -> bool:
        """Check if a task is overdue."""
        return due_date < datetime.now()

    @staticmethod
    def is_due_today(due_date: datetime) -> bool:
        """Check if a task is due today."""
        today = datetime.now().date()
        return due_date.date() == today

    @staticmethod
    def format_date(date_obj: datetime, format_string: str = "%Y-%m-%d") -> str:
        """Format a datetime object as string."""
        return date_obj.strftime(format_string)


class ValidationUtils:
    """Utilities for data validation."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username (alphanumeric and underscore, 3-20 chars)."""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None

    @staticmethod
    def validate_string(value: str, min_length: int = 1, max_length: int = 255) -> bool:
        """Validate string length."""
        return min_length <= len(value) <= max_length


class StringUtils:
    """Utilities for string operations."""

    @staticmethod
    def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
        """Truncate text to a maximum length."""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def to_slug(text: str) -> str:
        """Convert text to URL-friendly slug."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text

    @staticmethod
    def capitalize_words(text: str) -> str:
        """Capitalize first letter of each word."""
        return ' '.join(word.capitalize() for word in text.split())


class ListUtils:
    """Utilities for list operations."""

    @staticmethod
    def chunk(items: List, chunk_size: int) -> List[List]:
        """Divide a list into chunks."""
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    @staticmethod
    def flatten(nested_list: List[List]) -> List:
        """Flatten a nested list."""
        return [item for sublist in nested_list for item in sublist]

    @staticmethod
    def unique(items: List) -> List:
        """Get unique items from a list while preserving order."""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

