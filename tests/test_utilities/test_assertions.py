"""Unit tests for src/Core/utilities/assertions.py"""

import os
from unittest.mock import patch

import pytest

from src.Core.exceptions import AutomationError
from src.Core.utilities.assertions import Assertions


class TestAssertionsShouldBeEqual:
    """Test should_be_equal method."""

    def test_equal_values_pass(self) -> None:
        """Test equal values pass assertion."""
        assertions = Assertions()
        assertions.should_be_equal(5, 5)
        assertions.should_be_equal("test", "test")
        assertions.should_be_equal([1, 2], [1, 2])

    def test_unequal_values_fail(self) -> None:
        """Test unequal values raise error."""
        assertions = Assertions()
        with pytest.raises(AutomationError, match="Values not equal"):
            assertions.should_be_equal(5, 10)

    def test_unequal_with_test_name_adds_to_failed_list(self) -> None:
        """Test failed assertion adds to failed_test_cases."""
        assertions = Assertions()
        with pytest.raises(AutomationError):
            assertions.should_be_equal(1, 2, "TestCase_001")
        assert "TestCase_001" in assertions.failed_test_cases


class TestAssertionsShouldBeLowerThan:
    """Test should_be_lower_than method."""

    def test_lower_value_pass(self) -> None:
        """Test lower value passes."""
        assertions = Assertions()
        assertions.should_be_lower_than(5, 10)
        assertions.should_be_lower_than(0, 1)

    def test_higher_value_fail(self) -> None:
        """Test higher value fails."""
        assertions = Assertions()
        with pytest.raises(AutomationError, match="greater than expected"):
            assertions.should_be_lower_than(10, 5)

    def test_equal_value_pass(self) -> None:
        """Test equal value passes (not greater than)."""
        assertions = Assertions()
        # 5 is not > 5, so no error raised
        assertions.should_be_lower_than(5, 5)


class TestAssertionsShouldBeGreaterThanOrEqual:
    """Test should_be_greater_than_or_equal method."""

    def test_greater_value_pass(self) -> None:
        """Test greater value passes."""
        assertions = Assertions()
        assertions.should_be_greater_than_or_equal(10, 5)

    def test_equal_value_pass(self) -> None:
        """Test equal value passes."""
        assertions = Assertions()
        assertions.should_be_greater_than_or_equal(5, 5)

    def test_lower_value_fail(self) -> None:
        """Test lower value fails."""
        assertions = Assertions()
        with pytest.raises(AutomationError, match="less than expected"):
            assertions.should_be_greater_than_or_equal(5, 10)


class TestAssertionsShouldBeNotEqual:
    """Test should_be_not_equal method."""

    def test_different_values_pass(self) -> None:
        """Test different values pass."""
        assertions = Assertions()
        assertions.should_be_not_equal(5, 10)
        assertions.should_be_not_equal("a", "b")

    def test_equal_values_fail(self) -> None:
        """Test equal values fail."""
        assertions = Assertions()
        with pytest.raises(AutomationError, match="should not be equal"):
            assertions.should_be_not_equal(5, 5)


class TestAssertionsShouldNotContain:
    """Test should_not_contain method."""

    def test_not_containing_text_pass(self) -> None:
        """Test text not in data passes."""
        assertions = Assertions()
        assertions.should_not_contain("Hello World", "xyz")

    def test_containing_text_fail(self) -> None:
        """Test text in data fails."""
        assertions = Assertions()
        with pytest.raises(AutomationError, match="found in data but should not be"):
            assertions.should_not_contain("Hello World", "World")


class TestAssertionsShouldContain:
    """Test should_contain method."""

    def test_containing_text_pass(self) -> None:
        """Test text in data passes."""
        assertions = Assertions()
        assertions.should_contain("Hello World", "World")
        assertions.should_contain("Test123", "123")

    def test_not_containing_text_fail(self) -> None:
        """Test text not in data fails."""
        assertions = Assertions()
        with pytest.raises(AutomationError, match="not found in data"):
            assertions.should_contain("Hello", "xyz")


class TestAssertionsExtractFunctionName:
    """Test extract_function_name method."""

    def test_extract_function_name_success(self) -> None:
        """Test successful extraction of function name."""
        assertions = Assertions()
        text = "filename: Actions_LAP_TestFunction.py"
        result = assertions.extract_function_name(text, "LAP")
        assert result == "TestFunction"

    def test_extract_function_name_no_match(self) -> None:
        """Test extraction with no match returns empty."""
        assertions = Assertions()
        result = assertions.extract_function_name("no match here", "LAP")
        assert result == ""


class TestAssertionsFailedTestCases:
    """Test failed test cases management."""

    def test_get_failed_test_cases_empty(self) -> None:
        """Test get failed test cases when empty."""
        assertions = Assertions()
        assert assertions.get_failed_test_cases() == []

    def test_get_failed_test_cases_with_failures(self) -> None:
        """Test get failed test cases with failures."""
        assertions = Assertions()
        assertions.failed_test_cases = ["Test1", "Test2"]
        result = assertions.get_failed_test_cases()
        assert result == ["Test1", "Test2"]

    def test_clear_failed_test_cases(self) -> None:
        """Test clear failed test cases."""
        assertions = Assertions()
        assertions.failed_test_cases = ["Test1", "Test2"]
        assertions.clear_failed_test_cases()
        assert assertions.failed_test_cases == []

    def test_add_failed_test_case_with_pytest_env(self) -> None:
        """Test add failed test case extracts from pytest env."""
        assertions = Assertions()
        with patch.dict(
            os.environ, {"PYTEST_CURRENT_TEST": "test_file.py::TestCase_MyTest (call)"}
        ):
            assertions.add_failed_test_case("ignored")
        assert len(assertions.failed_test_cases) > 0

    def test_add_failed_test_case_without_pytest_env(self) -> None:
        """Test add failed test case uses provided name."""
        assertions = Assertions()
        with patch.dict(os.environ, {}, clear=True):
            assertions.add_failed_test_case("MyTest")
        assert "MyTest" in assertions.failed_test_cases
