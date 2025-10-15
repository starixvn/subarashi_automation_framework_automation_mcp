from playwright.sync_api import Page
from config.config import Config
from src.Core import auto_log
from src.Core.page import PageManager
from src.Core.api import APIManager
from src.Core.database import DatabaseManager
from src.Core.utilities import UtilitiesManager

from src.Interfaces import interface_login
from src.Interfaces import interface_common
from src.DataTest import data_login


UI = {
    "login_page": interface_login.Element_Login_Lap[Config.LANGUAGE],
    "menu": interface_common.Element_Menu[Config.LANGUAGE],
}

DataSet = {
    "login_page": data_login.Data_Login_Lap[Config.ENVIRONMENT],
    "login_page_lrf": data_login.Data_Login_Lrf[Config.ENVIRONMENT],
}


class ActionCommon:
    def __init__(self, page: Page):
        self.page = PageManager(page)
        self.api = APIManager(page.context.request)
        self.database = DatabaseManager()
        self.utils = UtilitiesManager()

    @auto_log
    def login(self):
        decrypted_password = self.utils.decrypt(
            DataSet["login_page"]["encrypted"],
            DataSet["login_page"]["Password"],
            DataSet["login_page"]["salt"],
        )
        self.page.navigate(Config.URLS[Config.SITE][Config.ENVIRONMENT]["url"])
        self.page.type_text(
            UI["login_page"]["txtUsername"], DataSet["login_page"]["Username"]
        )
        self.page.type_text(UI["login_page"]["txtPassword"], decrypted_password)
        self.page.click(UI["login_page"]["btnLogin"])
        self.page.for_page_load()
        self.page.verify_element_exist(UI["login_page"]["imgLogo"])
        self.getExternalServerName()

        if self.page.does_element_exist(
            "//div[@id='whatsNewList' and @class='whatsNewList active']"
        ):
            self.page.click("//input[@id='toggleAutoShow']")
            self.page.click("//div[@id='whatsNewList']//i[@class='icon icon-close']")

        self.page.click("//span[@id='user_Name']")
        self.page.click("//a[@data-activates='langList_dropdown']")
        if Config.LANGUAGE == "ch":
            self.page.click("//a[text()='简体中文']")
        elif Config.LANGUAGE == "vi":
            self.page.click("//a[contains(text(),'Tiếng Việt']")
        else:
            self.page.click("//a[text()='English' and @class='choice']")

        self.page.click(
            "//div[@class='widgetbox preferences_setting']//a[contains(@class,'btn btn-ok')]"
        )

    def getExternalServerName(self):
        res = self.api.get(
            url=Config.URLS[Config.SITE][Config.ENVIRONMENT]["url"],
            path=UI["login_page"]["lnkAccessBTC"],
        )
        self.lrfurl = res.url.replace("/BettingTicketCenter", "")

        res = self.api.get(
            url=Config.URLS[Config.SITE][Config.ENVIRONMENT]["url"],
            path=UI["login_page"]["lnkAccessSubsidiarySetting"],
        )
        # self.apiurl = res.json()["ApiUrl"]
        self.apiurl = Config.URLS[Config.SITE][Config.ENVIRONMENT]["apiurl"]

        self.analyticsurl = Config.URLS[Config.SITE][Config.ENVIRONMENT]["analyticsurl"]

    @auto_log
    def navigate_to_betting_ticket_center(self):
        self.page.click(UI["menu"]["lnkBettingTicketCenter"])
        self.page.for_timeout(2)
