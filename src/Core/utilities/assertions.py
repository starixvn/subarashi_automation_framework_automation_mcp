import re
import os
from typing import Any, List
from src.Core import auto_log, AutomationError


class Assertions:
    def __init__(self):
        self.failed_test_cases: List[str] = []

    @auto_log
    def should_be_equal(
        self, actual: Any, expected: Any, test_name: str = None
    ) -> None:
        try:
            if actual != expected:
                if test_name:
                    self.failed_test_cases.append(test_name)
                raise AutomationError(
                    f"Values not equal. Expected: {expected}, Actual: {actual}"
                )
        except Exception as e:
            raise AutomationError("Assertion failed: should_be_equal", str(e)) from e

    @auto_log
    def should_be_lower_than(
        self, value: Any, expected: Any, test_name: str = None
    ) -> None:
        try:
            if value > expected:
                if test_name:
                    self.failed_test_cases.append(test_name)
                raise AutomationError(
                    f"Value {value} is greater than expected {expected}"
                )
        except Exception as e:
            raise AutomationError(
                "Assertion failed: should_be_lower_than", str(e)
            ) from e

    @auto_log
    def should_be_greater_than_or_equal(
        self, value: Any, expected: Any, test_name: str = None
    ) -> None:
        try:
            if value < expected:
                if test_name:
                    self.failed_test_cases.append(test_name)
                raise AutomationError(f"Value {value} is less than expected {expected}")
        except Exception as e:
            raise AutomationError(
                "Assertion failed: should_be_greater_than_or_equal", str(e)
            ) from e

    @auto_log
    def should_be_not_equal(
        self, actual: Any, expected: Any, test_name: str = None
    ) -> None:
        try:
            if actual == expected:
                if test_name:
                    self.failed_test_cases.append(test_name)
                raise AutomationError(f"Values should not be equal. Both are: {actual}")
        except Exception as e:
            raise AutomationError(
                "Assertion failed: should_be_not_equal", str(e)
            ) from e

    @auto_log
    def should_not_contain(
        self, original_data: str, text: str, test_name: str = None
    ) -> None:
        try:
            if text in original_data:
                if test_name:
                    self.failed_test_cases.append(test_name)
                raise AutomationError(f"Text '{text}' found in data but should not be")
        except Exception as e:
            raise AutomationError("Assertion failed: should_not_contain", str(e)) from e

    @auto_log
    def should_contain(
        self, original_data: str, text: str, test_name: str = None
    ) -> None:
        try:
            if text not in original_data:
                if test_name:
                    self.failed_test_cases.append(test_name)
                raise AutomationError(f"Text '{text}' not found in data")
        except Exception as e:
            raise AutomationError("Assertion failed: should_contain", str(e)) from e

    @auto_log
    def extract_function_name(self, text: str, site: str) -> str:
        try:
            regex = f"filename.*Actions.*{site}_(.*).py"
            match = re.search(regex, text)
            if match:
                return match.group(1)
            return ""
        except Exception as e:
            raise AutomationError("Failed to extract function name", str(e)) from e

    @auto_log
    def get_failed_test_cases(self) -> List[str]:
        try:
            return self.failed_test_cases.copy()
        except Exception as e:
            raise AutomationError("Failed to get failed test cases", str(e)) from e

    @auto_log
    def clear_failed_test_cases(self) -> None:
        try:
            self.failed_test_cases.clear()
        except Exception as e:
            raise AutomationError("Failed to clear failed test cases", str(e)) from e

    @auto_log
    def add_failed_test_case(self, test_name: str) -> None:
        try:
            current_test = str(
                re.search(
                    "::(TestCase.*) ", os.getenv("PYTEST_CURRENT_TEST", "")
                ).group(1)
            ).replace("_", " ")
            self.failed_test_cases.append(current_test)
        except Exception:
            self.failed_test_cases.append(test_name)
