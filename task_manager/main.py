"""Main application entry point and example usage."""

import sys
from datetime import datetime, timedelta
from task_manager import TaskManager, Database
from task_manager.models import TaskPriority
from task_manager.config import get_config


def main():
    """Run the task manager application."""
    # Initialize configuration and database
    config = get_config("development")
    db = Database(config.DATA_DIR)
    manager = TaskManager(db)

    # Set current user
    manager.set_current_user("alice")

    # Create sample projects
    project1 = manager.create_project(
        name="Website Redesign",
        description="Redesign the company website with modern UI/UX",
        owner="alice"
    )

    project2 = manager.create_project(
        name="Mobile App Development",
        description="Develop a mobile app for task tracking",
        owner="bob"
    )

    print(f"✓ Created project: {project1.name} (ID: {project1.id})")
    print(f"✓ Created project: {project2.name} (ID: {project2.id})")
    print()

    # Create tasks for project 1
    task1 = manager.create_task(
        title="Design mockups",
        description="Create UI mockups for the homepage",
        project_id=project1.id,
        priority=TaskPriority.HIGH
    )

    task2 = manager.create_task(
        title="Set up development environment",
        description="Install Node.js, npm packages, and configure build tools",
        project_id=project1.id,
        priority=TaskPriority.MEDIUM
    )

    task3 = manager.create_task(
        title="Fix responsive design issues",
        description="Ensure the website works on mobile devices",
        project_id=project1.id,
        priority=TaskPriority.CRITICAL
    )

    print(f"✓ Created task: {task1.title}")
    print(f"✓ Created task: {task2.title}")
    print(f"✓ Created task: {task3.title}")
    print()

    # Create tasks for project 2
    task4 = manager.create_task(
        title="Design database schema",
        description="Plan the database structure for the mobile app",
        project_id=project2.id,
        priority=TaskPriority.HIGH
    )

    task5 = manager.create_task(
        title="Implement user authentication",
        description="Add login and registration functionality",
        project_id=project2.id,
        priority=TaskPriority.CRITICAL
    )

    print(f"✓ Created task: {task4.title}")
    print(f"✓ Created task: {task5.title}")
    print()

    # Add team members
    manager.add_team_member_to_project(project1.id, "bob")
    manager.add_team_member_to_project(project1.id, "charlie")
    manager.add_team_member_to_project(project2.id, "alice")

    print(f"✓ Added team members to {project1.name}")
    print(f"✓ Added team members to {project2.name}")
    print()

    # Assign tasks and mark some as in progress
    if task1:
        manager.assign_task(task1.id, "bob")
        task1.mark_in_progress()

    if task2:
        manager.assign_task(task2.id, "charlie")

    if task4:
        manager.assign_task(task4.id, "bob")
        task4.mark_in_progress()

    print("✓ Assigned tasks to team members")
    print()

    # Display project statistics
    for project in [project1, project2]:
        stats = manager.get_project_stats(project.id)
        if stats:
            print(f"📊 {stats['project_name']} Statistics:")
            print(f"   Total tasks: {stats['total_tasks']}")
            print(f"   Completed: {stats['completed_tasks']}")
            print(f"   In progress: {stats['in_progress_tasks']}")
            print(f"   To do: {stats['todo_tasks']}")
            print(f"   Completion: {stats['completion_percentage']:.1f}%")
            print(f"   Team size: {stats['team_size']}")
            print()

    # Display all tasks
    print("📝 All Tasks:")
    for task in manager.db.get_all_tasks():
        status_icon = "✓" if task.status.value == "completed" else "○"
        print(f"   {status_icon} [{task.priority.name}] {task.title} "
              f"(Project ID: {task.project_id}, Assigned to: {task.assigned_to})")
    print()

    # Get high priority tasks
    high_priority = manager.get_high_priority_tasks()
    print(f"⚠️  High Priority Tasks ({len(high_priority)}):")
    for task in high_priority:
        print(f"   - {task.title}")
    print()

    # Get my tasks
    manager.set_current_user("alice")
    my_tasks = manager.get_my_tasks()
    print(f"👤 Alice's Tasks ({len(my_tasks)}):")
    for task in my_tasks:
        print(f"   - {task.title}")
    print()

    # Get my projects
    my_projects = manager.get_my_projects()
    print(f"📂 Alice's Projects ({len(my_projects)}):")
    for project in my_projects:
        print(f"   - {project.name}")


if __name__ == "__main__":
    main()

