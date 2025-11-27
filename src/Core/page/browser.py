import re
from lxml import html  # type: ignore[import-untyped]
from typing import Any, List, Optional
from playwright.sync_api import Page, Frame
from src.Core import auto_log, AutomationError


class BrowserManager:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

    @auto_log
    def navigate_to(self, url: str) -> None:
        try:
            self.page.goto(url)
        except Exception as e:
            raise AutomationError(f"Failed to navigate to {url}", str(e)) from e

    @auto_log
    def navigate(self, url: str) -> None:
        self.navigate_to(url)

    @auto_log
    def get_current_url(self) -> str:
        try:
            return self.page.url
        except Exception as e:
            raise AutomationError("Failed to get current URL", str(e)) from e

    @auto_log
    def reload(self) -> None:
        try:
            self.page.reload()
        except Exception as e:
            raise AutomationError("Failed to reload page", str(e)) from e

    @auto_log
    def go_back(self) -> None:
        try:
            self.page.go_back()
        except Exception as e:
            raise AutomationError("Failed to go back", str(e)) from e

    @auto_log
    def go_forward(self) -> None:
        try:
            self.page.go_forward()
        except Exception as e:
            raise AutomationError("Failed to go forward", str(e)) from e

    @auto_log
    def get_title(self) -> str:
        try:
            return self.page.title()
        except Exception as e:
            raise AutomationError("Failed to get page title", str(e)) from e

    @auto_log
    def set_viewport_size(self, width: int, height: int) -> None:
        try:
            self.page.set_viewport_size({"width": width, "height": height})
        except Exception as e:
            raise AutomationError("Failed to set viewport size", str(e)) from e

    @auto_log
    def screenshot(self, path: str) -> None:
        try:
            self.page.screenshot(path=path, full_page=True)
        except Exception as e:
            raise AutomationError(f"Failed to take screenshot: {path}", str(e)) from e

    @auto_log
    def close_page(self) -> None:
        try:
            self.page.close()
        except Exception as e:
            raise AutomationError("Failed to close page", str(e)) from e

    @auto_log
    def evaluate(self, expression: str) -> Any:
        try:
            return self.page.evaluate(expression)
        except Exception as e:
            raise AutomationError(f"Failed to evaluate: {expression}", str(e)) from e

    @auto_log
    def get_frames(self) -> List[Frame]:
        try:
            return self.page.frames
        except Exception as e:
            raise AutomationError("Failed to get frames", str(e)) from e

    @auto_log
    def get_frame_by_name(self, name: str) -> Frame:
        try:
            frame = self.page.frame(name=name)
            if not frame:
                raise AutomationError(f"Frame not found: {name}")
            return frame
        except Exception as e:
            raise AutomationError(f"Failed to get frame: {name}", str(e)) from e

    @auto_log
    def get_frame_content(self, frame_index: int) -> str:
        try:
            frames = self.page.frames
            return frames[frame_index].content()
        except Exception as e:
            raise AutomationError(
                f"Failed to get frame content at index {frame_index}", str(e)
            ) from e

    @auto_log
    def sleep(self, milliseconds: float) -> None:
        try:
            self.page.wait_for_timeout(milliseconds)
        except Exception as e:
            raise AutomationError(f"Failed to sleep {milliseconds}ms", str(e)) from e

    # ========================================================================
    # REGEX METHODS
    # ========================================================================

    @auto_log
    def match_by_regex(self, pattern: str) -> bool:
        try:
            return bool(re.search(pattern, self.page.content()))
        except Exception as e:
            raise AutomationError(
                f"Failed to match regex pattern: {pattern}", str(e)
            ) from e

    @auto_log
    def match_by_regex_on_frame(self, frame_name: str, pattern: str) -> bool:
        try:
            frame = self.page.frame(name=frame_name)
            if not frame:
                raise AutomationError(f"Frame not found: {frame_name}")
            return bool(re.search(pattern, frame.content()))
        except Exception as e:
            raise AutomationError(
                f"Failed to match regex on frame {frame_name}", str(e)
            ) from e

    @auto_log
    def extract_by_regex(self, pattern: str, group: Optional[int] = None) -> str:
        try:
            match = re.search(pattern, self.page.content())
            if match:
                return match.group(group) if group is not None else match.group(0)
            return ""
        except Exception as e:
            raise AutomationError(
                f"Failed to extract by regex: {pattern}", str(e)
            ) from e

    @auto_log
    def extract_by_regex_on_frame(
        self, frame_name: str, pattern: str, group: Optional[int] = None
    ) -> str:
        try:
            frames = self.page.frames
            content = frames[1].content() if len(frames) > 1 else ""
            match = re.search(pattern, content)
            if match:
                return match.group(group) if group is not None else match.string
            return ""
        except Exception as e:
            raise AutomationError(
                f"Failed to extract by regex on frame {frame_name}", str(e)
            ) from e

    # ========================================================================
    # SCREENSHOT & DOWNLOAD METHODS
    # ========================================================================

    @auto_log
    def screenshot_element(
        self, selector: str, path: str, full_page: bool = False
    ) -> None:
        try:
            self.page.locator(selector).screenshot(path=path)
        except Exception as e:
            raise AutomationError(
                f"Failed to screenshot element {selector}", str(e)
            ) from e

    @auto_log
    def screenshot_element_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        path: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            if frame_xpath == "" and idx_child_frame is None:
                element = self.page.locator(selector)
            elif idx_child_frame is None:
                frame = self.page.frame_locator(frame_xpath)
                element = frame.locator(selector)
            else:
                frames = self.page.frames
                child_frame = frames[1].child_frames
                element = child_frame[idx_child_frame].locator(selector)

            element.screenshot(path=path)
        except Exception as e:
            raise AutomationError(
                f"Failed to screenshot element on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def download_file(self, selector: str, download_path: str) -> str:
        try:
            with self.page.expect_download() as download_info:
                self.page.locator(selector).click()
            download = download_info.value
            download.save_as(download_path)
            return download_path
        except Exception as e:
            raise AutomationError("Failed to download file", str(e)) from e

    @auto_log
    def download_file_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        download_path: str,
        idx_child_frame: Optional[int] = None,
    ) -> str:
        try:
            if idx_child_frame is None:
                frame = self.page.frame_locator(frame_xpath)
                element = frame.locator(selector)
            else:
                frames = self.page.frames
                child_frame = frames[1].child_frames
                element = child_frame[idx_child_frame].locator(selector)

            with self.page.expect_download() as download_info:
                element.click()
            download = download_info.value
            download.save_as(download_path)
            return download_path
        except Exception as e:
            raise AutomationError(
                f"Failed to download file on frame {frame_xpath}", str(e)
            ) from e

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @auto_log
    def extract_document(self, selector: str) -> Any:
        try:
            text = self.page.inner_html(selector)
            return html.fromstring(text)
        except Exception as e:
            raise AutomationError(
                f"Failed to extract document from {selector}", str(e)
            ) from e

    @auto_log
    def get_text_on_document(self, document: Any, xpath: str) -> str:
        try:
            result = document.xpath(xpath)
            return result[0].text if result else ""
        except Exception as e:
            raise AutomationError("Failed to get text from document", str(e)) from e

    @auto_log
    def get_element_on_document(self, document: Any, xpath: str) -> Any:
        try:
            result = document.xpath(xpath)
            return result[0] if result else None
        except Exception as e:
            raise AutomationError("Failed to get element from document", str(e)) from e

    @auto_log
    def get_substring_in_content(
        self, content: str, keyword: str, str_start: str, str_end: str
    ) -> str:
        try:
            idx_keyword = str(content).index(keyword)
            if idx_keyword > 0:
                sub_content = str(content[idx_keyword:]).strip().split(str_end)
                sub_content = sub_content[0].strip().split(str_start)
                return sub_content[1] if len(sub_content) > 1 else ""
            return ""
        except Exception as e:
            raise AutomationError("Failed to extract substring", str(e)) from e

    @auto_log
    def get_last_frame_index(self) -> int:
        try:
            frames = self.page.frames
            return len(frames) - 1
        except Exception as e:
            raise AutomationError("Failed to get last frame index", str(e)) from e
