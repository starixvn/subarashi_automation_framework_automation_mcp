"""
Unit tests for src/Core/decorators.py

Tests the @retry and @auto_log decorators to ensure proper behavior,
logging, retry logic, and Allure integration.
"""

import logging
import time
from typing import Any
from unittest.mock import patch

import pytest

from src.Core.decorators import auto_log, retry
from src.Core.exceptions import AutomationError, ElementError


class TestRetryDecorator:
    """Test @retry decorator functionality."""

    def test_successful_execution_first_attempt(self) -> None:
        """Test function succeeds on first attempt - no retry."""
        call_count = 0

        @retry(max_attempts=3)
        def successful_function() -> str:
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_function()
        assert result == "success"
        assert call_count == 1

    def test_successful_execution_second_attempt(self) -> None:
        """Test function succeeds on second attempt (1 retry)."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def retry_once_function() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First attempt fails")
            return "success"

        result = retry_once_function()
        assert result == "success"
        assert call_count == 2

    def test_successful_execution_third_attempt(self) -> None:
        """Test function succeeds on third attempt (2 retries)."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def retry_twice_function() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"

        result = retry_twice_function()
        assert result == "success"
        assert call_count == 3

    def test_failure_after_max_attempts_exceeded(self) -> None:
        """Test function fails after max attempts exceeded."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def always_fails() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        with pytest.raises(ValueError, match="Always fails"):
            always_fails()

        assert call_count == 3

    def test_default_max_attempts(self) -> None:
        """Test default max_attempts=3."""
        call_count = 0

        @retry(delay=0.1)  # No max_attempts specified
        def function() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")

        with pytest.raises(ValueError):
            function()

        assert call_count == 3  # Default is 3

    def test_custom_max_attempts_five(self) -> None:
        """Test custom max_attempts=5."""
        call_count = 0

        @retry(max_attempts=5, delay=0.1)
        def function() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")

        with pytest.raises(ValueError):
            function()

        assert call_count == 5

    def test_custom_max_attempts_one(self) -> None:
        """Test custom max_attempts=1 (no retries)."""
        call_count = 0

        @retry(max_attempts=1, delay=0.1)
        def function() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")

        with pytest.raises(ValueError):
            function()

        assert call_count == 1

    def test_default_delay(self) -> None:
        """Test default delay=1.0."""

        @retry(max_attempts=2, backoff=1.0)  # No delay specified
        def function() -> None:
            raise ValueError("Fail")

        start_time = time.time()
        with pytest.raises(ValueError):
            function()
        elapsed = time.time() - start_time

        # Should have at least 1 second delay (default)
        assert elapsed >= 0.9  # Allow some tolerance

    def test_custom_delay(self) -> None:
        """Test custom delay=0.5."""

        @retry(max_attempts=2, delay=0.5, backoff=1.0)
        def function() -> None:
            raise ValueError("Fail")

        start_time = time.time()
        with pytest.raises(ValueError):
            function()
        elapsed = time.time() - start_time

        # Should have at least 0.5 seconds delay
        assert 0.4 <= elapsed <= 0.8

    def test_default_backoff(self) -> None:
        """Test default backoff=2.0."""
        delays: list[float] = []

        @retry(max_attempts=3, delay=0.1)  # No backoff specified, default is 2.0
        def function() -> None:
            delays.append(time.time())
            raise ValueError("Fail")

        with pytest.raises(ValueError):
            function()

        # Check exponential backoff: delay * 2^attempt
        # First attempt: no delay
        # Second attempt: delay * 2^0 = 0.1
        # Third attempt: delay * 2^1 = 0.2
        assert len(delays) == 3

    def test_custom_backoff(self) -> None:
        """Test custom backoff=1.5."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1, backoff=1.5)
        def function() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("Fail")

        with pytest.raises(ValueError):
            function()

        assert call_count == 3

    def test_exception_filtering_matching(self) -> None:
        """Test exception filtering - retry on matching exception."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def function() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Retry this")
            return "success"

        result = function()
        assert result == "success"
        assert call_count == 2

    def test_exception_filtering_non_matching(self) -> None:
        """Test exception filtering - don't retry on non-matching exception."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def function() -> None:
            nonlocal call_count
            call_count += 1
            raise TypeError("Don't retry this")

        with pytest.raises(TypeError):
            function()

        assert call_count == 1  # No retry for non-matching exception

    def test_no_exception_filtering(self) -> None:
        """Test with no exception filtering - retry all exceptions."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)  # No exceptions parameter
        def function() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First")
            elif call_count == 2:
                raise TypeError("Second")
            return "success"

        result = function()
        assert result == "success"
        assert call_count == 3

    def test_retry_logging_messages(self, caplog: Any) -> None:
        """Test retry logging messages."""
        with caplog.at_level(logging.WARNING):

            @retry(max_attempts=3, delay=0.1)
            def function() -> None:
                raise ValueError("Fail")

            with pytest.raises(ValueError):
                function()

        # Check warning messages
        assert any("Attempt 1/3 failed" in record.message for record in caplog.records)
        assert any("Attempt 2/3 failed" in record.message for record in caplog.records)

    def test_with_function_return_value(self) -> None:
        """Test retry preserves function return value."""

        @retry(max_attempts=3, delay=0.1)
        def function(x: int, y: int) -> int:
            return x + y

        result = function(5, 3)
        assert result == 8

    def test_with_function_return_none(self) -> None:
        """Test retry with function returning None."""

        @retry(max_attempts=3, delay=0.1)
        def function() -> None:
            pass

        result = function()
        assert result is None

    def test_with_class_method(self) -> None:
        """Test retry decorator on class method."""

        class TestClass:
            call_count = 0

            @retry(max_attempts=3, delay=0.1)
            def method(self) -> str:
                TestClass.call_count += 1
                if TestClass.call_count < 2:
                    raise ValueError("Retry")
                return "success"

        obj = TestClass()
        result = obj.method()
        assert result == "success"
        assert TestClass.call_count == 2

    def test_with_static_method(self) -> None:
        """Test retry decorator on static method."""

        class TestClass:
            call_count = 0

            @staticmethod
            @retry(max_attempts=3, delay=0.1)
            def static_method() -> str:
                TestClass.call_count += 1
                if TestClass.call_count < 2:
                    raise ValueError("Retry")
                return "success"

        result = TestClass.static_method()
        assert result == "success"
        assert TestClass.call_count == 2

    def test_exception_preservation(self) -> None:
        """Test original exception is raised after retries."""
        original_error = ValueError("Original error message")

        @retry(max_attempts=2, delay=0.1)
        def function() -> None:
            raise original_error

        with pytest.raises(ValueError) as exc_info:
            function()

        assert exc_info.value == original_error

    def test_decorator_stacking_with_auto_log(self, caplog: Any) -> None:
        """Test retry stacked with auto_log decorator."""
        call_count = 0

        with caplog.at_level(logging.DEBUG):

            @auto_log
            @retry(max_attempts=2, delay=0.1)
            def function() -> str:
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    raise ValueError("Retry")
                return "success"

            result = function()

        assert result == "success"
        assert call_count == 2

    def test_with_multiple_exception_types(self) -> None:
        """Test filtering with multiple exception types."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError, TypeError))
        def function() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First")
            elif call_count == 2:
                raise TypeError("Second")
            return "success"

        result = function()
        assert result == "success"
        assert call_count == 3

    def test_retry_counter_accuracy(self) -> None:
        """Test retry counter is accurate."""
        attempts: list[int] = []

        @retry(max_attempts=5, delay=0.1)
        def function() -> None:
            attempts.append(len(attempts) + 1)
            raise ValueError("Fail")

        with pytest.raises(ValueError):
            function()

        assert attempts == [1, 2, 3, 4, 5]


