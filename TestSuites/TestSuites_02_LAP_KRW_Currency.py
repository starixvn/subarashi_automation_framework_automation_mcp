import sys
import pytest
from os.path import abspath
from os.path import dirname as d

from src.Action.action_common import ActionCommon
from src.Action.action_my_account import ActionMyAccount

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)


class TestLAPKRWCurrency:
    TEST_CASE_SHEET_NAME = "Testcase"

    @pytest.fixture(autouse=True)
    def setup_action(self, page):
        self.action_common = ActionCommon(page)
        self.action_my_account = ActionMyAccount(page)

    @pytest.mark.tc_id("LAP_TC_1")
    def test_001_verify_krw_in_my_account_default_base_currency(self):
        self.action_my_account.verify_krw_in_my_account_default_base_currency()

    @pytest.mark.tc_id("LAP_TC_2")
    def test_002_verify_krw_in_dashboard_base_currency(self):
        self.action_my_account.verify_krw_in_dashboard_base_currency()

    @pytest.mark.tc_id("LAP_TC_4")
    def test_004_verify_krw_in_dashboard_sportsbook(self):
        self.action_my_account.verify_krw_in_dashboard_sportsbook()

    @pytest.mark.tc_id("LAP_TC_5")
    def test_005_verify_krw_in_betting_ticket_center(self):
        self.action_common.navigate_to_betting_ticket_center()
        self.action_my_account.verify_krw_in_betting_ticket_center()
