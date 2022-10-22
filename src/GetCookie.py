import requests, json, logging, constants
from bs4 import BeautifulSoup

class GetCookie:
    
    def get_csrftoken(self) -> str:
        request = requests.get(constants.BASED_URL)
        soup = BeautifulSoup(request.text, "html.parser")
        script = soup.findAll("script", {"type": "text/javascript"})[3].text
        raw_data = script.replace(";", "").replace("window._sharedData = ", "")
        json_data = json.loads(raw_data)
        csrftoken = json_data["config"]["csrf_token"]
        logging.debug(f"csrftoken : {csrftoken}")
        logging.info("csrftoken retrieved")
        return csrftoken
    
    def get_mid(self) -> str:
        request = requests.get(constants.MID_URL)
        mid = request.text
        logging.debug(f"mid : {mid}")
        logging.info("mid retrieved")
        return mid