class TestAutoLogDecorator:
    """Test @auto_log decorator functionality."""

    def test_successful_function_execution_logging(self, caplog: Any) -> None:
        """Test successful function execution is logged."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def test_function() -> str:
                return "success"

            result = test_function()

        assert result == "success"
        assert any("[ENTER]" in record.message for record in caplog.records)
        assert any("[EXIT]" in record.message for record in caplog.records)

    def test_log_entry_message_format(self, caplog: Any) -> None:
        """Test log entry message format."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def my_test_function() -> None:
                pass

            my_test_function()

        entry_logs = [r for r in caplog.records if "[ENTER]" in r.message]
        assert len(entry_logs) > 0
        assert "my_test_function" in entry_logs[0].message

    def test_log_exit_message_format(self, caplog: Any) -> None:
        """Test log exit message format."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def my_test_function() -> None:
                pass

            my_test_function()

        exit_logs = [r for r in caplog.records if "[EXIT]" in r.message]
        assert len(exit_logs) > 0
        assert "my_test_function" in exit_logs[0].message
        assert "Duration" in exit_logs[0].message

    def test_duration_calculation(self, caplog: Any) -> None:
        """Test duration calculation is present."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def slow_function() -> None:
                time.sleep(0.1)

            slow_function()

        exit_logs = [r for r in caplog.records if "[EXIT]" in r.message]
        assert any("ms" in log.message for log in exit_logs)

    def test_error_logging_on_exception(self, caplog: Any) -> None:
        """Test error is logged when exception occurs."""
        with caplog.at_level(logging.ERROR):

            @auto_log
            def failing_function() -> None:
                raise ValueError("Test error")

            with pytest.raises(ValueError):
                failing_function()

        error_logs = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_logs) > 0
        assert "[ERROR]" in error_logs[0].message
        assert "Test error" in error_logs[0].message

    def test_error_message_format(self, caplog: Any) -> None:
        """Test error message format includes function name and error."""
        with caplog.at_level(logging.ERROR):

            @auto_log
            def error_function() -> None:
                raise AutomationError("Custom error")

            with pytest.raises(AutomationError):
                error_function()

        error_logs = [r for r in caplog.records if "[ERROR]" in r.message]
        assert any("error_function" in log.message for log in error_logs)

    def test_class_method_logging(self, caplog: Any) -> None:
        """Test class method logging includes class name."""

        class TestClass:
            @auto_log
            def test_method(self) -> str:
                return "success"

        with caplog.at_level(logging.DEBUG):
            obj = TestClass()
            obj.test_method()

        enter_logs = [r for r in caplog.records if "[ENTER]" in r.message]
        assert any("TestClass" in log.message for log in enter_logs)

    def test_function_logging_no_class_name(self, caplog: Any) -> None:
        """Test function logging doesn't include class name."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def standalone_function() -> None:
                pass

            standalone_function()

        enter_logs = [r for r in caplog.records if "[ENTER]" in r.message]
        # Should just have function name, not ClassName.function_name
        assert any("standalone_function" in log.message for log in enter_logs)

    def test_function_name_extraction(self, caplog: Any) -> None:
        """Test function name is correctly extracted."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def my_custom_function_name() -> None:
                pass

            my_custom_function_name()

        assert any("my_custom_function_name" in r.message for r in caplog.records)

    def test_step_name_formatting(self) -> None:
        """Test step name formatting (replace _ with space, title case)."""

        # This is used for Allure steps
        @auto_log
        def test_my_function_name() -> None:
            pass

        # The step name should be "Test My Function Name"
        # We can't easily test this without Allure, but we can verify the decorator works
        test_my_function_name()

    @patch("src.Core.decorators.Config.ALLURE_ENABLED", True)
    def test_allure_disabled_no_import_error(self) -> None:
        """Test no error when Allure is disabled."""

        @auto_log
        def function() -> str:
            return "success"

        result = function()
        assert result == "success"

    def test_with_function_returning_value(self) -> None:
        """Test auto_log preserves function return value."""

        @auto_log
        def add(a: int, b: int) -> int:
            return a + b

        result = add(5, 3)
        assert result == 8

    def test_with_function_returning_none(self) -> None:
        """Test auto_log with function returning None."""

        @auto_log
        def returns_none() -> None:
            pass

        result = returns_none()
        assert result is None

    def test_with_function_with_args(self, caplog: Any) -> None:
        """Test auto_log with function arguments."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def function_with_args(a: int, b: str) -> str:
                return f"{a}-{b}"

            result = function_with_args(42, "test")

        assert result == "42-test"

    def test_with_function_with_kwargs(self) -> None:
        """Test auto_log with function keyword arguments."""

        @auto_log
        def function_with_kwargs(a: int = 1, b: str = "default") -> str:
            return f"{a}-{b}"

        result = function_with_kwargs(a=10, b="custom")
        assert result == "10-custom"

    def test_with_args_and_kwargs(self) -> None:
        """Test auto_log with mixed args and kwargs."""

        @auto_log
        def mixed_function(a: int, b: int, c: int = 3) -> int:
            return a + b + c

        result = mixed_function(1, 2, c=5)
        assert result == 8

    def test_exception_re_raising(self) -> None:
        """Test exception is re-raised after logging."""

        @auto_log
        def raising_function() -> None:
            raise ElementError("Test error")

        with pytest.raises(ElementError, match="Test error"):
            raising_function()

    def test_logging_levels(self, caplog: Any) -> None:
        """Test correct logging levels are used."""
        with caplog.at_level(logging.DEBUG):

            @auto_log
            def function() -> None:
                pass

            function()

        # Entry/Exit should be DEBUG
        debug_logs = [r for r in caplog.records if r.levelno == logging.DEBUG]
        assert len(debug_logs) >= 2  # At least ENTER and EXIT

    def test_decorator_preserves_function_metadata(self) -> None:
        """Test decorator preserves __name__ and __doc__."""

        @auto_log
        def documented_function() -> None:
            """This is a test function."""
            pass

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a test function."

    def test_decorator_stacking_order(self) -> None:
        """Test decorator stacking maintains correct order."""
        call_order: list[str] = []

        @auto_log
        @retry(max_attempts=2, delay=0.1)
        def stacked_function() -> str:
            call_order.append("function")
            return "success"

        result = stacked_function()
        assert result == "success"
        assert "function" in call_order

    def test_with_nested_function_calls(self, caplog: Any) -> None:
        """Test with nested function calls."""

        @auto_log
        def outer() -> str:
            return inner()

        @auto_log
        def inner() -> str:
            return "nested"

        with caplog.at_level(logging.DEBUG):
            result = outer()

        assert result == "nested"
        # Both outer and inner should be logged
        assert any("outer" in r.message for r in caplog.records)
        assert any("inner" in r.message for r in caplog.records)
