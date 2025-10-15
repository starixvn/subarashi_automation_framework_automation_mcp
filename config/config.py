from pathlib import Path
from typing import ClassVar


class Config:
    ROOT_DIR = Path(__file__).parent.parent
    ENVIRONMENT = "local"
    SITE = "lap"
    LANGUAGE = "en"
    BROWSER = "chromium"
    HEADLESS = False
    TIMEOUT = 30
    DEBUG = False
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_IDS = []
    TEAMS_CONVERSATION_IDS = []
    SLACK_BOT_TOKEN = "xoxb-8352731735536-8948054884291-ZWQ933ANuC1mc4eoRxDp6g5h"
    SLACK_CHANNEL_ID = "C08USD10388"
    GOOGLE_SHEETS_ID = "1S3ynvvSHgq8hw3I34g15wAc_c3jWJ30LFCJoYJJLyP0"
    GOOGLE_SHEETS_ENABLED = True
    SCREENSHOT_ON_FAILURE = True
    VIDEO_ON_FAILURE = False
    FULL_PAGE_SCREENSHOT = True
    NOTIFY_ON_FAILURE = True
    NOTIFY_PASS_RATE_THRESHOLD = 95.0
    URLS: ClassVar[dict[str, dict[str, str]]] = {
        "lap": {
            "local": {
                "url": "https://lap.nexdev.net/LAP/12bet?Language=en",
                "apiurl": "https://lap-playeradmin1.nexdev.net",
                "lrfurl": "https://lrf.nexdev.net/LRF9",
                "analyticsurl": "https://lap.nexdev.net/LAP6/12betv5/App/App",
            },
            "uat": {
                "url": "http://lap.starixuat.com:8081/nbt53p9",
                "analyticsurl": "https://analytics.amazzu.com",
            },
            "prod": {
                "url": "https://portal8.bpadmin999.com/nbt53p9",
                "analyticsurl": "https://analytics.amazzu.com",
            },
        },
        "lrf": {
            "local": {
                "url": "https://lrf.nexdev.net/LRF1/Authorization/SignIn?=NotAllow",
                "folder": "/LRF1",
                "url_access_token": "https://bt.amazzu.com/",
            },
            "uat": {
                "url": "https://lrf.starixuat.com/LRF4/Authorization/SignIn?=NotAllow",
                "folder": "/LRF4",
                "url_access_token": "https://lapbt1.starixuat.com",
            },
            "prod": {
                "url": "https://internal.amazzu.com/Authorization/SignIn?umtoken=2ZJy-zk4ygITRRXMj_mgIw2",  # "https://internal.amazzu.com/Authorization/SignIn?umtoken=hxnFJdAlajJO0VVYM6UoYw2"#"https://internal.amazzu.com/Authorization/SignIn?umtoken=hxnFJdAlajJO0VVYM6UoYw2"#"https://internal.amazzu.com"
                "folder": "",
                "url_access_token": "https://bt.amazzu.com",
            },
        },
    }

    CREDENTIALS_DATABASE: ClassVar[dict[str, dict[str, dict[str, str]]]] = {
        "Username": {
            "local": "testteam",
        },
        "Password": {
            "local": "@quality#",
        },
    }
