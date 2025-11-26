ELEMENT_MENU_CH = {
    "lnkCustomerManagement": "//span[@class='menu-title' and text()='Customer Management']",
    "CustomerManagement": {
        "lnkPlayerAdministration": "//a[@target='FunctionFrame' and text()='Player Administration']",
        "lnkPlayerSegmentation": "//a[@target='FunctionFrame' and text()='Player Segmentation']",
        "lnkCommissionGroupList": "//a[@target='FunctionFrame' and text()='Commission Group List']",
    },
}

ELEMENT_MENU = {
    "en": {
        "lnkDashboard": "//span[@class='menu-title' and text()='DASHBOARD']",
        "lnkBettingTicketCenter": "//span[@class='menu-title' and text()='Betting Ticket Center']",
        "Notification": {
            "lnkResettlement": "//a[@target='FunctionFrame' and text()='Resettlement']"
        },
        "lnkCustomerManagement": "//span[@class='menu-title' and text()='Customer Management']",
        "CustomerManagement": {
            "lnkPlayerAdministration": "//a[@target='FunctionFrame' and text()='Player Administration']",
            "lnkPlayerSegmentation": "//a[@target='FunctionFrame' and text()='Player Segmentation']",
            "lnkCommissionGroupList": "//a[@target='FunctionFrame' and text()='Commission Group List']",
            "lnkAbnormalBet": "//a[@target='FunctionFrame' and text()='Abnormal Bet']",
            "lnkOddsGroupLicenseeSetting": "//a[@target='FunctionFrame' and text()='Odds Group Licensee Setting']",
        },
        "lnkReports": "//span[@class='menu-title' and text()='Reports']",
        "Reports": {
            "lnkCustomerWinLoss": "//a[@target='FunctionFrame' and text()='Customer Win Loss']",
            "lnkWinLossAnalysis": "//a[@target='FunctionFrame' and contains(@href,'WinlossAnalysisReport')]",
            "lnkSubsidiaryPerformance": "//a[@target='FunctionFrame' and contains(@href,'SubsidiaryPerformanceReport')]",
        },
        "lnkFinance": "//span[@class='menu-title' and text()='Finance']",
        "Finance": {
            "lnkDepositInformation": "//a[@target='FunctionFrame' and text()='Deposit Information']"
        },
    },
    "ch": {
        "lnkDashboard": "//span[@class='menu-title' and text()='信息板']",
        "lnkCustomerManagement": "//span[@class='menu-title' and text()='会员管理']",
        "CustomerManagement": {
            "lnkPlayerAdministration": "//a[@target='FunctionFrame' and text()='玩家管理']",
            "lnkPlayerSegmentation": "//a[@target='FunctionFrame' and text()='玩家分类']",
            "lnkCommissionGroupList": "//a[@target='FunctionFrame' and text()='佣金组别列表']",
            "lnkAbnormalBet": "//a[@target='FunctionFrame' and text()='非正规注单']",
            "lnkOddsGroupLicenseeSetting": "//a[@target='FunctionFrame' and text()='设定水位组别']",
        },
        "lnkReports": "//span[@class='menu-title' and text()='报告']",
        "Reports": {
            "lnkCustomerWinLoss": "//a[@target='FunctionFrame' and text()='会员输赢']",
            "lnkWinLossAnalysis": "//a[@target='FunctionFrame' and contains(@href,'WinlossAnalysisReport')]",
            "lnkSubsidiaryPerformance": "//a[@target='FunctionFrame' and contains(@href,'SubsidiaryPerformanceReport')]",
        },
    },
}

