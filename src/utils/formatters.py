"""Rich formatting utilities for beautiful console output."""

from datetime import datetime
from typing import List

from rich.console import Console
from rich.table import Table

from src.models.task import Task

console = Console()


def format_task_table(tasks: List[Task], title: str = "Tasks") -> Table:
    """Format tasks as a Rich table.

    Args:
        tasks: List of tasks to format
        title: Table title

    Returns:
        Rich Table object ready for display
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")

    # Define columns
    table.add_column("ID", style="cyan", justify="right", width=5)
    table.add_column("Title", style="white", width=30)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Categories", style="yellow", width=20)
    table.add_column("Due Date", style="blue", width=16)

    # Add rows
    for task in tasks:
        status = "✓ Done" if task.completed else "○ Pending"
        status_style = "green" if task.completed else "white"

        # Handle priority (could be enum or string due to use_enum_values)
        priority_value = task.priority.value if hasattr(task.priority, 'value') else task.priority
        priority_style = {
            "HIGH": "red bold",
            "MEDIUM": "yellow",
            "LOW": "blue",
        }.get(priority_value, "white")

        categories_str = ", ".join(task.categories) if task.categories else "-"
        due_date_str = format_datetime(task.due_date) if task.due_date else "-"

        table.add_row(
            str(task.id),
            task.title[:28] + "..." if len(task.title) > 30 else task.title,
            f"[{status_style}]{status}[/{status_style}]",
            f"[{priority_style}]{priority_value}[/{priority_style}]",
            categories_str,
            due_date_str,
        )

    return table


def format_task_detail(task: Task) -> None:
    """Display detailed task information.

    Args:
        task: Task to display
    """
    console.print("\n[bold cyan]Task Details[/bold cyan]")
    console.print(f"[bold]ID:[/bold] {task.id}")
    console.print(f"[bold]Title:[/bold] {task.title}")

    if task.description:
        console.print(f"[bold]Description:[/bold] {task.description}")

    status = "✓ Completed" if task.completed else "○ Pending"
    status_style = "green" if task.completed else "white"
    console.print(f"[bold]Status:[/bold] [{status_style}]{status}[/{status_style}]")

    # Handle priority (could be enum or string due to use_enum_values)
    priority_value = task.priority.value if hasattr(task.priority, 'value') else task.priority
    priority_style = {
        "HIGH": "red bold",
        "MEDIUM": "yellow",
        "LOW": "blue",
    }.get(priority_value, "white")
    console.print(f"[bold]Priority:[/bold] [{priority_style}]{priority_value}[/{priority_style}]")

    if task.categories:
        console.print(f"[bold]Categories:[/bold] {', '.join(task.categories)}")

    if task.due_date:
        console.print(f"[bold]Due Date:[/bold] {format_datetime(task.due_date)}")

    if task.recurrence_pattern:
        # Handle recurrence (could be enum or string due to use_enum_values)
        recurrence_value = task.recurrence_pattern.value if hasattr(task.recurrence_pattern, 'value') else task.recurrence_pattern
        console.print(f"[bold]Recurrence:[/bold] {recurrence_value}")

    console.print(f"[bold]Created:[/bold] {format_datetime(task.created_at)}")
    console.print(f"[bold]Updated:[/bold] {format_datetime(task.updated_at)}")
    console.print()


def format_datetime(dt: datetime) -> str:
    """Format datetime for display.

    Args:
        dt: Datetime to format

    Returns:
        Formatted datetime string
    """
    return dt.strftime("%Y-%m-%d %H:%M")


def print_success(message: str) -> None:
    """Print success message.

    Args:
        message: Success message to display
    """
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message.

    Args:
        message: Error message to display
    """
    console.print(f"[red]✗[/red] {message}", style="bold red")


def print_warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Warning message to display
    """
    console.print(f"[yellow]⚠[/yellow] {message}", style="bold yellow")


def print_info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message to display
    """
    console.print(f"[blue]ℹ[/blue] {message}", style="blue")
