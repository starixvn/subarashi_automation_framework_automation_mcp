"""
Unit tests for src/Core/exceptions.py

Tests all custom exception classes to ensure proper behavior,
inheritance, and error message formatting.
"""

import pytest

from src.Core.exceptions import (
    AutomationError,
    ElementError,
    NavigationError,
    ValidationError,
)


class TestAutomationError:
    """Test AutomationError base exception class."""

    def test_create_with_message_only(self) -> None:
        """Test creating AutomationError with message only."""
        error = AutomationError("Test error message")
        assert error.message == "Test error message"
        assert error.details is None
        assert str(error) == "Test error message"

    def test_create_with_message_and_details(self) -> None:
        """Test creating AutomationError with message and details."""
        error = AutomationError("Test error", "Additional details")
        assert error.message == "Test error"
        assert error.details == "Additional details"
        assert str(error) == "Test error: Additional details"

    def test_string_representation_without_details(self) -> None:
        """Test __str__ method without details."""
        error = AutomationError("Simple error")
        assert str(error) == "Simple error"

    def test_string_representation_with_details(self) -> None:
        """Test __str__ method with details."""
        error = AutomationError("Error occurred", "Stack trace here")
        assert str(error) == "Error occurred: Stack trace here"

    def test_inherits_from_exception(self) -> None:
        """Test AutomationError inherits from Exception."""
        error = AutomationError("Test")
        assert isinstance(error, Exception)

    def test_can_be_raised(self) -> None:
        """Test AutomationError can be raised."""
        with pytest.raises(AutomationError) as exc_info:
            raise AutomationError("Test error")
        assert str(exc_info.value) == "Test error"

    def test_can_be_caught(self) -> None:
        """Test AutomationError can be caught."""
        try:
            raise AutomationError("Test error", "Details")
        except AutomationError as e:
            assert e.message == "Test error"
            assert e.details == "Details"

    def test_with_none_details(self) -> None:
        """Test with explicitly None details."""
        error = AutomationError("Message", None)
        assert error.details is None
        assert str(error) == "Message"

    def test_with_empty_string_details(self) -> None:
        """Test with empty string details."""
        error = AutomationError("Message", "")
        assert error.details == ""
        assert str(error) == "Message"

    def test_with_special_characters(self) -> None:
        """Test with special characters in message."""
        special_msg = "Error: <element> not found @ line #123!"
        error = AutomationError(special_msg)
        assert str(error) == special_msg

    def test_with_unicode_characters(self) -> None:
        """Test with unicode characters."""
        unicode_msg = "错误: элемент không tìm thấy"
        error = AutomationError(unicode_msg)
        assert str(error) == unicode_msg

    def test_exception_chaining(self) -> None:
        """Test exception chaining with 'raise from'."""
        original = ValueError("Original error")
        try:
            try:
                raise original
            except ValueError as e:
                raise AutomationError("Wrapped error") from e
        except AutomationError as ae:
            assert str(ae) == "Wrapped error"
            assert ae.__cause__ == original

    def test_multiple_exception_types(self) -> None:
        """Test catching multiple exception types."""
        with pytest.raises((AutomationError, ValueError)):
            raise AutomationError("Test")

    def test_exception_attributes_access(self) -> None:
        """Test accessing exception attributes."""
        error = AutomationError("Test message", "Test details")
        assert hasattr(error, "message")
        assert hasattr(error, "details")
        assert hasattr(error, "args")

    def test_exception_repr(self) -> None:
        """Test exception repr."""
        error = AutomationError("Test")
        repr_str = repr(error)
        assert "AutomationError" in repr_str or "Test" in repr_str


class TestElementError:
    """Test ElementError exception class."""

    def test_inherits_from_automation_error(self) -> None:
        """Test ElementError inherits from AutomationError."""
        error = ElementError("Test")
        assert isinstance(error, AutomationError)
        assert isinstance(error, Exception)

    def test_create_element_error(self) -> None:
        """Test creating ElementError."""
        error = ElementError("Element not found")
        assert error.message == "Element not found"

    def test_create_with_details(self) -> None:
        """Test creating ElementError with details."""
        error = ElementError("Element not found", "Selector: #submit-btn")
        assert error.message == "Element not found"
        assert error.details == "Selector: #submit-btn"
        assert str(error) == "Element not found: Selector: #submit-btn"

    def test_can_be_raised_as_element_error(self) -> None:
        """Test ElementError can be raised and caught specifically."""
        with pytest.raises(ElementError):
            raise ElementError("Test")

    def test_can_be_caught_as_automation_error(self) -> None:
        """Test ElementError can be caught as AutomationError."""
        with pytest.raises(AutomationError):
            raise ElementError("Test")

    def test_distinguishable_from_other_errors(self) -> None:
        """Test ElementError is distinguishable from other error types."""
        element_error = ElementError("Test")
        assert type(element_error).__name__ == "ElementError"
        assert not isinstance(element_error, NavigationError)
        assert not isinstance(element_error, ValidationError)