ELEMENT_MENU_LRF = {
    "en": {
        "lnkNotification": "//span[@class='menu-title' and text()='NOTIFICATION']",
        "lnkReports": "//span[@class='menu-title' and text()='REPORTS']",
        "lnkUpcomingReportClosures": "//span[@class='menu-title' and text()='Upcoming Report Closures']",
        "lnkCustomerReports": "//span[@class='menu-title' and text()='CUSTOMER REPORTS']",
        "lnkCustomerInformation": "//span[@class='menu-title' and text()='CUSTOMER INFORMATION']",
        "Notification": {
            "lnkResettlement": "//a[contains(@href,'NotificationReport')]"
        },
        "Reports": {
            "lnkLastBetMonitoring": "//a[contains(@href,'LastBetsMonitoringBetList')]",
            "lnkLiveReport": "//a[contains(@href,'LiveReport')]",
            "lnkBettingTicketCenter": "//a[contains(@href,'BettingTicketCenter')]",
            "lnkWinLossAnalysis": "//a[contains(@href,'WinlossAnalysisReport')]",
            "lnkWinLossByTimeZone": "//a[contains(@href,'WinLossByTimeZoneReport')]",
            "lnkSabaVirtualSportsWinLoss": "//a[contains(@href,'SabaVirtualSportsWinLossReport')]",
            "lnkWinLossByLeague": "//a[contains(@href,'LeagueWinLossReport')]",
            "lnkExchangeWinLoss": "//a[contains(@href,'ExchangeWinlossReport')]",
            "lnkTurnoverReport": "//a[contains(@href,'TurnoverReport')]",
            "lnkResults": "//a[contains(@href,'ResultReport')]",
        },
        "UpcomingReportClosures": {
            "lnkLicenseeWinLossReport": "//a[contains(@href,'LicenseeWinLossReport')]",
            "lnkCashOutWinLoss": "//a[contains(@href,'NewCashOutWinLossReport')]",
        },
        "CustomerReports": {
            "lnkCustomerWinLoss": "//a[contains(@href,'CustomerWinlossReport')]",
            "lnkPlayerSabaCoins": "//a[contains(@href,'PlayerSabaCoinsReport')]",
        },
        "CustomerInfomation": {
            "lnkAbnormalBet": "//a[contains(@href,'AbnormalBetReport')]"
        },
    },
    "ch": {
        "lnkNotification": "//span[@class='menu-title' and text()='NOTIFICATION']",
        "lnkReports": "//span[@class='menu-title' and text()='报告']",
        "lnkUpcomingReportClosures": "//span[@class='menu-title' and text()='即将关闭的报告']",
        "lnkCustomerReports": "//span[@class='menu-title' and text()='客户报告']",
        "lnkCustomerInformation": "//span[@class='menu-title' and text()='客户资料']",
        "Notification": {
            "lnkResettlement": "//a[contains(@href,'NotificationReport')]"
        },
        "Reports": {
            "lnkLastBetMonitoring": "//a[contains(@href,'LastBetsMonitoringBetList')]",
            "lnkLiveReport": "//a[contains(@href,'LiveReport')]",
            "lnkBettingTicketCenter": "//a[contains(@href,'BettingTicketCenter')]",
            "lnkWinLossByTimeZone": "//a[contains(@href,'WinLossByTimeZoneReport')]",
            "lnkWinLossAnalysis": "//a[contains(@href,'WinlossAnalysisReport')]",
            "lnkSabaVirtualSportsWinLoss": "//a[contains(@href,'SabaVirtualSportsWinLossReport')]",
            "lnkExchangeWinLoss": "//a[contains(@href,'ExchangeWinlossReport')]",
            "lnkTurnoverReport": "//a[contains(@href,'TurnoverReport')]",
            "lnkResults": "//a[contains(@href,'ResultReport')]",
        },
        "UpcomingReportClosures": {
            "lnkLicenseeWinLossReport": "//a[contains(@href,'LicenseeWinLossReport')]",
            "lnkCashOutWinLoss": "//a[contains(@href,'NewCashOutWinLossReport')]",
        },
        "CustomerReports": {
            "lnkCustomerWinLoss": "//a[contains(@href,'CustomerWinlossReport')]",
            "lnkPlayerSabaCoins": "//a[contains(@href,'PlayerSabaCoinsReport')]",
        },
        "CustomerInfomation": {
            "lnkAbnormalBet": "//a[contains(@href,'AbnormalBetReport')]"
        },
    },
}

ELEMENT_FRAMES = {
    "frmMain": "//iframe[@name='FunctionFrame']",
    "frmSub": "//iframe[@name='paDetailFrame']",
}

ELEMENT_FRAMES_LRF = {"frmMain": "//iframe[@id='mainFrame']"}

ELEMENTS = {
    "en": {
        "ddlCurrencySingle": "//div[@id='select-list-CurrencyId']",
        "ddlBaseCurrency": "//div[@id='select-list-BaseCurrency']",
        "icoBack": "//a[@class='icon-back']",
        "icoMatchBack": "//button[@class='waves-effect waves-light btn btn-back']",
        "DateRange": "//input[@id='DateRange']",
        "lblBetListTitle": "//div[contains(@class,'betlist-container')]/div[@class='content-title']",
        "icoClosePopup": "//div[contains(@class,'popup-container show')]/div/div/a[@class='popup-close']",
        "lblPopupTitle": "//div[contains(@class,'popup-container show')]/div/div[@class='popup-title']/div[@class='txt-title']",
        "titleReport": "//span[@id='page-title']",
        "icoUserGuide": "//i[@class='icon-book right']",
        "icoExportExcel": "//i[@class='icon-excel right']",
    },
    "ch": {
        "ddlCurrencySingle": "//div[@id='select-list-CurrencyId']",
        "ddlBaseCurrency": "//div[@id='select-list-BaseCurrency']",
        "icoBack": "//a[@class='icon-back']",
        "icoMatchBack": "//button[@class='waves-effect waves-light btn btn-back']",
        "DateRange": "//input[@id='DateRange']",
        "lblBetListTitle": "//div[contains(@class,'betlist-container')]/div[@class='content-title']",
        "icoClosePopup": "//div[@class='popup-container show']/div/div/a[@class='popup-close']",
        "lblPopupTitle": "//div[@class='popup-container show']/div/div[@class='popup-title']/div[@class='txt-title']",
        "titleReport": "//span[@id='page-title']",
        "icoUserGuide": "//i[@class='icon-book right']",
        "icoExportExcel": "//i[@class='icon-excel right']",
    },
}

REGEX = {"token": '__RequestVerificationToken" type="hidden" value="(.+)"'}
