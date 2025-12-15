"""Main CLI entry point for todo application."""

from datetime import datetime, timedelta
from typing import Optional

import click
import questionary

from src.services.task_service import TaskService
from src.storage.task_store import InMemoryTaskStore
from src.utils.date_parser import parse_date
from src.utils.formatters import (
    console,
    format_task_table,
    print_error,
    print_info,
    print_success,
)
from src.utils.validators import (
    validate_categories,
    validate_description,
    validate_priority,
    validate_recurrence_pattern,
    validate_task_id,
    validate_title,
)

# Global task store and service instances
task_store = InMemoryTaskStore()
task_service = TaskService(task_store)


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0", prog_name="todo")
def cli(ctx: click.Context) -> None:
    """Todo Console Application - Manage your tasks efficiently.

    A powerful command-line todo application with priorities, categories,
    search, filtering, recurring tasks, and due date reminders.
    """
    if ctx.invoked_subcommand is None:
        show_main_menu()


def show_main_menu() -> None:
    """Display interactive main menu."""
    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Task",
                "List Tasks",
                "Update Task",
                "Delete Task",
                "Complete Task",
                "Search Tasks",
                "Sort Tasks",
                "Exit"
            ],
            qmark="",
            pointer="►"
        ).ask()

        if choice is None or choice == "Exit":
            console.print("[blue]Goodbye![/blue]")
            break
        elif choice == "Add Task":
            interactive_add()
        elif choice == "List Tasks":
            interactive_list()
        elif choice == "Update Task":
            interactive_update()
        elif choice == "Delete Task":
            interactive_delete()
        elif choice == "Complete Task":
            interactive_complete()
        elif choice == "Search Tasks":
            interactive_search()
        elif choice == "Sort Tasks":
            interactive_sort()


