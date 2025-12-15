"""Date parsing utilities for natural language date inputs."""

from datetime import datetime, timedelta
from typing import Optional

from dateutil import parser as dateutil_parser


def parse_date(date_string: str) -> datetime:
    """Parse natural language date string into datetime.

    Supports formats:
    - ISO format: "2025-01-15", "2025-01-15 14:30"
    - Natural language: "tomorrow", "next monday", "in 3 days"
    - Relative: "today", "tomorrow"

    Args:
        date_string: Date string to parse

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If date string cannot be parsed
    """
    date_string = date_string.lower().strip()

    # Handle relative dates
    now = datetime.now()

    if date_string in ["today", "now"]:
        return now

    if date_string == "tomorrow":
        return now + timedelta(days=1)

    if date_string == "yesterday":
        return now - timedelta(days=1)

    # Handle "in X days/weeks/months"
    if date_string.startswith("in "):
        try:
            return parse_relative_date(date_string)
        except ValueError:
            pass

    # Handle "next <day of week>"
    if date_string.startswith("next "):
        try:
            return parse_next_weekday(date_string)
        except ValueError:
            pass

    # Try dateutil parser for complex formats
    try:
        parsed_date = dateutil_parser.parse(date_string, fuzzy=True)
        return parsed_date
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Unable to parse date '{date_string}'. "
            f"Try formats like: '2025-01-15', 'tomorrow', 'next monday', 'in 3 days'"
        ) from e


def parse_relative_date(date_string: str) -> datetime:
    """Parse relative date like 'in 3 days'.

    Args:
        date_string: Relative date string

    Returns:
        Parsed datetime

    Raises:
        ValueError: If format is invalid
    """
    parts = date_string.split()
    if len(parts) != 3 or parts[0] != "in":
        raise ValueError("Invalid relative date format")

    try:
        amount = int(parts[1])
    except ValueError as e:
        raise ValueError("Invalid number in relative date") from e

    unit = parts[2].lower()
    now = datetime.now()

    if unit in ["day", "days"]:
        return now + timedelta(days=amount)
    elif unit in ["week", "weeks"]:
        return now + timedelta(weeks=amount)
    elif unit in ["month", "months"]:
        # Approximate month as 30 days
        return now + timedelta(days=amount * 30)
    elif unit in ["hour", "hours"]:
        return now + timedelta(hours=amount)
    else:
        raise ValueError(f"Unsupported time unit: {unit}")


def parse_next_weekday(date_string: str) -> datetime:
    """Parse 'next <weekday>' format.

    Args:
        date_string: Next weekday string

    Returns:
        Parsed datetime

    Raises:
        ValueError: If weekday is invalid
    """
    parts = date_string.split()
    if len(parts) != 2 or parts[0] != "next":
        raise ValueError("Invalid next weekday format")

    weekday_name = parts[1].lower()
    weekday_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    if weekday_name not in weekday_map:
        raise ValueError(f"Invalid weekday: {weekday_name}")

    target_weekday = weekday_map[weekday_name]
    now = datetime.now()
    current_weekday = now.weekday()

    # Calculate days until next occurrence
    days_ahead = target_weekday - current_weekday
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    return now + timedelta(days=days_ahead)


def format_date_relative(dt: datetime) -> str:
    """Format datetime as relative string when appropriate.

    Args:
        dt: Datetime to format

    Returns:
        Formatted relative date string
    """
    now = datetime.now()
    delta = dt - now

    if delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days == -1:
        return "Yesterday"
    elif 0 < delta.days < 7:
        return f"In {delta.days} days"
    else:
        return dt.strftime("%Y-%m-%d %H:%M")
