import requests, constants, json, logging
from utils.encrypt_password import encrypt_password
from GetCookie import GetCookie
from GetHeader import GetHeader

class InstagramAuth:
    
    def __init__(self, username: str, password: str) -> None:
        logging.info("Authenticating...")
        self.session: requests.Session = requests.Session()
        self.username: str = username
        self.password: str = self.enc_password(password)
        self.csrftoken: str = GetCookie().get_csrftoken()
        self.mid: str = GetCookie().get_mid()
        
        self.session.headers.update({
            "user-agent": constants.USER_AGENT,
            "X-CSRFToken": self.csrftoken,
        })
        logging.debug("Session headers updated")
        self.session.cookies.update({
            "mid": self.mid,
            "csrftoken": self.csrftoken,
        })
        logging.debug("Session cookies updated")
        self.payload: dict = {
            "username": self.username,
            "enc_password": self.password,
        }
        logging.debug("Payload created")
        
        self.login_request = self.login(self.payload)
    
    def enc_password(self, password: str) -> str:
        logging.info("Encrypting password...")
        key_id = int(GetHeader().get_ig_set_password_encryption_web_key_id())
        logging.debug(f"key_id : {key_id}")
        pub_key = GetHeader().get_ig_set_password_encryption_web_pub_key()
        logging.debug(f"pub_key : {pub_key}")
        key_version = int(GetHeader().get_ig_set_password_encryption_web_key_version())
        logging.debug(f"key_version : {key_version}")
        enc_password = encrypt_password(key_id, pub_key, password, key_version)
        logging.debug(f"enc_password : {enc_password}")
        logging.info("Password encrypted")
        return enc_password
    
    def login(self, payload: dict) -> requests.Session:
        login_request = self.session.post(constants.LOGIN_URL, data=payload, allow_redirects=True)
        logging.debug("Login request sent")
        logging.debug(f"LOGIN REQUEST STATUS CODE : {login_request.status_code}")
        logging.info(f"LOGIN REQUEST TEXT : {login_request.text}\n")
        return login_request

    def get_session(self) -> requests.Session:
        return self.session


if __name__ == "__main__":
    print(InstagramAuth("username", "password").enc_password("password"))