def interactive_add() -> None:
    """Interactive task addition with keyboard selection."""
    try:
        # Get title
        console.print("\n[cyan]Create New Task[/cyan]")
        console.print("[dim]Enter task details below:[/dim]\n")

        title = questionary.text(
            "Task title:",
            validate=lambda text: len(text.strip()) > 0 or "Title cannot be empty",
            instruction="(Type and press Enter)"
        ).ask()

        if title is None:
            return

        # Get description
        description = questionary.text(
            "Description (optional):",
            default="",
            instruction="(Type and press Enter, or just press Enter to skip)"
        ).ask()

        if description is None:
            description = ""

        # Get priority with keyboard selection
        priority = questionary.select(
            "Priority:",
            choices=["HIGH", "MEDIUM", "LOW"],
            default="MEDIUM",
            qmark="",
            pointer="►"
        ).ask()

        if priority is None:
            priority = "MEDIUM"

        # Get categories
        add_categories = questionary.confirm(
            "Add categories?",
            default=False
        ).ask()

        categories = []
        if add_categories:
            while True:
                category = questionary.text(
                    "Category (press Enter to finish):",
                    default=""
                ).ask()

                if not category or not category.strip():
                    break
                categories.append(category.strip())

        # Get due date
        add_due_date = questionary.confirm(
            "Add due date?",
            default=False
        ).ask()

        due_date = None
        if add_due_date:
            due_str = questionary.text(
                "Due date (e.g., '2025-01-15', 'tomorrow', 'next monday'):"
            ).ask()

            if due_str and due_str.strip():
                try:
                    due_date = parse_date(due_str)
                except ValueError as e:
                    print_error(f"Invalid due date: {e}")
                    return

        # Get recurrence
        add_recurring = questionary.confirm(
            "Make it recurring?",
            default=False
        ).ask()

        recurrence_pattern = None
        if add_recurring:
            recurrence_pattern = questionary.select(
                "Recurrence pattern:",
                choices=["DAILY", "WEEKLY", "MONTHLY"],
                qmark="",
                pointer="►"
            ).ask()

        # Validate and create task
        validated_title = validate_title(title)
        validated_description = validate_description(description)
        validated_priority = validate_priority(priority)
        validated_categories = validate_categories(categories)
        validated_recurrence = validate_recurrence_pattern(recurrence_pattern) if recurrence_pattern else None

        task = task_service.create_task(
            title=validated_title,
            description=validated_description,
            priority=validated_priority,
            categories=validated_categories,
            due_date=due_date,
            recurrence_pattern=validated_recurrence,
        )

        print_success(f"Task created successfully (ID: {task.id})")
        console.print(f"  Title: {task.title}")
        if task.description:
            console.print(f"  Description: {task.description}")
        console.print(f"  Priority: {task.priority}")
        if task.categories:
            console.print(f"  Categories: {', '.join(task.categories)}")
        if task.due_date:
            console.print(f"  Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        if task.recurrence_pattern:
            console.print(f"  Recurrence: {task.recurrence_pattern}")

        console.print()  # Add blank line

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


def interactive_list() -> None:
    """Interactive task listing with preset views."""
    try:
        # Show preset view options
        view = questionary.select(
            "View:",
            choices=[
                "All tasks",
                "Pending tasks",
                "Completed tasks",
                "High priority tasks",
                "Medium priority tasks",
                "Low priority tasks",
                "Custom filters..."
            ],
            default="Pending tasks",
            qmark="",
            pointer="►"
        ).ask()

        if view is None:
            return

        # Handle preset views
        if view == "Custom filters...":
            # Custom filtering flow
            status = questionary.select(
                "Show tasks:",
                choices=["All", "Pending", "Completed"],
                default="All",
                qmark="",
                pointer="►"
            ).ask()

            if status is None:
                return

            # Ask for priority filter
            filter_priority = questionary.confirm(
                "Filter by priority?",
                default=False
            ).ask()

            priority = None
            if filter_priority:
                priority = questionary.select(
                    "Priority:",
                    choices=["HIGH", "MEDIUM", "LOW"],
                    qmark="",
                    pointer="►"
                ).ask()

            # Ask for category filter
            filter_category = questionary.confirm(
                "Filter by category?",
                default=False
            ).ask()

            category = None
            if filter_category:
                category = questionary.text("Category:").ask()

            # Ask for created date filter
            filter_created = questionary.confirm(
                "Filter by created date?",
                default=False
            ).ask()

            created_date_start = None
            created_date_end = None
            if filter_created:
                created_preset = questionary.select(
                    "Created date filter:",
                    choices=["Any time", "Today", "Last 7 days", "Last 30 days", "Custom date..."],
                    default="Any time",
                    qmark="",
                    pointer="►"
                ).ask()

                if created_preset == "Today":
                    now = datetime.now()
                    created_date_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                    created_date_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
                elif created_preset == "Last 7 days":
                    now = datetime.now()
                    created_date_start = now - timedelta(days=7)
                    created_date_end = now
                elif created_preset == "Last 30 days":
                    now = datetime.now()
                    created_date_start = now - timedelta(days=30)
                    created_date_end = now
                elif created_preset == "Custom date...":
                    date_input = questionary.text(
                        "Enter date (e.g., '2025-01-15', 'today', 'yesterday'):"
                    ).ask()
                    if date_input and date_input.strip():
                        try:
                            created_date_start = parse_date(date_input).replace(hour=0, minute=0, second=0, microsecond=0)
                            created_date_end = created_date_start.replace(hour=23, minute=59, second=59, microsecond=999999)
                        except ValueError as e:
                            print_error(f"Invalid date: {e}")
                            return

            # Ask for due date filter
            filter_due = questionary.confirm(
                "Filter by due date?",
                default=False
            ).ask()

            due_date_filter = None
            due_date_custom = None
            if filter_due:
                due_preset = questionary.select(
                    "Due date filter:",
                    choices=["Any time", "Overdue", "Today", "This week", "Custom date..."],
                    default="Any time",
                    qmark="",
                    pointer="►"
                ).ask()

                if due_preset == "Overdue":
                    due_date_filter = "overdue"
                elif due_preset == "Today":
                    due_date_filter = "today"
                elif due_preset == "This week":
                    due_date_filter = "this_week"
                elif due_preset == "Custom date...":
                    date_input = questionary.text(
                        "Enter due date (e.g., '2025-01-15', 'tomorrow', 'next monday'):"
                    ).ask()
                    if date_input and date_input.strip():
                        try:
                            due_date_custom = parse_date(date_input)
                        except ValueError as e:
                            print_error(f"Invalid date: {e}")
                            return

            # Get tasks based on filters
            if status == "All":
                tasks = task_service.get_all_tasks()
            elif status == "Pending":
                tasks = task_service.filter_tasks(completed=False)
            else:  # Completed
                tasks = task_service.filter_tasks(completed=True)

            # Apply additional filters
            if priority:
                priority_val = lambda t: t.priority.value if hasattr(t.priority, 'value') else t.priority
                tasks = [t for t in tasks if priority_val(t) == priority.upper()]

            if category:
                tasks = [
                    t for t in tasks if category.lower() in [c.lower() for c in t.categories]
                ]

            # Apply created date filter
            if created_date_start and created_date_end:
                tasks = [
                    t for t in tasks
                    if created_date_start <= t.created_at <= created_date_end
                ]

            # Apply due date filter
            if due_date_filter or due_date_custom:
                now = datetime.now()
                if due_date_filter == "overdue":
                    tasks = [t for t in tasks if t.due_date and t.due_date < now]
                elif due_date_filter == "today":
                    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
                    tasks = [t for t in tasks if t.due_date and today_start <= t.due_date <= today_end]
                elif due_date_filter == "this_week":
                    week_end = now + timedelta(days=7)
                    tasks = [t for t in tasks if t.due_date and now <= t.due_date <= week_end]
                elif due_date_custom:
                    due_start = due_date_custom.replace(hour=0, minute=0, second=0, microsecond=0)
                    due_end = due_date_custom.replace(hour=23, minute=59, second=59, microsecond=999999)
                    tasks = [t for t in tasks if t.due_date and due_start <= t.due_date <= due_end]

            # Sort tasks by created_at (default)
            tasks = task_service.sort_tasks(tasks, "created_at")

            # Display tasks
            if not tasks:
                print_info("No tasks found matching the criteria.")
                return

            table = format_task_table(tasks, title=f"Tasks ({len(tasks)} total)")
            console.print(table)
            console.print()

        else:
            # Handle preset views
            if view == "All tasks":
                tasks = task_service.get_all_tasks()
                title = f"All Tasks ({len(tasks)} total)"
            elif view == "Pending tasks":
                tasks = task_service.filter_tasks(completed=False)
                title = f"Pending Tasks ({len(tasks)} total)"
            elif view == "Completed tasks":
                tasks = task_service.filter_tasks(completed=True)
                title = f"Completed Tasks ({len(tasks)} total)"
            elif view == "High priority tasks":
                tasks = task_service.get_all_tasks()
                priority_val = lambda t: t.priority.value if hasattr(t.priority, 'value') else t.priority
                tasks = [t for t in tasks if priority_val(t) == "HIGH"]
                title = f"High Priority Tasks ({len(tasks)} total)"
            elif view == "Medium priority tasks":
                tasks = task_service.get_all_tasks()
                priority_val = lambda t: t.priority.value if hasattr(t.priority, 'value') else t.priority
                tasks = [t for t in tasks if priority_val(t) == "MEDIUM"]
                title = f"Medium Priority Tasks ({len(tasks)} total)"
            elif view == "Low priority tasks":
                tasks = task_service.get_all_tasks()
                priority_val = lambda t: t.priority.value if hasattr(t.priority, 'value') else t.priority
                tasks = [t for t in tasks if priority_val(t) == "LOW"]
                title = f"Low Priority Tasks ({len(tasks)} total)"

            # Sort by created_at (default)
            tasks = task_service.sort_tasks(tasks, "created_at")

            # Display tasks
            if not tasks:
                print_info("No tasks found.")
                return

            table = format_task_table(tasks, title=title)
            console.print(table)
            console.print()

    except Exception as e:
        print_error(f"Error listing tasks: {e}")


def interactive_update() -> None:
    """Interactive task update with one-by-one field selection."""
    try:
        # Show all tasks first
        tasks = task_service.get_all_tasks()
        if not tasks:
            print_info("No tasks to update.")
            return

        table = format_task_table(tasks, title="Select a task to update")
        console.print(table)

        # Get task ID
        task_id_str = questionary.text("Task ID to update:").ask()
        if not task_id_str:
            return

        task_id = validate_task_id(task_id_str)
        task = task_service.get_task(task_id)

        if task is None:
            print_error(f"Task with ID {task_id} not found.")
            return

        console.print(f"\n[yellow]Updating task: {task.title}[/yellow]\n")

        # Loop for updating fields one by one
        updated_count = 0
        while True:
            # Refresh task data after each update
            task = task_service.get_task(task_id)
            if not task:
                break

            # Show current values
            priority_val = task.priority.value if hasattr(task.priority, 'value') else task.priority
            console.print(f"[dim]Current - Title: {task.title} | Priority: {priority_val}[/dim]")

            # Ask which field to update
            field_choice = questionary.select(
                "Which field do you want to update?",
                choices=[
                    "Title",
                    "Description",
                    "Priority",
                    "Categories",
                    "Due Date",
                    "Recurrence",
                    "Done (finish updating)"
                ],
                qmark="",
                pointer="►"
            ).ask()

            if field_choice is None or field_choice == "Done (finish updating)":
                break

            # Update the selected field
            if field_choice == "Title":
                console.print(f"\n[cyan]Current title:[/cyan] {task.title}")
                console.print("[dim]Type the new title below and press Enter:[/dim]")
                new_title = questionary.text(
                    "New title:",
                    default=task.title,
                    instruction="(Edit and press Enter)"
                ).ask()
                if new_title and new_title.strip():
                    validated_title = validate_title(new_title)
                    updated_task = task_service.update_task(task_id, title=validated_title)
                    if updated_task:
                        print_success(f"✓ Title updated to: {validated_title}")
                        updated_count += 1
                    else:
                        print_error("Failed to update title")
                console.print()

            elif field_choice == "Description":
                console.print(f"\n[cyan]Current description:[/cyan] {task.description if task.description else '(empty)'}")
                console.print("[dim]Type the new description below and press Enter:[/dim]")
                new_desc = questionary.text(
                    "New description:",
                    default=task.description if task.description else "",
                    instruction="(Edit and press Enter, or leave empty)"
                ).ask()
                if new_desc is not None:
                    validated_desc = validate_description(new_desc)
                    updated_task = task_service.update_task(task_id, description=validated_desc)
                    if updated_task:
                        print_success(f"✓ Description updated")
                        updated_count += 1
                    else:
                        print_error("Failed to update description")
                console.print()

            elif field_choice == "Priority":
                priority_default = task.priority.value if hasattr(task.priority, 'value') else task.priority
                new_priority = questionary.select(
                    "Select priority:",
                    choices=["HIGH", "MEDIUM", "LOW"],
                    default=priority_default,
                    qmark="",
                    pointer="►"
                ).ask()
                if new_priority:
                    validated_priority = validate_priority(new_priority)
                    updated_task = task_service.update_task(task_id, priority=validated_priority)
                    if updated_task:
                        print_success(f"✓ Priority updated to: {new_priority}")
                        updated_count += 1
                    else:
                        print_error("Failed to update priority")
                console.print()

            elif field_choice == "Categories":
                console.print(f"\n[cyan]Current categories:[/cyan] {', '.join(task.categories) if task.categories else '(none)'}")
                categories = []
                console.print("[yellow]Enter categories (press Enter with empty input to finish):[/yellow]")
                while True:
                    cat = questionary.text("Category:", default="").ask()
                    if not cat or not cat.strip():
                        break
                    categories.append(cat.strip())
                if categories:
                    validated_categories = validate_categories(categories)
                    updated_task = task_service.update_task(task_id, categories=validated_categories)
                    if updated_task:
                        print_success(f"✓ Categories updated to: {', '.join(categories)}")
                        updated_count += 1
                    else:
                        print_error("Failed to update categories")
                console.print()

            elif field_choice == "Due Date":
                console.print(f"\n[cyan]Current due date:[/cyan] {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else '(none)'}")
                due_str = questionary.text(
                    "New due date (e.g., '2025-01-15', 'tomorrow'):",
                    instruction="(Type date and press Enter)"
                ).ask()
                if due_str and due_str.strip():
                    try:
                        parsed_date = parse_date(due_str)
                        updated_task = task_service.update_task(task_id, due_date=parsed_date)
                        if updated_task:
                            print_success(f"✓ Due date updated to: {parsed_date.strftime('%Y-%m-%d %H:%M')}")
                            updated_count += 1
                        else:
                            print_error("Failed to update due date")
                    except ValueError as e:
                        print_error(f"Invalid due date: {e}")
                console.print()

            elif field_choice == "Recurrence":
                recurrence_val = task.recurrence_pattern.value if hasattr(task.recurrence_pattern, 'value') else task.recurrence_pattern if task.recurrence_pattern else "(none)"
                console.print(f"\n[cyan]Current recurrence:[/cyan] {recurrence_val}")
                new_recurrence = questionary.select(
                    "Select recurrence pattern:",
                    choices=["DAILY", "WEEKLY", "MONTHLY", "None"],
                    qmark="",
                    pointer="►"
                ).ask()
                if new_recurrence:
                    if new_recurrence != "None":
                        validated_recurrence = validate_recurrence_pattern(new_recurrence)
                        updated_task = task_service.update_task(task_id, recurrence_pattern=validated_recurrence)
                        if updated_task:
                            print_success(f"✓ Recurrence updated to: {new_recurrence}")
                            updated_count += 1
                        else:
                            print_error("Failed to update recurrence")
                    else:
                        updated_task = task_service.update_task(task_id, recurrence_pattern=None)
                        if updated_task:
                            print_success(f"✓ Recurrence removed")
                            updated_count += 1
                        else:
                            print_error("Failed to remove recurrence")
                console.print()

        # Show final summary
        if updated_count > 0:
            final_task = task_service.get_task(task_id)
            if final_task:
                console.print(f"[green]✓ Task updated successfully ({updated_count} field{'s' if updated_count > 1 else ''} changed)[/green]")
                console.print(f"  ID: {final_task.id}")
                console.print(f"  Title: {final_task.title}")
                priority_val = final_task.priority.value if hasattr(final_task.priority, 'value') else final_task.priority
                console.print(f"  Priority: {priority_val}")
                if final_task.description:
                    console.print(f"  Description: {final_task.description}")
                if final_task.categories:
                    console.print(f"  Categories: {', '.join(final_task.categories)}")
                if final_task.due_date:
                    console.print(f"  Due: {final_task.due_date.strftime('%Y-%m-%d %H:%M')}")
                if final_task.recurrence_pattern:
                    recurrence_val = final_task.recurrence_pattern.value if hasattr(final_task.recurrence_pattern, 'value') else final_task.recurrence_pattern
                    console.print(f"  Recurrence: {recurrence_val}")
        else:
            print_info("No changes made.")

        console.print()  # Add blank line

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


def interactive_delete() -> None:
    """Interactive task deletion."""
    try:
        # Show all tasks first
        tasks = task_service.get_all_tasks()
        if not tasks:
            print_info("No tasks to delete.")
            return

        table = format_task_table(tasks, title="Select a task to delete")
        console.print(table)

        # Get task ID
        task_id_str = questionary.text("Task ID to delete:").ask()
        if not task_id_str:
            return

        task_id = validate_task_id(task_id_str)
        task = task_service.get_task(task_id)

        if task is None:
            print_error(f"Task with ID {task_id} not found.")
            return

        # Confirm deletion
        console.print(f"\n[yellow]About to delete task:[/yellow]")
        console.print(f"  ID: {task.id}")
        console.print(f"  Title: {task.title}")

        confirm = questionary.confirm(
            "Are you sure you want to delete this task?",
            default=False
        ).ask()

        if confirm:
            if task_service.delete_task(task_id):
                print_success(f"Task {task_id} deleted successfully")
            else:
                print_error(f"Failed to delete task {task_id}")
        else:
            console.print("[blue]Deletion cancelled.[/blue]")

        console.print()  # Add blank line

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


def interactive_complete() -> None:
    """Interactive task completion toggle."""
    try:
        # Show pending tasks
        tasks = task_service.filter_tasks(completed=False)
        if not tasks:
            print_info("No pending tasks to complete.")
            return

        table = format_task_table(tasks, title="Select a task to mark as complete")
        console.print(table)

        # Get task ID
        task_id_str = questionary.text("Task ID to complete:").ask()
        if not task_id_str:
            return

        task_id = validate_task_id(task_id_str)
        task = task_service.get_task(task_id)

        if task is None:
            print_error(f"Task with ID {task_id} not found.")
            return

        # Toggle completion
        updated_task = task_service.toggle_completion(task_id)

        if updated_task:
            if updated_task.completed:
                print_success(f"Task {task_id} marked as complete")

                if updated_task.recurrence_pattern:
                    recurrence_val = updated_task.recurrence_pattern.value if hasattr(updated_task.recurrence_pattern, 'value') else updated_task.recurrence_pattern
                    console.print(
                        f"[blue]ℹ[/blue] Created next occurrence for recurring task "
                        f"({recurrence_val})"
                    )
            else:
                print_success(f"Task {task_id} marked as incomplete")

            console.print(f"  Title: {updated_task.title}")
        else:
            print_error(f"Failed to update task {task_id}")

        console.print()  # Add blank line

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


def interactive_search() -> None:
    """Interactive task search."""
    try:
        keyword = questionary.text("Search keyword:").ask()

        if not keyword or not keyword.strip():
            print_error("Search keyword cannot be empty")
            return

        tasks = task_service.search_tasks(keyword.strip())

        if not tasks:
            print_info(f"No tasks found matching '{keyword}'")
            return

        table = format_task_table(tasks, title=f"Search Results for '{keyword}' ({len(tasks)} found)")
        console.print(table)
        console.print()  # Add blank line

    except Exception as e:
        print_error(f"Error searching tasks: {e}")


def interactive_sort() -> None:
    """Interactive task sorting with preset options."""
    try:
        sort_option = questionary.select(
            "Sort all tasks by:",
            choices=[
                "Priority (High to Low)",
                "Due date (Earliest first)",
                "Created date (Newest first)",
                "Created date (Oldest first)",
                "Title (A to Z)",
                "Title (Z to A)"
            ],
            default="Priority (High to Low)",
            qmark="",
            pointer="►"
        ).ask()

        if sort_option is None:
            return

        tasks = task_service.get_all_tasks()

        if not tasks:
            print_info("No tasks to sort")
            return

        # Map selection to sort field and order
        if sort_option == "Priority (High to Low)":
            sorted_tasks = task_service.sort_tasks(tasks, "priority", reverse=False)
            title = "Tasks sorted by Priority (High to Low)"
        elif sort_option == "Due date (Earliest first)":
            sorted_tasks = task_service.sort_tasks(tasks, "due_date", reverse=False)
            title = "Tasks sorted by Due Date (Earliest first)"
        elif sort_option == "Created date (Newest first)":
            sorted_tasks = task_service.sort_tasks(tasks, "created_at", reverse=True)
            title = "Tasks sorted by Created Date (Newest first)"
        elif sort_option == "Created date (Oldest first)":
            sorted_tasks = task_service.sort_tasks(tasks, "created_at", reverse=False)
            title = "Tasks sorted by Created Date (Oldest first)"
        elif sort_option == "Title (A to Z)":
            sorted_tasks = task_service.sort_tasks(tasks, "title", reverse=False)
            title = "Tasks sorted by Title (A to Z)"
        elif sort_option == "Title (Z to A)":
            sorted_tasks = task_service.sort_tasks(tasks, "title", reverse=True)
            title = "Tasks sorted by Title (Z to A)"

        table = format_task_table(sorted_tasks, title=title)
        console.print(table)
        console.print()  # Add blank line

    except Exception as e:
        print_error(f"Error sorting tasks: {e}")


@cli.command()
@click.argument("title")
@click.option("--description", "-d", default="", help="Task description")
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["HIGH", "MEDIUM", "LOW"], case_sensitive=False),
    default="MEDIUM",
    help="Task priority",
)
@click.option("--category", "-c", multiple=True, help="Category tags (can specify multiple)")
@click.option("--due", help="Due date (e.g., '2025-01-15', 'tomorrow', 'next monday')")
@click.option(
    "--recurring",
    type=click.Choice(["DAILY", "WEEKLY", "MONTHLY"], case_sensitive=False),
    help="Recurrence pattern",
)
def add(
    title: str,
    description: str,
    priority: str,
    category: tuple,
    due: Optional[str],
    recurring: Optional[str],
) -> None:
    """Add a new task.

    Examples:

        todo add "Buy groceries"

        todo add "Team meeting" -d "Discuss Q1 goals" -p HIGH --category work

        todo add "Water plants" --due tomorrow --recurring DAILY
    """
    try:
        # Validate inputs
        validated_title = validate_title(title)
        validated_description = validate_description(description)
        validated_priority = validate_priority(priority)
        validated_categories = validate_categories(list(category))

        # Parse due date if provided
        due_date = None
        if due:
            try:
                due_date = parse_date(due)
            except ValueError as e:
                print_error(f"Invalid due date: {e}")
                return

        # Validate recurrence pattern if provided
        validated_recurrence = None
        if recurring:
            validated_recurrence = validate_recurrence_pattern(recurring)

        # Create task
        task = task_service.create_task(
            title=validated_title,
            description=validated_description,
            priority=validated_priority,
            categories=validated_categories,
            due_date=due_date,
            recurrence_pattern=validated_recurrence,
        )

        print_success(f"Task created successfully (ID: {task.id})")
        console.print(f"  Title: {task.title}")
        if task.description:
            console.print(f"  Description: {task.description}")
        console.print(f"  Priority: {task.priority}")
        if task.categories:
            console.print(f"  Categories: {', '.join(task.categories)}")
        if task.due_date:
            console.print(f"  Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        if task.recurrence_pattern:
            console.print(f"  Recurrence: {task.recurrence_pattern}")

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


@cli.command(name="list")
@click.option(
    "--status",
    type=click.Choice(["pending", "completed", "all"], case_sensitive=False),
    default="all",
    help="Filter by completion status",
)
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["HIGH", "MEDIUM", "LOW"], case_sensitive=False),
    help="Filter by priority",
)
@click.option("--category", "-c", help="Filter by category")
@click.option(
    "--sort-by",
    type=click.Choice(["priority", "due_date", "created_at", "title"], case_sensitive=False),
    default="created_at",
    help="Sort tasks by field",
)
def list_tasks(status: str, priority: Optional[str], category: Optional[str], sort_by: str) -> None:
    """List tasks with optional filters.

    Examples:

        todo list

        todo list --status pending

        todo list --priority HIGH --category work

        todo list --sort-by due_date
    """
    try:
        # Get tasks based on filters
        if status == "all":
            tasks = task_service.get_all_tasks()
        elif status == "pending":
            tasks = task_service.filter_tasks(completed=False)
        else:  # completed
            tasks = task_service.filter_tasks(completed=True)

        # Apply additional filters
        if priority:
            priority_val = lambda t: t.priority.value if hasattr(t.priority, 'value') else t.priority
            tasks = [t for t in tasks if priority_val(t) == priority.upper()]

        if category:
            tasks = [
                t for t in tasks if category.lower() in [c.lower() for c in t.categories]
            ]

        # Sort tasks
        tasks = task_service.sort_tasks(tasks, sort_by.lower())

        # Display tasks
        if not tasks:
            print_info("No tasks found matching the criteria.")
            return

        table = format_task_table(tasks, title=f"Tasks ({len(tasks)} total)")
        console.print(table)

    except Exception as e:
        print_error(f"Error listing tasks: {e}")


