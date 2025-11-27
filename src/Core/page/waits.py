from typing import Optional, Literal
from playwright.sync_api import Page
from config.config import Config
from src.Core import auto_log, ElementError
from .frame import Frame


class Waits(Frame):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page: Page = page

    @auto_log
    def for_element(self, selector: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.locator(selector).wait_for(
                state="visible", timeout=timeout * 1000
            )
        except Exception as e:
            raise ElementError(f"Element did not appear: {selector}", str(e)) from e

    @auto_log
    def for_element_visible(
        self, selector: str, timeout: Optional[float] = None
    ) -> None:
        self.for_element(selector, timeout)

    @auto_log
    def for_element_hidden(
        self, selector: str, timeout: Optional[float] = None
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(f"Element did not hide: {selector}", str(e)) from e

    @auto_log
    def for_element_attached(
        self, selector: str, timeout: Optional[float] = None
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.locator(selector).wait_for(
                state="attached", timeout=timeout * 1000
            )
        except Exception as e:
            raise ElementError(f"Element did not attach: {selector}", str(e)) from e

    @auto_log
    def for_element_detached(
        self, selector: str, timeout: Optional[float] = None
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.locator(selector).wait_for(
                state="detached", timeout=timeout * 1000
            )
        except Exception as e:
            raise ElementError(f"Element did not detach: {selector}", str(e)) from e

    @auto_log
    def for_page_load(self, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout * 1000)
        except Exception as e:
            raise ElementError("Page did not load", str(e)) from e

    @auto_log
    def for_network_idle(self, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        except Exception as e:
            raise ElementError("Network did not become idle", str(e)) from e

    @auto_log
    def for_dom_ready(self, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout * 1000)
        except Exception as e:
            raise ElementError("DOM not ready", str(e)) from e

    @auto_log
    def for_selector(self, selector: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_selector(selector, timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(f"Selector did not appear: {selector}", str(e)) from e

    @auto_log
    def for_url_change(self, url_pattern: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_url(url_pattern, timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(
                f"URL did not change to pattern: {url_pattern}", str(e)
            ) from e

    @auto_log
    def for_function(self, js_function: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_function(js_function, timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(
                f"Function condition not met: {js_function}", str(e)
            ) from e

    @auto_log
    def for_response(self, url_pattern: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_event(
                "response",
                predicate=lambda r: url_pattern in r.url,
                timeout=timeout * 1000,
            )
        except Exception as e:
            raise ElementError(
                f"Response not received for: {url_pattern}", str(e)
            ) from e

    @auto_log
    def for_request(self, url_pattern: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_event(
                "request",
                predicate=lambda r: url_pattern in r.url,
                timeout=timeout * 1000,
            )
        except Exception as e:
            raise ElementError(f"Request not sent for: {url_pattern}", str(e)) from e

    @auto_log
    def for_timeout(self, seconds: float) -> None:
        try:
            self.page.wait_for_timeout(seconds * 1000)
        except Exception as e:
            raise ElementError(f"Wait timeout failed: {seconds}s", str(e)) from e

    @auto_log
    def for_element_enabled(
        self, selector: str, timeout: Optional[float] = None
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_function(
                f"() => document.querySelector('{selector}') && !document.querySelector('{selector}').disabled",
                timeout=timeout * 1000,
            )
        except Exception as e:
            raise ElementError(
                f"Element did not become enabled: {selector}", str(e)
            ) from e

    @auto_log
    def for_element_clickable(
        self, selector: str, timeout: Optional[float] = None
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout * 1000)
            if not element.is_enabled():
                raise ElementError(f"Element is not clickable: {selector}")
        except Exception as e:
            raise ElementError(
                f"Element did not become clickable: {selector}", str(e)
            ) from e

    @auto_log
    def for_text_present(self, text: str, timeout: Optional[float] = None) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            self.page.wait_for_function(
                f"() => document.body.textContent.includes('{text}')",
                timeout=timeout * 1000,
            )
        except Exception as e:
            raise ElementError(f"Text not found on page: {text}", str(e)) from e

    # ========================================================================
    # IFRAME SUPPORT METHODS
    # ========================================================================

    @auto_log
    def for_element_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        timeout: Optional[float] = None,
        state: Literal["attached", "detached", "hidden", "visible"] = "visible",
        idx_child_frame: Optional[int] = None,
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.wait_for(state=state, timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(
                f"Element did not appear on frame {frame_xpath}: {selector}", str(e)
            ) from e

    @auto_log
    def for_element_visible_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        timeout: Optional[float] = None,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        self.for_element_on_frame(
            frame_xpath, selector, timeout, "visible", idx_child_frame
        )

    @auto_log
    def for_element_hidden_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        timeout: Optional[float] = None,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.wait_for(state="hidden", timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(
                f"Element did not hide on frame {frame_xpath}: {selector}", str(e)
            ) from e

    @auto_log
    def for_element_attached_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        timeout: Optional[float] = None,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.wait_for(state="attached", timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(
                f"Element did not attach on frame {frame_xpath}: {selector}", str(e)
            ) from e

    @auto_log
    def for_frame_load(
        self,
        frame_name: str,
        state: Literal["domcontentloaded", "load", "networkidle"] = "load",
        timeout: Optional[float] = None,
    ) -> None:
        if timeout is None:
            timeout = Config.TIMEOUT / 1000
        try:
            frame = self.page.frame(name=frame_name)
            if not frame:
                raise ElementError(f"Frame not found: {frame_name}")
            frame.wait_for_load_state(state=state, timeout=timeout * 1000)
        except Exception as e:
            raise ElementError(f"Frame did not load: {frame_name}", str(e)) from e
