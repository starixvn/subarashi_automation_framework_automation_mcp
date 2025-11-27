import re
import jsonschema  # type: ignore[import-untyped]
from typing import Any, Dict
from playwright.sync_api import APIResponse
from src.Core import auto_log, AutomationError
from .extractor import Extractor
from jsonpath_ng import parse  # type: ignore[import-untyped]


class Assertions:
    @staticmethod
    @auto_log
    def status_code_equals(response: APIResponse, expected_status: int) -> None:
        try:
            actual_status = response.status
            if actual_status != expected_status:
                raise AutomationError(
                    f"Status code mismatch. Expected: {expected_status}, Actual: {actual_status}"
                )
        except Exception as e:
            raise AutomationError("Failed to verify status code", str(e)) from e

    @staticmethod
    @auto_log
    def status_code_in_range(
        response: APIResponse, min_status: int, max_status: int
    ) -> None:
        try:
            actual_status = response.status
            if not (min_status <= actual_status <= max_status):
                raise AutomationError(
                    f"Status code {actual_status} not in range {min_status}-{max_status}"
                )
        except Exception as e:
            raise AutomationError("Failed to verify status code range", str(e)) from e

    @staticmethod
    @auto_log
    def response_contains_text(response: APIResponse, text: str) -> None:
        try:
            response_text = response.text()
            if text not in response_text:
                raise AutomationError(f"Response does not contain text: '{text}'")
        except Exception as e:
            raise AutomationError(
                "Failed to verify response contains text", str(e)
            ) from e

    @staticmethod
    @auto_log
    def response_not_contains_text(response: APIResponse, text: str) -> None:
        try:
            response_text = response.text()
            if text in response_text:
                raise AutomationError(f"Response should not contain text: '{text}'")
        except Exception as e:
            raise AutomationError(
                "Failed to verify response does not contain text", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_field_equals(
        response: APIResponse, field_path: str, expected_value: Any
    ) -> None:
        try:
            actual_value = Extractor.json_field(response, field_path)
            if actual_value != expected_value:
                raise AutomationError(
                    f"JSON field '{field_path}' mismatch. Expected: {expected_value}, Actual: {actual_value}"
                )
        except Exception as e:
            raise AutomationError(
                f"Failed to verify JSON field '{field_path}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_field_not_null(response: APIResponse, field_path: str) -> None:
        try:
            value = Extractor.json_field(response, field_path)
            if value is None:
                raise AutomationError(f"JSON field '{field_path}' should not be null")
        except Exception as e:
            raise AutomationError(
                f"Failed to verify JSON field '{field_path}' is not null", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_field_is_null(response: APIResponse, field_path: str) -> None:
        try:
            value = Extractor.json_field(response, field_path)
            if value is not None:
                raise AutomationError(
                    f"JSON field '{field_path}' should be null but was: {value}"
                )
        except Exception as e:
            raise AutomationError(
                f"Failed to verify JSON field '{field_path}' is null", str(e)
            ) from e

    @staticmethod
    @auto_log
    def header_exists(response: APIResponse, header_name: str) -> None:
        try:
            headers = response.headers
            header_found = any(
                header.lower() == header_name.lower() for header in headers.keys()
            )
            if not header_found:
                raise AutomationError(f"Header '{header_name}' not found in response")
        except Exception as e:
            raise AutomationError(
                f"Failed to verify header '{header_name}' exists", str(e)
            ) from e

    @staticmethod
    @auto_log
    def header_equals(
        response: APIResponse, header_name: str, expected_value: str
    ) -> None:
        try:
            actual_value = Extractor.header_value(response, header_name)
            if actual_value != expected_value:
                raise AutomationError(
                    f"Header '{header_name}' mismatch. Expected: '{expected_value}', Actual: '{actual_value}'"
                )
        except Exception as e:
            raise AutomationError(
                f"Failed to verify header '{header_name}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def content_type_equals(response: APIResponse, expected_content_type: str) -> None:
        try:
            actual_content_type = Extractor.content_type(response)
            if actual_content_type != expected_content_type:
                raise AutomationError(
                    f"Content-Type mismatch. Expected: '{expected_content_type}', Actual: '{actual_content_type}'"
                )
        except Exception as e:
            raise AutomationError("Failed to verify content type", str(e)) from e

    @staticmethod
    @auto_log
    def response_time_less_than(response: APIResponse, max_time_ms: int) -> None:
        try:
            response_time = getattr(response, "_timing", {}).get(
                "responseEnd", 0
            ) - getattr(response, "_timing", {}).get("requestStart", 0)
            if response_time > max_time_ms:
                raise AutomationError(
                    f"Response time {response_time}ms exceeds maximum {max_time_ms}ms"
                )
        except Exception as e:
            raise AutomationError("Failed to verify response time", str(e)) from e

    @staticmethod
    @auto_log
    def match_by_regex(response: APIResponse, pattern: str) -> None:
        try:
            response_text = response.text()
            if not re.search(pattern, response_text):
                raise AutomationError(
                    f"Response does not match regex pattern: '{pattern}'"
                )
        except Exception as e:
            raise AutomationError(
                f"Failed to match regex pattern '{pattern}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def match_by_jsonpath(response: APIResponse, jsonpath_expr: str) -> None:
        try:
            json_data = response.json()
            expression = parse(jsonpath_expr)
            matches = expression.find(json_data)

            if not matches:
                raise AutomationError(
                    f"No matches found for JSONPath expression: '{jsonpath_expr}'"
                )
        except Exception as e:
            raise AutomationError(
                f"Failed to match JSONPath '{jsonpath_expr}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_schema_valid(response: APIResponse, schema: Dict[str, Any]) -> None:
        try:
            json_data = response.json()
            jsonschema.validate(json_data, schema)
        except Exception as e:
            raise AutomationError("JSON schema validation failed", str(e)) from e

    @staticmethod
    @auto_log
    def json_array_length_equals(
        response: APIResponse, field_path: str, expected_length: int
    ) -> None:
        try:
            array_data = Extractor.json_field(response, field_path)
            if not isinstance(array_data, list):
                raise AutomationError(f"Field '{field_path}' is not an array")
            actual_length = len(array_data)
            if actual_length != expected_length:
                raise AutomationError(
                    f"Array length mismatch. Expected: {expected_length}, Actual: {actual_length}"
                )
        except Exception as e:
            raise AutomationError(
                f"Failed to verify array length for '{field_path}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_array_not_empty(response: APIResponse, field_path: str) -> None:
        try:
            array_data = Extractor.json_field(response, field_path)
            if not isinstance(array_data, list):
                raise AutomationError(f"Field '{field_path}' is not an array")
            if len(array_data) == 0:
                raise AutomationError(f"Array '{field_path}' should not be empty")
        except Exception as e:
            raise AutomationError(
                f"Failed to verify array '{field_path}' is not empty", str(e)
            ) from e
