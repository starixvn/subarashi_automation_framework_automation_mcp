from typing import Optional
from playwright.sync_api import Page
from src.Core.exceptions import ElementError
from src.Core import auto_log, retry
from .frame import Frame


class Actions(Frame):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page: Page = page

    @auto_log
    # @retry(max_attempts=3)
    def click(self, selector: str) -> None:
        try:
            self.page.locator(selector).click()
        except Exception as e:
            raise ElementError(f"Failed to click {selector}", str(e)) from e

    @auto_log
    @retry(max_attempts=2)
    def double_click(self, selector: str) -> None:
        try:
            self.page.locator(selector).dblclick()
        except Exception as e:
            raise ElementError(f"Failed to double click {selector}", str(e)) from e

    @auto_log
    # @retry(max_attempts=3)
    def right_click(self, selector: str) -> None:
        try:
            self.page.locator(selector).click(button="right")
        except Exception as e:
            raise ElementError(f"Failed to right click {selector}", str(e)) from e

    @auto_log
    # @retry(max_attempts=3)
    def fill(self, selector: str, text: str) -> None:
        try:
            element = self.page.locator(selector)
            element.clear()
            element.fill(text)
        except Exception as e:
            raise ElementError(f"Failed to fill {selector}", str(e)) from e

    @auto_log
    # @retry(max_attempts=3)
    def fill_text(self, selector: str, text: str) -> None:
        self.fill(selector, text)

    @auto_log
    # @retry(max_attempts=3)
    def type_text(self, selector: str, text: str) -> None:
        try:
            self.page.locator(selector).type(text)
        except Exception as e:
            raise ElementError(f"Failed to type in {selector}", str(e)) from e

    @auto_log
    # @retry(max_attempts=3)
    def clear(self, selector: str) -> None:
        try:
            self.page.locator(selector).clear()
        except Exception as e:
            raise ElementError(f"Failed to clear {selector}", str(e)) from e

    @auto_log
    def select_option(self, selector: str, value: str) -> None:
        try:
            self.page.locator(selector).select_option(value)
        except Exception as e:
            raise ElementError(f"Failed to select in {selector}", str(e)) from e

    @auto_log
    def check(self, selector: str) -> None:
        try:
            self.page.locator(selector).check()
        except Exception as e:
            raise ElementError(f"Failed to check {selector}", str(e)) from e

    @auto_log
    def check_checkbox(self, selector: str) -> None:
        self.check(selector)

    @auto_log
    def uncheck(self, selector: str) -> None:
        try:
            self.page.locator(selector).uncheck()
        except Exception as e:
            raise ElementError(f"Failed to uncheck {selector}", str(e)) from e

    @auto_log
    def hover(self, selector: str) -> None:
        try:
            self.page.locator(selector).hover()
        except Exception as e:
            raise ElementError(f"Failed to hover {selector}", str(e)) from e

    @auto_log
    def focus(self, selector: str) -> None:
        try:
            self.page.locator(selector).focus()
        except Exception as e:
            raise ElementError(f"Failed to focus {selector}", str(e)) from e

    @auto_log
    def press_key(self, selector: str, key: str) -> None:
        try:
            self.page.locator(selector).press(key)
        except Exception as e:
            raise ElementError(
                f"Failed to press key {key} on {selector}", str(e)
            ) from e

    @auto_log
    def scroll_to(self, selector: str) -> None:
        try:
            self.page.locator(selector).scroll_into_view_if_needed()
        except Exception as e:
            raise ElementError(f"Failed to scroll to {selector}", str(e)) from e

    @auto_log
    def drag_and_drop(self, source: str, target: str) -> None:
        try:
            self.page.locator(source).drag_to(self.page.locator(target))
        except Exception as e:
            raise ElementError(f"Failed to drag {source} to {target}", str(e)) from e

    @auto_log
    def upload_file(self, selector: str, file_path: str) -> None:
        try:
            self.page.locator(selector).set_input_files(file_path)
        except Exception as e:
            raise ElementError(f"Failed to upload file to {selector}", str(e)) from e

    @auto_log
    def get_text(self, selector: str) -> str:
        try:
            return self.page.locator(selector).text_content() or ""
        except Exception as e:
            raise ElementError(f"Failed to get text from {selector}", str(e)) from e

    @auto_log
    def get_attribute(self, selector: str, attribute: str) -> str:
        try:
            return self.page.locator(selector).get_attribute(attribute) or ""
        except Exception as e:
            raise ElementError(
                f"Failed to get attribute {attribute} from {selector}", str(e)
            ) from e

    @auto_log
    def get_value(self, selector: str) -> str:
        try:
            return self.page.locator(selector).input_value()
        except Exception as e:
            raise ElementError(f"Failed to get value from {selector}", str(e)) from e

    # ========================================================================
    # IFRAME SUPPORT METHODS
    # ========================================================================

    @auto_log
    # @retry(max_attempts=3)
    def fill_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        text: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.clear()
            element.fill(text)
        except Exception as e:
            raise ElementError(f"Failed to fill on frame {frame_xpath}", str(e)) from e

    @auto_log
    # @retry(max_attempts=3)
    def click_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            element.click()
        except Exception as e:
            raise ElementError(f"Failed to click on frame {frame_xpath}", str(e)) from e

    @auto_log
    def select_option_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        value: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.select_option(label=value)
        except Exception as e:
            raise ElementError(
                f"Failed to select option on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def check_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.check()
        except Exception as e:
            raise ElementError(f"Failed to check on frame {frame_xpath}", str(e)) from e

    @auto_log
    def uncheck_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.uncheck()
        except Exception as e:
            raise ElementError(
                f"Failed to uncheck on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def get_text_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> str:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            return element.inner_text()
        except Exception as e:
            raise ElementError(
                f"Failed to get text on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def get_attribute_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        attribute: str,
        idx_child_frame: Optional[int] = None,
    ) -> str:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            return element.get_attribute(attribute) or ""
        except Exception as e:
            raise ElementError(
                f"Failed to get attribute on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def get_value_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> str:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            return element.input_value()
        except Exception as e:
            raise ElementError(
                f"Failed to get value on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def get_inner_html_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> str:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            return element.inner_html()
        except Exception as e:
            raise ElementError(
                f"Failed to get inner HTML on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def get_inner_html_on_frame_by_name(self, frame_name: str, selector: str) -> str:
        try:
            frame = self.page.frame(name=frame_name)
            return frame.inner_html(selector)
        except Exception as e:
            raise ElementError(
                f"Failed to get inner HTML on frame {frame_name}", str(e)
            ) from e

    @auto_log
    def hover_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.hover()
        except Exception as e:
            raise ElementError(f"Failed to hover on frame {frame_xpath}", str(e)) from e

    @auto_log
    def click_element_by_index(self, selector: str, index: int) -> None:
        try:
            self.page.locator(selector).nth(index).click()
        except Exception as e:
            raise ElementError(
                f"Failed to click element at index {index}", str(e)
            ) from e

    @auto_log
    def get_text_by_index(self, selector: str, index: int) -> str:
        try:
            return self.page.locator(selector).nth(index).inner_text()
        except Exception as e:
            raise ElementError(f"Failed to get text at index {index}", str(e)) from e

    @auto_log
    def get_attribute_by_index(self, selector: str, index: int, attribute: str) -> str:
        try:
            return self.page.locator(selector).nth(index).get_attribute(attribute) or ""
        except Exception as e:
            raise ElementError(
                f"Failed to get attribute at index {index}", str(e)
            ) from e

    @auto_log
    def count_elements(self, selector: str) -> int:
        try:
            return self.page.locator(selector).count()
        except Exception as e:
            raise ElementError(f"Failed to count elements: {selector}", str(e)) from e

    @auto_log
    def count_elements_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> int:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            return element.count()
        except Exception as e:
            raise ElementError(
                f"Failed to count elements on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def press_key_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        key: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            element.press(key)
        except Exception as e:
            raise ElementError(
                f"Failed to press key on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def drag_and_drop_on_frame(
        self,
        frame_xpath: str,
        source: str,
        target: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            source_element = self._get_frame_element(
                frame_xpath, source, idx_child_frame
            )
            target_element = self._get_frame_element(
                frame_xpath, target, idx_child_frame
            )
            source_element.drag_to(target_element)
        except Exception as e:
            raise ElementError(
                f"Failed to drag and drop on frame {frame_xpath}", str(e)
            ) from e