@cli.command()
@click.argument("task_id")
@click.option("--title", "-t", help="New task title")
@click.option("--description", "-d", help="New task description")
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["HIGH", "MEDIUM", "LOW"], case_sensitive=False),
    help="New task priority",
)
@click.option("--category", "-c", multiple=True, help="New category tags (replaces existing)")
@click.option("--due", help="New due date")
@click.option(
    "--recurring",
    type=click.Choice(["DAILY", "WEEKLY", "MONTHLY"], case_sensitive=False),
    help="New recurrence pattern",
)
def update(
    task_id: str,
    title: Optional[str],
    description: Optional[str],
    priority: Optional[str],
    category: tuple,
    due: Optional[str],
    recurring: Optional[str],
) -> None:
    """Update an existing task.

    Examples:

        todo update 1 --title "New title"

        todo update 2 --priority HIGH --due "2025-01-20"

        todo update 3 --category work --category urgent
    """
    try:
        # Validate task ID
        validated_id = validate_task_id(task_id)

        # Check if task exists
        task = task_service.get_task(validated_id)
        if task is None:
            print_error(f"Task with ID {validated_id} not found.")
            return

        # Build update dictionary
        updates = {}

        if title is not None:
            updates["title"] = validate_title(title)

        if description is not None:
            updates["description"] = validate_description(description)

        if priority is not None:
            updates["priority"] = validate_priority(priority)

        if category:
            updates["categories"] = validate_categories(list(category))

        if due is not None:
            try:
                updates["due_date"] = parse_date(due)
            except ValueError as e:
                print_error(f"Invalid due date: {e}")
                return

        if recurring is not None:
            updates["recurrence_pattern"] = validate_recurrence_pattern(recurring)

        # Check if any updates were provided
        if not updates:
            print_error("No updates provided. Use --title, --description, --priority, etc.")
            return

        # Update task
        updated_task = task_service.update_task(validated_id, **updates)

        if updated_task:
            print_success(f"Task {validated_id} updated successfully")
            console.print(f"  Title: {updated_task.title}")
            console.print(f"  Priority: {updated_task.priority.value}")
            if updated_task.categories:
                console.print(f"  Categories: {', '.join(updated_task.categories)}")
        else:
            print_error(f"Failed to update task {validated_id}")

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


