from typing import Any, Dict, Optional

from playwright.sync_api import APIRequestContext, APIResponse

from src.Core import AutomationError, auto_log, retry


class Client:
    def __init__(self, api_context: APIRequestContext) -> None:
        self.api: APIRequestContext = api_context

    @auto_log
    def get(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.get(
                url=full_url,
                headers=headers,
                params=params,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"GET request failed for {url}", str(e)) from e

    @auto_log
    @retry(max_attempts=5, delay=1.0)
    def post(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        form_data: Optional[Dict[str, Any]] = None,
        multipart: Optional[Dict[str, Any]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.post(
                url=full_url,
                headers=headers,
                data=data,
                params=params,
                form=form_data,
                multipart=multipart,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"POST request failed for {url}", str(e)) from e

    @auto_log
    @retry(max_attempts=3)
    def put(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.put(
                url=full_url,
                headers=headers,
                data=data,
                params=params,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"PUT request failed for {url}", str(e)) from e

    @auto_log
    @retry(max_attempts=3)
    def patch(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.patch(
                url=full_url,
                headers=headers,
                data=data,
                params=params,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"PATCH request failed for {url}", str(e)) from e

    @auto_log
    @retry(max_attempts=3)
    def delete(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.delete(
                url=full_url,
                headers=headers,
                params=params,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"DELETE request failed for {url}", str(e)) from e

    @auto_log
    def head(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.head(
                url=full_url,
                headers=headers,
                params=params,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"HEAD request failed for {url}", str(e)) from e

    @auto_log
    def options(
        self,
        url: str,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 100000,
    ) -> APIResponse:
        try:
            full_url = url + path if path else url
            response = self.api.fetch(
                full_url,
                method="OPTIONS",
                headers=headers,
                timeout=timeout,
                ignore_https_errors=True,
            )
            return response
        except Exception as e:
            raise AutomationError(f"OPTIONS request failed for {url}", str(e)) from e

    @auto_log
    def request(self, method: str, url: str, **kwargs: Any) -> APIResponse:
        try:
            response = self.api.fetch(url, method=method.upper(), **kwargs)
            return response
        except Exception as e:
            raise AutomationError(
                f"{method.upper()} request failed for {url}", str(e)
            ) from e
