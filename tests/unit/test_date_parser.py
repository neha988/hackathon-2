"""Unit tests for date parser."""

from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from src.utils.date_parser import (
    format_date_relative,
    parse_date,
    parse_next_weekday,
    parse_relative_date,
)


class TestParseDate:
    """Test date parsing."""

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_date_today(self):
        """Test parsing 'today'."""
        result = parse_date("today")
        expected = datetime(2025, 1, 15, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_date_now(self):
        """Test parsing 'now'."""
        result = parse_date("now")
        expected = datetime(2025, 1, 15, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_date_tomorrow(self):
        """Test parsing 'tomorrow'."""
        result = parse_date("tomorrow")
        expected = datetime(2025, 1, 16, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_date_yesterday(self):
        """Test parsing 'yesterday'."""
        result = parse_date("yesterday")
        expected = datetime(2025, 1, 14, 12, 0, 0)
        assert result.date() == expected.date()

    def test_parse_date_iso_format(self):
        """Test parsing ISO format date."""
        result = parse_date("2025-12-31")
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 31

    def test_parse_date_iso_format_with_time(self):
        """Test parsing ISO format with time."""
        result = parse_date("2025-12-31 23:59:00")
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 31
        assert result.hour == 23
        assert result.minute == 59

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_date_in_3_days(self):
        """Test parsing 'in 3 days'."""
        result = parse_date("in 3 days")
        expected = datetime(2025, 1, 18, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_date_in_2_weeks(self):
        """Test parsing 'in 2 weeks'."""
        result = parse_date("in 2 weeks")
        expected = datetime(2025, 1, 29, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")  # Wednesday
    def test_parse_date_next_monday(self):
        """Test parsing 'next monday'."""
        result = parse_date("next monday")
        assert result.weekday() == 0  # Monday
        assert result.date() == datetime(2025, 1, 20).date()

    @freeze_time("2025-01-15 12:00:00")  # Wednesday
    def test_parse_date_next_friday(self):
        """Test parsing 'next friday'."""
        result = parse_date("next friday")
        assert result.weekday() == 4  # Friday
        assert result.date() == datetime(2025, 1, 17).date()

    def test_parse_date_case_insensitive(self):
        """Test that parsing is case insensitive."""
        result1 = parse_date("TODAY")
        result2 = parse_date("Today")
        result3 = parse_date("today")
        assert result1.date() == result2.date() == result3.date()

    def test_parse_date_invalid_raises_error(self):
        """Test that invalid date string raises error."""
        with pytest.raises(ValueError, match="Unable to parse date"):
            parse_date("invalid date string xyz")


class TestParseRelativeDate:
    """Test relative date parsing."""

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_relative_date_days(self):
        """Test parsing relative days."""
        result = parse_relative_date("in 5 days")
        expected = datetime(2025, 1, 20, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_relative_date_weeks(self):
        """Test parsing relative weeks."""
        result = parse_relative_date("in 3 weeks")
        expected = datetime(2025, 2, 5, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_relative_date_months(self):
        """Test parsing relative months (approximated)."""
        result = parse_relative_date("in 2 months")
        # Months are approximated as 30 days
        expected = datetime(2025, 3, 16, 12, 0, 0)
        assert result.date() == expected.date()

    @freeze_time("2025-01-15 12:00:00")
    def test_parse_relative_date_hours(self):
        """Test parsing relative hours."""
        result = parse_relative_date("in 6 hours")
        expected = datetime(2025, 1, 15, 18, 0, 0)
        assert result == expected

    def test_parse_relative_date_invalid_format_raises_error(self):
        """Test that invalid format raises error."""
        with pytest.raises(ValueError):
            parse_relative_date("5 days")  # Missing "in"

    def test_parse_relative_date_invalid_number_raises_error(self):
        """Test that invalid number raises error."""
        with pytest.raises(ValueError):
            parse_relative_date("in abc days")

    def test_parse_relative_date_invalid_unit_raises_error(self):
        """Test that invalid time unit raises error."""
        with pytest.raises(ValueError, match="Unsupported time unit"):
            parse_relative_date("in 5 years")


class TestParseNextWeekday:
    """Test next weekday parsing."""

    @freeze_time("2025-01-15 12:00:00")  # Wednesday
    def test_parse_next_weekday_monday(self):
        """Test parsing next Monday."""
        result = parse_next_weekday("next monday")
        assert result.weekday() == 0
        assert result.date() == datetime(2025, 1, 20).date()

    @freeze_time("2025-01-15 12:00:00")  # Wednesday
    def test_parse_next_weekday_friday(self):
        """Test parsing next Friday."""
        result = parse_next_weekday("next friday")
        assert result.weekday() == 4
        assert result.date() == datetime(2025, 1, 17).date()

    @freeze_time("2025-01-15 12:00:00")  # Wednesday
    def test_parse_next_weekday_wednesday_skips_to_next_week(self):
        """Test that next wednesday skips to next week."""
        result = parse_next_weekday("next wednesday")
        assert result.weekday() == 2
        assert result.date() == datetime(2025, 1, 22).date()

    @freeze_time("2025-01-15 12:00:00")  # Wednesday
    def test_parse_next_weekday_all_days(self):
        """Test parsing all weekdays."""
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, weekday in enumerate(weekdays):
            result = parse_next_weekday(f"next {weekday}")
            assert result.weekday() == i

    def test_parse_next_weekday_invalid_format_raises_error(self):
        """Test that invalid format raises error."""
        with pytest.raises(ValueError):
            parse_next_weekday("monday")  # Missing "next"

    def test_parse_next_weekday_invalid_day_raises_error(self):
        """Test that invalid weekday raises error."""
        with pytest.raises(ValueError, match="Invalid weekday"):
            parse_next_weekday("next invalidday")


class TestFormatDateRelative:
    """Test relative date formatting."""

    @freeze_time("2025-01-15 12:00:00")
    def test_format_date_relative_today(self):
        """Test formatting today as relative."""
        dt = datetime(2025, 1, 15, 14, 30)
        result = format_date_relative(dt)
        assert result == "Today"

    @freeze_time("2025-01-15 12:00:00")
    def test_format_date_relative_tomorrow(self):
        """Test formatting tomorrow as relative."""
        dt = datetime(2025, 1, 16, 14, 30)
        result = format_date_relative(dt)
        assert result == "Tomorrow"

    @freeze_time("2025-01-15 12:00:00")
    def test_format_date_relative_yesterday(self):
        """Test formatting yesterday as relative."""
        dt = datetime(2025, 1, 14, 14, 30)
        result = format_date_relative(dt)
        assert result == "Yesterday"

    @freeze_time("2025-01-15 12:00:00")
    def test_format_date_relative_in_3_days(self):
        """Test formatting date in 3 days as relative."""
        dt = datetime(2025, 1, 18, 14, 30)
        result = format_date_relative(dt)
        assert result == "In 3 days"

    @freeze_time("2025-01-15 12:00:00")
    def test_format_date_relative_beyond_week(self):
        """Test formatting date beyond a week shows absolute."""
        dt = datetime(2025, 2, 1, 14, 30)
        result = format_date_relative(dt)
        assert result == "2025-02-01 14:30"

    @freeze_time("2025-01-15 12:00:00")
    def test_format_date_relative_past_beyond_yesterday(self):
        """Test formatting past date shows absolute."""
        dt = datetime(2025, 1, 10, 14, 30)
        result = format_date_relative(dt)
        assert result == "2025-01-10 14:30"
