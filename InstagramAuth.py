import requests, constants, json
from encrypt_password import encrypt_password
from bs4 import BeautifulSoup

class InstagramAuth:
    
    def __init__(self, username: str, password: str) -> None:
        self.session: requests.Session = requests.Session()
        self.username: str = username
        self.password: str = self.enc_password(password)
        self.csrftoken: str = self.get_csrftoken()
        self.mid: str = self.get_mid()
        
        self.session.headers.update({
            "user-agent": constants.USER_AGENT,
            "X-CSRFToken": self.csrftoken,
        })
        self.session.cookies.update({
            "mid": self.mid,
            "csrftoken": self.csrftoken,
        })
        self.payload: dict = {
            "username": self.username,
            "enc_password": self.password,
        }
        
        self.login_request = self.login(self.payload)
        print(f"LOGIN REQUEST STATUS CODE : {self.login_request.status_code}\nLOGIN REQUEST TEXT : {self.login_request.text}\n")
    
    def enc_password(self, password: str) -> str:
        request = requests.get(constants.LOGIN_URL)
        key_id = int(request.headers["ig-set-password-encryption-web-key-id"])
        pub_key = request.headers["ig-set-password-encryption-web-pub-key"]
        key_version = int(request.headers["ig-set-password-encryption-web-key-version"])
        enc_password = encrypt_password(key_id, pub_key, password, key_version)
        return enc_password
    
    def get_csrftoken(self) -> str:
        request = requests.get(constants.BASED_URL)
        soup = BeautifulSoup(request.text, "html.parser")
        script = soup.findAll("script", {"type": "text/javascript"})[3].text
        raw_data = script.replace(";", "").replace("window._sharedData = ", "")
        json_data = json.loads(raw_data)
        csrftoken = json_data["config"]["csrf_token"]
        return csrftoken
    
    def get_mid(self) -> str:
        request = requests.get(constants.MID_URL)
        mid = request.text
        return mid
    
    def login(self, payload: dict) -> requests.Session:
        login_request = self.session.post(constants.LOGIN_URL, data=payload, allow_redirects=True)
        return login_request

    def get_session(self) -> requests.Session:
        return self.session


if __name__ == "__main__":
    print(InstagramAuth("username", "password").get_session())