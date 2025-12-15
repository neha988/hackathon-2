"""Unit tests for validators."""

import pytest

from src.utils.validators import (
    validate_categories,
    validate_description,
    validate_priority,
    validate_recurrence_pattern,
    validate_task_id,
    validate_title,
)


class TestValidateTitle:
    """Test title validation."""

    def test_validate_title_valid(self):
        """Test validating a valid title."""
        result = validate_title("  Test Task  ")
        assert result == "Test Task"

    def test_validate_title_strips_whitespace(self):
        """Test that title strips leading/trailing whitespace."""
        result = validate_title("   Task   ")
        assert result == "Task"

    def test_validate_title_empty_raises_error(self):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_title("")

    def test_validate_title_whitespace_only_raises_error(self):
        """Test that whitespace-only title raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_title("   ")

    def test_validate_title_too_long_raises_error(self):
        """Test that title > 200 chars raises error."""
        long_title = "x" * 201
        with pytest.raises(ValueError, match="cannot exceed 200 characters"):
            validate_title(long_title)

    def test_validate_title_exactly_200_chars(self):
        """Test that title with exactly 200 chars is valid."""
        title_200 = "x" * 200
        result = validate_title(title_200)
        assert len(result) == 200


class TestValidateDescription:
    """Test description validation."""

    def test_validate_description_valid(self):
        """Test validating a valid description."""
        result = validate_description("  Test description  ")
        assert result == "Test description"

    def test_validate_description_empty(self):
        """Test that empty description is valid."""
        result = validate_description("")
        assert result == ""

    def test_validate_description_strips_whitespace(self):
        """Test that description strips whitespace."""
        result = validate_description("   Description   ")
        assert result == "Description"

    def test_validate_description_too_long_raises_error(self):
        """Test that description > 1000 chars raises error."""
        long_desc = "x" * 1001
        with pytest.raises(ValueError, match="cannot exceed 1000 characters"):
            validate_description(long_desc)

    def test_validate_description_exactly_1000_chars(self):
        """Test that description with exactly 1000 chars is valid."""
        desc_1000 = "x" * 1000
        result = validate_description(desc_1000)
        assert len(result) == 1000


class TestValidatePriority:
    """Test priority validation."""

    def test_validate_priority_high(self):
        """Test validating HIGH priority."""
        assert validate_priority("HIGH") == "HIGH"
        assert validate_priority("high") == "HIGH"
        assert validate_priority("High") == "HIGH"

    def test_validate_priority_medium(self):
        """Test validating MEDIUM priority."""
        assert validate_priority("MEDIUM") == "MEDIUM"
        assert validate_priority("medium") == "MEDIUM"

    def test_validate_priority_low(self):
        """Test validating LOW priority."""
        assert validate_priority("LOW") == "LOW"
        assert validate_priority("low") == "LOW"

    def test_validate_priority_case_insensitive(self):
        """Test that priority validation is case insensitive."""
        assert validate_priority("HiGh") == "HIGH"
        assert validate_priority("MeDiUm") == "MEDIUM"

    def test_validate_priority_invalid_raises_error(self):
        """Test that invalid priority raises error."""
        with pytest.raises(ValueError, match="Invalid priority"):
            validate_priority("INVALID")

    def test_validate_priority_empty_raises_error(self):
        """Test that empty priority raises error."""
        with pytest.raises(ValueError, match="Invalid priority"):
            validate_priority("")


class TestValidateRecurrencePattern:
    """Test recurrence pattern validation."""

    def test_validate_recurrence_daily(self):
        """Test validating DAILY recurrence."""
        assert validate_recurrence_pattern("DAILY") == "DAILY"
        assert validate_recurrence_pattern("daily") == "DAILY"

    def test_validate_recurrence_weekly(self):
        """Test validating WEEKLY recurrence."""
        assert validate_recurrence_pattern("WEEKLY") == "WEEKLY"
        assert validate_recurrence_pattern("weekly") == "WEEKLY"

    def test_validate_recurrence_monthly(self):
        """Test validating MONTHLY recurrence."""
        assert validate_recurrence_pattern("MONTHLY") == "MONTHLY"
        assert validate_recurrence_pattern("monthly") == "MONTHLY"

    def test_validate_recurrence_case_insensitive(self):
        """Test that recurrence validation is case insensitive."""
        assert validate_recurrence_pattern("DaiLy") == "DAILY"

    def test_validate_recurrence_invalid_raises_error(self):
        """Test that invalid recurrence raises error."""
        with pytest.raises(ValueError, match="Invalid recurrence pattern"):
            validate_recurrence_pattern("YEARLY")


class TestValidateCategories:
    """Test categories validation."""

    def test_validate_categories_valid(self):
        """Test validating valid categories."""
        result = validate_categories(["work", "urgent"])
        assert result == ["work", "urgent"]

    def test_validate_categories_strips_whitespace(self):
        """Test that categories strip whitespace."""
        result = validate_categories(["  work  ", "  urgent  "])
        assert result == ["work", "urgent"]

    def test_validate_categories_converts_to_lowercase(self):
        """Test that categories are converted to lowercase."""
        result = validate_categories(["WORK", "Urgent", "Personal"])
        assert result == ["work", "urgent", "personal"]

    def test_validate_categories_empty_list(self):
        """Test that empty list returns empty list."""
        result = validate_categories([])
        assert result == []

    def test_validate_categories_none(self):
        """Test that None returns empty list."""
        result = validate_categories(None)
        assert result == []

    def test_validate_categories_filters_empty_strings(self):
        """Test that empty strings are filtered out."""
        result = validate_categories(["work", "   ", "urgent", ""])
        assert result == ["work", "urgent"]

    def test_validate_categories_too_long_raises_error(self):
        """Test that category > 50 chars raises error."""
        long_category = "x" * 51
        with pytest.raises(ValueError, match="exceeds 50 characters"):
            validate_categories([long_category])

    def test_validate_categories_with_comma_raises_error(self):
        """Test that category with comma raises error."""
        with pytest.raises(ValueError, match="cannot contain commas"):
            validate_categories(["work,urgent"])

    def test_validate_categories_mixed_valid_invalid(self):
        """Test validation with mix of valid and invalid categories."""
        # First category is valid, second has comma
        with pytest.raises(ValueError, match="cannot contain commas"):
            validate_categories(["work", "urgent,important"])


class TestValidateTaskId:
    """Test task ID validation."""

    def test_validate_task_id_valid(self):
        """Test validating valid task IDs."""
        assert validate_task_id("1") == 1
        assert validate_task_id("42") == 42
        assert validate_task_id("999") == 999

    def test_validate_task_id_zero_raises_error(self):
        """Test that task ID 0 raises error."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            validate_task_id("0")

    def test_validate_task_id_negative_raises_error(self):
        """Test that negative task ID raises error."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            validate_task_id("-1")

    def test_validate_task_id_not_integer_raises_error(self):
        """Test that non-integer task ID raises error."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            validate_task_id("abc")

    def test_validate_task_id_float_raises_error(self):
        """Test that float task ID raises error."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            validate_task_id("1.5")

    def test_validate_task_id_empty_raises_error(self):
        """Test that empty task ID raises error."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            validate_task_id("")
