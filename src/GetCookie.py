import requests, json, logging, constants
from bs4 import BeautifulSoup

class GetCookie:
    
    def get_csrftoken(self) -> str:
        request = requests.get(constants.BASED_URL)
        soup = BeautifulSoup(request.text, "html.parser")
        script = soup.findAll("script")
        for i in script:
            if "csrf_token\\" in i.text:
                csrftoken = i.text.split('"')[i.text.split('"').index("csrf_token\\")+2][:-1]
                logging.debug(f"csrftoken : {csrftoken}")
                logging.info("csrftoken retrieved")
                return csrftoken
    
    def get_mid(self) -> str:
        request = requests.get(constants.MID_URL)
        mid = request.text
        logging.debug(f"mid : {mid}")
        logging.info("mid retrieved")
        return mid

if __name__ == "__main__":
    print(GetCookie().get_csrftoken())
    #print(GetCookie().get_mid())