from typing import Optional
from playwright.sync_api import Page, Locator, FrameLocator


class Frame:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

    def _get_frame_element(
        self,
        frame_xpath: str,
        selector: str,
        idx_child_frame: Optional[int] = None,
        idx_latest_frame: Optional[int] = None,
    ) -> Locator:
        # Case 1 & 2: Direct page or frame locator
        if idx_child_frame is None and idx_latest_frame is None:
            if frame_xpath == "":
                return self.page.locator(selector)
            else:
                frame: FrameLocator = self.page.frame_locator(frame_xpath)
                return frame.locator(selector)

        # Case 3: Child frame by index
        elif idx_latest_frame is None:
            frames = self.page.frames
            child_frame = frames[1].child_frames
            return child_frame[idx_child_frame].locator(selector)

        # Case 4: Latest frame by index
        else:
            frames = self.page.frames[idx_latest_frame]
            return frames.locator(selector)