@cli.command()
@click.argument("task_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
def delete(task_id: str, yes: bool) -> None:
    """Delete a task.

    Examples:

        todo delete 1

        todo delete 2 --yes
    """
    try:
        # Validate task ID
        validated_id = validate_task_id(task_id)

        # Check if task exists
        task = task_service.get_task(validated_id)
        if task is None:
            print_error(f"Task with ID {validated_id} not found.")
            return

        # Confirm deletion unless --yes flag is used
        if not yes:
            console.print(f"\n[yellow]About to delete task:[/yellow]")
            console.print(f"  ID: {task.id}")
            console.print(f"  Title: {task.title}")
            if click.confirm("\nAre you sure you want to delete this task?", default=False):
                pass
            else:
                console.print("[blue]Deletion cancelled.[/blue]")
                return

        # Delete task
        if task_service.delete_task(validated_id):
            print_success(f"Task {validated_id} deleted successfully")
        else:
            print_error(f"Failed to delete task {validated_id}")

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


@cli.command()
@click.argument("task_id")
def complete(task_id: str) -> None:
    """Mark a task as complete or incomplete (toggle).

    Examples:

        todo complete 1

        todo complete 2
    """
    try:
        # Validate task ID
        validated_id = validate_task_id(task_id)

        # Check if task exists
        task = task_service.get_task(validated_id)
        if task is None:
            print_error(f"Task with ID {validated_id} not found.")
            return

        # Toggle completion
        updated_task = task_service.toggle_completion(validated_id)

        if updated_task:
            if updated_task.completed:
                print_success(f"Task {validated_id} marked as complete")

                # Check if recurring task created next occurrence
                if updated_task.recurrence_pattern:
                    recurrence_val = updated_task.recurrence_pattern.value if hasattr(updated_task.recurrence_pattern, 'value') else updated_task.recurrence_pattern
                    console.print(
                        f"[blue]ℹ[/blue] Created next occurrence for recurring task "
                        f"({recurrence_val})"
                    )
            else:
                print_success(f"Task {validated_id} marked as incomplete")

            console.print(f"  Title: {updated_task.title}")
        else:
            print_error(f"Failed to update task {validated_id}")

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


@cli.command()
@click.argument("keyword")
def search(keyword: str) -> None:
    """Search tasks by keyword in title and description.

    Examples:

        todo search meeting

        todo search "Q1 goals"
    """
    try:
        if not keyword or not keyword.strip():
            print_error("Search keyword cannot be empty")
            return

        tasks = task_service.search_tasks(keyword.strip())

        if not tasks:
            print_info(f"No tasks found matching '{keyword}'")
            return

        table = format_task_table(tasks, title=f"Search Results for '{keyword}' ({len(tasks)} found)")
        console.print(table)

    except Exception as e:
        print_error(f"Error searching tasks: {e}")


@cli.command()
@click.argument(
    "sort_by",
    type=click.Choice(["priority", "due_date", "created_at", "title"], case_sensitive=False),
)
@click.option("--reverse", "-r", is_flag=True, help="Reverse sort order")
def sort(sort_by: str, reverse: bool) -> None:
    """Display tasks sorted by specified field.

    Examples:

        todo sort priority

        todo sort due_date

        todo sort title --reverse
    """
    try:
        tasks = task_service.get_all_tasks()

        if not tasks:
            print_info("No tasks to sort")
            return

        sorted_tasks = task_service.sort_tasks(tasks, sort_by.lower(), reverse=reverse)

        order = "descending" if reverse else "ascending"
        table = format_task_table(
            sorted_tasks, title=f"Tasks sorted by {sort_by} ({order})"
        )
        console.print(table)

    except Exception as e:
        print_error(f"Error sorting tasks: {e}")


if __name__ == "__main__":
    cli()
