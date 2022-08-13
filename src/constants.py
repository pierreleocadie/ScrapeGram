import os, datetime

BASED_URL: str = "https://www.instagram.com"
LOGIN_URL: str = f"{BASED_URL}/accounts/login/ajax/?hl=fr"
MID_URL: str = f"{BASED_URL}/web/__mid/"

if not os.path.exists(os.path.join("src", "logs")):
    os.mkdir(os.path.join("src", "logs"))

LOGS_PATH: str = os.path.join("src", "logs", f"{datetime.date.today()}.log")

SESSION_SAVE_FILE_PATH: str = os.path.join("src", "session_saves", "session_save.pickle")
SETTINGS_FILE_PATH: str = os.path.join("src", "settings.json")

USER_OUTPUT_FOLDER_PATH: str = "OUTPUT"
USER_OUTPUT_FOLLOWING_DATA_FILE_PATH: str = os.path.join(USER_OUTPUT_FOLDER_PATH, "following_data.pickle")
USER_OUTPUT_FOLLOWERS_DATA_FILE_PATH: str = os.path.join(USER_OUTPUT_FOLDER_PATH, "followers_data.pickle")

GET_FOLLOWERS_LIST_QUERY_ID: str = "17851374694183129"
GET_FOLLOWING_LIST_QUERY_ID: str = "17874545323001329"


USER_AGENT: str = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"