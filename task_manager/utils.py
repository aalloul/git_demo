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


class TimeUtils:
    """Utilities for time and duration operations."""

    @staticmethod
    def format_duration(hours: float) -> str:
        """Format hours as a readable duration string."""
        if hours < 1:
            minutes = int(hours * 60)
            return f"{minutes}m"
        elif hours == int(hours):
            return f"{int(hours)}h"
        else:
            h = int(hours)
            m = int((hours - h) * 60)
            return f"{h}h {m}m"

    @staticmethod
    def hours_to_minutes(hours: float) -> int:
        """Convert hours to minutes."""
        return int(hours * 60)

    @staticmethod
    def minutes_to_hours(minutes: int) -> float:
        """Convert minutes to hours."""
        return minutes / 60

    @staticmethod
    def calculate_time_difference(start_date: datetime, end_date: datetime) -> dict:
        """Calculate the difference between two dates."""
        delta = end_date - start_date
        return {
            'days': delta.days,
            'hours': delta.seconds // 3600,
            'minutes': (delta.seconds % 3600) // 60,
            'total_hours': delta.total_seconds() / 3600
        }


class TagUtils:
    """Utilities for tag management and operations."""

    @staticmethod
    def normalize_tag(tag: str) -> str:
        """Normalize a tag (lowercase, strip whitespace)."""
        return tag.lower().strip()

    @staticmethod
    def validate_tag(tag: str) -> bool:
        """Validate if a tag is valid."""
        if not tag or len(tag) > 50:
            return False
        return all(c.isalnum() or c in ['-', '_'] for c in tag)

    @staticmethod
    def parse_tags(tag_string: str) -> List[str]:
        """Parse a comma or space-separated string of tags."""
        tags = re.split(r'[,\s]+', tag_string.strip())
        return [TagUtils.normalize_tag(tag) for tag in tags if tag]


