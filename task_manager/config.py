"""Configuration module for the task manager application."""

import os
from typing import Dict, Any


class Config:
    """Base configuration class."""

    # Application settings
    APP_NAME = "Task Manager Pro"
    APP_VERSION = "2.0.0"
    DEBUG = False
    TESTING = False

    # Database settings
    DATA_DIR = "./data"
    PROJECTS_FILE = "projects.json"
    TASKS_FILE = "tasks.json"

    # UI settings
    ITEMS_PER_PAGE = 50
    DATE_FORMAT = "%d/%m/%Y %H:%M"

    # Notification settings
    ENABLE_NOTIFICATIONS = True
    NOTIFY_OVERDUE_TASKS = True
    NOTIFY_DUE_TODAY = True
    NOTIFICATION_CHANNEL = "email"

    @classmethod
    def get_database_path(cls) -> str:
        """Get the full path to the database directory."""
        return os.path.abspath(cls.DATA_DIR)

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATA_DIR = "./data/dev"
    LOG_LEVEL = "DEBUG"


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATA_DIR = "./data/test"
    ENABLE_NOTIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DATA_DIR = "/opt/task_manager/data"
    LOG_LEVEL = "WARNING"


def get_config(environment: str = "production") -> Config:
    """Get configuration object based on environment."""
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    return configs.get(environment, ProductionConfig)

