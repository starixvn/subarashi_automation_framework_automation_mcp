from typing import Optional
from playwright.sync_api import Page
from src.Core import auto_log, ElementError
from .frame import Frame


class Assertions(Frame):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page: Page = page

    @auto_log
    def element_visible(self, selector: str) -> bool:
        try:
            return self.page.locator(selector).is_visible()
        except Exception as e:
            raise ElementError(
                f"Failed to check element visibility: {selector}", str(e)
            ) from e

    @auto_log
    def element_hidden(self, selector: str) -> bool:
        try:
            return not self.page.locator(selector).is_visible()
        except Exception as e:
            raise ElementError(
                f"Failed to check element hidden: {selector}", str(e)
            ) from e

    @auto_log
    def element_exists(self, selector: str) -> bool:
        try:
            return self.page.locator(selector).count() > 0
        except Exception as e:
            raise ElementError(
                f"Failed to check element exists: {selector}", str(e)
            ) from e

    @auto_log
    def element_enabled(self, selector: str) -> bool:
        try:
            return self.page.locator(selector).is_enabled()
        except Exception as e:
            raise ElementError(
                f"Failed to check element enabled: {selector}", str(e)
            ) from e

    @auto_log
    def element_disabled(self, selector: str) -> bool:
        try:
            return self.page.locator(selector).is_disabled()
        except Exception as e:
            raise ElementError(
                f"Failed to check element disabled: {selector}", str(e)
            ) from e

    @auto_log
    def element_checked(self, selector: str) -> bool:
        try:
            return self.page.locator(selector).is_checked()
        except Exception as e:
            raise ElementError(
                f"Failed to check element checked: {selector}", str(e)
            ) from e

    @auto_log
    def element_editable(self, selector: str) -> bool:
        try:
            return self.page.locator(selector).is_editable()
        except Exception as e:
            raise ElementError(
                f"Failed to check element editable: {selector}", str(e)
            ) from e

    @auto_log
    def element_text_equals(self, selector: str, expected_text: str) -> None:
        try:
            actual_text = self.page.locator(selector).text_content()
            if actual_text != expected_text:
                raise ElementError(
                    f"Text mismatch. Expected: '{expected_text}', Actual: '{actual_text}'"
                )
        except Exception as e:
            raise ElementError(f"Failed to verify text for {selector}", str(e)) from e

    @auto_log
    def element_text_contains(self, selector: str, text: str) -> None:
        try:
            actual_text = self.page.locator(selector).text_content() or ""
            if text not in actual_text:
                raise ElementError(
                    f"Text '{text}' not found in element. Actual: '{actual_text}'"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify text contains for {selector}", str(e)
            ) from e

    @auto_log
    def element_value_equals(self, selector: str, expected_value: str) -> None:
        try:
            actual_value = self.page.locator(selector).input_value()
            if actual_value != expected_value:
                raise ElementError(
                    f"Value mismatch. Expected: '{expected_value}', Actual: '{actual_value}'"
                )
        except Exception as e:
            raise ElementError(f"Failed to verify value for {selector}", str(e)) from e

    @auto_log
    def element_attribute_equals(
        self, selector: str, attribute: str, expected_value: str
    ) -> None:
        try:
            actual_value = self.page.locator(selector).get_attribute(attribute) or ""
            if actual_value != expected_value:
                raise ElementError(
                    f"Attribute '{attribute}' mismatch. Expected: '{expected_value}', Actual: '{actual_value}'"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify attribute {attribute} for {selector}", str(e)
            ) from e

    @auto_log
    def element_attribute_contains(
        self, selector: str, attribute: str, text: str
    ) -> None:
        try:
            actual_value = self.page.locator(selector).get_attribute(attribute) or ""
            if text not in actual_value:
                raise ElementError(
                    f"Attribute '{attribute}' does not contain '{text}'. Actual: '{actual_value}'"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify attribute contains for {selector}", str(e)
            ) from e

    @auto_log
    def page_title_equals(self, expected_title: str) -> None:
        try:
            actual_title = self.page.title()
            if actual_title != expected_title:
                raise ElementError(
                    f"Title mismatch. Expected: '{expected_title}', Actual: '{actual_title}'"
                )
        except Exception as e:
            raise ElementError("Failed to verify page title", str(e)) from e

    @auto_log
    def page_title_contains(self, text: str) -> None:
        try:
            actual_title = self.page.title()
            if text not in actual_title:
                raise ElementError(
                    f"Title does not contain '{text}'. Actual: '{actual_title}'"
                )
        except Exception as e:
            raise ElementError("Failed to verify page title contains", str(e)) from e

    @auto_log
    def page_url_equals(self, expected_url: str) -> None:
        try:
            current_url = self.page.url
            if current_url != expected_url:
                raise ElementError(
                    f"URL mismatch. Expected: '{expected_url}', Actual: '{current_url}'"
                )
        except Exception as e:
            raise ElementError("Failed to verify URL equals", str(e)) from e

    @auto_log
    def page_url_contains(self, url_part: str) -> None:
        try:
            current_url = self.page.url
            if url_part not in current_url:
                raise ElementError(
                    f"URL does not contain '{url_part}'. Current: '{current_url}'"
                )
        except Exception as e:
            raise ElementError("Failed to verify URL contains", str(e)) from e

    @auto_log
    def element_count_equals(self, selector: str, expected_count: int) -> None:
        try:
            actual_count = self.page.locator(selector).count()
            if actual_count != expected_count:
                raise ElementError(
                    f"Element count mismatch. Expected: {expected_count}, Actual: {actual_count}"
                )
        except Exception as e:
            raise ElementError(f"Failed to count elements: {selector}", str(e)) from e

    @auto_log
    def element_count_greater_than(self, selector: str, min_count: int) -> None:
        try:
            actual_count = self.page.locator(selector).count()
            if actual_count <= min_count:
                raise ElementError(
                    f"Element count should be > {min_count}, but was {actual_count}"
                )
        except Exception as e:
            raise ElementError(f"Failed to count elements: {selector}", str(e)) from e

    @auto_log
    def page_has_text(self, text: str) -> None:
        try:
            page_content = self.page.content()
            if text not in page_content:
                raise ElementError(f"Page does not contain text: '{text}'")
        except Exception as e:
            raise ElementError("Failed to verify page has text", str(e)) from e

    @auto_log
    def verify_element_exist(self, selector: str) -> None:
        try:
            if not self.element_exists(selector):
                raise ElementError(
                    f"Element verification failed - not found: {selector}"
                )
            if not self.element_visible(selector):
                raise ElementError(
                    f"Element verification failed - not visible: {selector}"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify element exists: {selector}", str(e)
            ) from e

    @auto_log
    def does_element_exist(self, selector: str) -> bool:
        try:
            return self.element_exists(selector)
        except Exception:
            return False

    # ========================================================================
    # IFRAME SUPPORT METHODS
    # ========================================================================

    @auto_log
    def element_visible_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> bool:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            return element.is_visible()
        except Exception as e:
            raise ElementError(
                f"Failed to check visibility on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_exists_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> bool:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            return element.count() > 0
        except Exception as e:
            raise ElementError(
                f"Failed to check exists on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_enabled_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> bool:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            return element.is_enabled()
        except Exception as e:
            raise ElementError(
                f"Failed to check enabled on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_checked_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> bool:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            return element.is_checked()
        except Exception as e:
            raise ElementError(
                f"Failed to check checkbox on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_text_equals_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        expected_text: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            actual_text = element.text_content()
            if actual_text != expected_text:
                raise ElementError(
                    f"Text mismatch. Expected: '{expected_text}', Actual: '{actual_text}'"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify text on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_text_contains_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        text: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            actual_text = element.text_content() or ""
            if text not in actual_text:
                raise ElementError(
                    f"Text '{text}' not found in element. Actual: '{actual_text}'"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify text contains on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_value_equals_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        expected_value: str,
        idx_child_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            actual_value = element.input_value()
            if actual_value != expected_value:
                raise ElementError(
                    f"Value mismatch. Expected: '{expected_value}', Actual: '{actual_value}'"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to verify value on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_count_equals_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        expected_count: int,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> None:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            actual_count = element.count()
            if actual_count != expected_count:
                raise ElementError(
                    f"Element count mismatch. Expected: {expected_count}, Actual: {actual_count}"
                )
        except Exception as e:
            raise ElementError(
                f"Failed to count elements on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def is_checkbox_checked_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> bool:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            return element.is_checked()
        except Exception as e:
            raise ElementError(
                f"Failed to check checkbox state on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def element_not_visible_on_frame(
        self, frame_xpath: str, selector: str, idx_child_frame: Optional[int] = None
    ) -> None:
        try:
            element = self._get_frame_element(frame_xpath, selector, idx_child_frame)
            if element.is_visible():
                raise ElementError(f"Element should not be visible: {selector}")
        except Exception as e:
            raise ElementError(
                f"Failed to verify element not visible on frame {frame_xpath}", str(e)
            ) from e

    @auto_log
    def does_element_exist_on_frame(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> bool:
        try:
            element = self._get_frame_element(
                frame_xpath, selector, idx_child_frame, idx_latest_frame
            )
            return element.is_visible()
        except Exception:
            return False