class TestNavigationError:
    """Test NavigationError exception class."""

    def test_inherits_from_automation_error(self) -> None:
        """Test NavigationError inherits from AutomationError."""
        error = NavigationError("Test")
        assert isinstance(error, AutomationError)
        assert isinstance(error, Exception)

    def test_create_navigation_error(self) -> None:
        """Test creating NavigationError."""
        error = NavigationError("Failed to navigate")
        assert error.message == "Failed to navigate"

    def test_create_with_details(self) -> None:
        """Test creating NavigationError with details."""
        error = NavigationError("Navigation failed", "URL: https://example.com")
        assert error.message == "Navigation failed"
        assert error.details == "URL: https://example.com"

    def test_can_be_raised_as_navigation_error(self) -> None:
        """Test NavigationError can be raised and caught specifically."""
        with pytest.raises(NavigationError):
            raise NavigationError("Test")

    def test_can_be_caught_as_automation_error(self) -> None:
        """Test NavigationError can be caught as AutomationError."""
        with pytest.raises(AutomationError):
            raise NavigationError("Test")

    def test_distinguishable_from_other_errors(self) -> None:
        """Test NavigationError is distinguishable from other error types."""
        nav_error = NavigationError("Test")
        assert type(nav_error).__name__ == "NavigationError"
        assert not isinstance(nav_error, ElementError)
        assert not isinstance(nav_error, ValidationError)


class TestValidationError:
    """Test ValidationError exception class."""

    def test_inherits_from_automation_error(self) -> None:
        """Test ValidationError inherits from AutomationError."""
        error = ValidationError("Test")
        assert isinstance(error, AutomationError)
        assert isinstance(error, Exception)

    def test_create_validation_error(self) -> None:
        """Test creating ValidationError."""
        error = ValidationError("Validation failed")
        assert error.message == "Validation failed"

    def test_create_with_details(self) -> None:
        """Test creating ValidationError with details."""
        error = ValidationError("Validation failed", "Expected: 'test', Got: 'prod'")
        assert error.message == "Validation failed"
        assert error.details == "Expected: 'test', Got: 'prod'"

    def test_can_be_raised_as_validation_error(self) -> None:
        """Test ValidationError can be raised and caught specifically."""
        with pytest.raises(ValidationError):
            raise ValidationError("Test")

    def test_can_be_caught_as_automation_error(self) -> None:
        """Test ValidationError can be caught as AutomationError."""
        with pytest.raises(AutomationError):
            raise ValidationError("Test")

    def test_distinguishable_from_other_errors(self) -> None:
        """Test ValidationError is distinguishable from other error types."""
        val_error = ValidationError("Test")
        assert type(val_error).__name__ == "ValidationError"
        assert not isinstance(val_error, ElementError)
        assert not isinstance(val_error, NavigationError)


class TestExceptionHierarchy:
    """Test exception hierarchy and relationships."""

    def test_all_inherit_from_automation_error(self) -> None:
        """Test all custom exceptions inherit from AutomationError."""
        errors = [
            ElementError("test"),
            NavigationError("test"),
            ValidationError("test"),
        ]
        for error in errors:
            assert isinstance(error, AutomationError)

    def test_all_inherit_from_exception(self) -> None:
        """Test all custom exceptions inherit from Exception."""
        errors = [
            AutomationError("test"),
            ElementError("test"),
            NavigationError("test"),
            ValidationError("test"),
        ]
        for error in errors:
            assert isinstance(error, Exception)

    def test_specific_exception_catching(self) -> None:
        """Test catching specific exception types."""
        # ElementError
        with pytest.raises(ElementError):
            raise ElementError("test")

        # NavigationError
        with pytest.raises(NavigationError):
            raise NavigationError("test")

        # ValidationError
        with pytest.raises(ValidationError):
            raise ValidationError("test")

    def test_generic_exception_catching(self) -> None:
        """Test catching using base AutomationError."""
        exceptions = [
            ElementError("test"),
            NavigationError("test"),
            ValidationError("test"),
        ]

        for exc in exceptions:
            with pytest.raises(AutomationError):
                raise exc

    def test_exception_type_checking(self) -> None:
        """Test type checking for different exception types."""
        element_error = ElementError("test")
        nav_error = NavigationError("test")
        val_error = ValidationError("test")

        assert type(element_error) is ElementError
        assert type(nav_error) is NavigationError
        assert type(val_error) is ValidationError

        assert type(element_error) is not type(nav_error)
        assert type(nav_error) is not type(val_error)
        assert type(val_error) is not type(element_error)
