from os.path import abspath
from os.path import dirname as d
import sys

import pytest

from src.Action.action_common import ActionCommon

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)


class TestDemoPlaywright:
    TEST_CASE_SHEET_NAME = "Testcase"

    @pytest.fixture(autouse=True)
    def setup_action(self, page):
        self.action_demo = ActionCommon(page)

    @pytest.mark.tc_id("LAP_TC_1")
    def Testcase_001_Verify_Message_Display(self):
        pass
