import json
import re
from jsonpath_ng import parse
from typing import Optional, Any, Dict, List
from playwright.sync_api import APIResponse
from src.Core import auto_log, AutomationError


class Extractor:
    @staticmethod
    @auto_log
    def text(response: APIResponse) -> str:
        try:
            return response.text()
        except Exception as e:
            raise AutomationError("Failed to extract response text", str(e)) from e

    @staticmethod
    @auto_log
    def json(response: APIResponse) -> Dict[str, Any]:
        try:
            return response.json()
        except Exception as e:
            raise AutomationError("Failed to extract JSON from response", str(e)) from e

    @staticmethod
    @auto_log
    def status_code(response: APIResponse) -> int:
        try:
            return response.status
        except Exception as e:
            raise AutomationError("Failed to extract status code", str(e)) from e

    @staticmethod
    @auto_log
    def headers(response: APIResponse) -> Dict[str, str]:
        try:
            return dict(response.headers)
        except Exception as e:
            raise AutomationError("Failed to extract headers", str(e)) from e

    @staticmethod
    @auto_log
    def header_value(response: APIResponse, header_name: str) -> Optional[str]:
        try:
            headers = response.headers
            for header, value in headers.items():
                if header.lower() == header_name.lower():
                    return value
            return None
        except Exception as e:
            raise AutomationError(
                f"Failed to extract header '{header_name}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_field(response: APIResponse, field_path: str) -> Any:
        try:
            data = response.json()
            fields = field_path.split(".")
            current = data
            for field in fields:
                if isinstance(current, dict) and field in current:
                    current = current[field]
                elif isinstance(current, list) and field.isdigit():
                    index = int(field)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        return None
                else:
                    return None
            return current
        except Exception as e:
            raise AutomationError(
                f"Failed to extract field '{field_path}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def regex_match(
        response: APIResponse, pattern: str, group: int = 0
    ) -> Optional[str]:
        try:
            text = response.text()
            match = re.search(pattern, text)
            if match:
                return match.group(group)
            return None
        except Exception as e:
            raise AutomationError(
                f"Failed to extract regex pattern '{pattern}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def regex_match_all(response: APIResponse, pattern: str) -> List[str]:
        try:
            text = response.text()
            matches = re.findall(pattern, text)
            return matches
        except Exception as e:
            raise AutomationError(
                f"Failed to extract all regex matches for '{pattern}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_string_to_dict(json_string: str) -> Dict[str, Any]:
        try:
            return json.loads(json_string)
        except Exception as e:
            raise AutomationError(
                "Failed to convert JSON string to dictionary", str(e)
            ) from e

    @staticmethod
    @auto_log
    def jsonpath(response: APIResponse, jsonpath_expr: str, index: int = 0) -> Any:
        try:
            json_data = response.json()
            expression = parse(jsonpath_expr)
            matches = expression.find(json_data)

            if matches and len(matches) > index:
                return matches[index].value
            return None
        except Exception as e:
            raise AutomationError(
                f"Failed to extract JSONPath '{jsonpath_expr}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def jsonpath_all(response: APIResponse, jsonpath_expr: str) -> List[Any]:
        try:
            json_data = response.json()
            expression = parse(jsonpath_expr)
            matches = expression.find(json_data)

            return [match.value for match in matches]
        except Exception as e:
            raise AutomationError(
                f"Failed to extract all JSONPath matches for '{jsonpath_expr}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def url(response: APIResponse) -> str:
        try:
            return response.url
        except Exception as e:
            raise AutomationError("Failed to extract response URL", str(e)) from e

    @staticmethod
    @auto_log
    def content_type(response: APIResponse) -> Optional[str]:
        try:
            return response.headers.get("content-type")
        except Exception as e:
            raise AutomationError("Failed to extract content type", str(e)) from e

    @staticmethod
    @auto_log
    def content_length(response: APIResponse) -> Optional[int]:
        try:
            length_str = response.headers.get("content-length")
            return int(length_str) if length_str else None
        except Exception as e:
            raise AutomationError("Failed to extract content length", str(e)) from e

    @staticmethod
    @auto_log
    def cookies(response: APIResponse) -> Dict[str, str]:
        try:
            cookies = {}
            set_cookie_headers = response.headers.get_all("set-cookie") or []
            for cookie_header in set_cookie_headers:
                if "=" in cookie_header:
                    name, value = cookie_header.split("=", 1)
                    value = value.split(";")[0]
                    cookies[name.strip()] = value.strip()
            return cookies
        except Exception as e:
            raise AutomationError("Failed to extract cookies", str(e)) from e

    @staticmethod
    @auto_log
    def json_fields(response: APIResponse, field_paths: List[str]) -> Dict[str, Any]:
        try:
            result = {}
            for field_path in field_paths:
                result[field_path] = Extractor.json_field(response, field_path)
            return result
        except Exception as e:
            raise AutomationError("Failed to extract multiple fields", str(e)) from e

    @staticmethod
    @auto_log
    def json_array_field(response: APIResponse, field_path: str, index: int = 0) -> Any:
        try:
            array_value = Extractor.json_field(response, field_path)

            if not isinstance(array_value, list):
                raise AutomationError(f"Field '{field_path}' is not an array")

            if index >= len(array_value):
                raise AutomationError(
                    f"Array index {index} out of bounds for field '{field_path}'"
                )

            return array_value[index]
        except Exception as e:
            raise AutomationError(
                f"Failed to extract array field '{field_path}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_array_length(response: APIResponse, field_path: str) -> int:
        try:
            array_value = Extractor.json_field(response, field_path)

            if not isinstance(array_value, list):
                raise AutomationError(f"Field '{field_path}' is not an array")

            return len(array_value)
        except Exception as e:
            raise AutomationError(
                f"Failed to get array length for '{field_path}'", str(e)
            ) from e

    @staticmethod
    @auto_log
    def json_keys(response: APIResponse, field_path: str = "") -> List[str]:
        try:
            if field_path:
                obj_value = Extractor.json_field(response, field_path)
            else:
                obj_value = response.json()

            if not isinstance(obj_value, dict):
                raise AutomationError(f"Field '{field_path}' is not an object")

            return list(obj_value.keys())
        except Exception as e:
            raise AutomationError(
                f"Failed to extract keys from '{field_path}'", str(e)
            ) from e
