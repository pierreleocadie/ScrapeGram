import requests, constants, logging
from bs4 import BeautifulSoup

class GetHeaders:
    
    def get_ig_set_password_encryption_web_key_id(self) -> str:
        request = requests.get(constants.LOGIN_URL)
        key_id: str = request.headers["ig-set-password-encryption-web-key-id"]
        return key_id
    
    def get_ig_set_password_encryption_web_pub_key(self) -> str:
        request = requests.get(constants.LOGIN_URL)
        pub_key = request.headers["ig-set-password-encryption-web-pub-key"]
        return pub_key
    
    def get_ig_set_password_encryption_web_key_version(self) -> str:
        request = requests.get(constants.LOGIN_URL)
        key_version = request.headers["ig-set-password-encryption-web-key-version"]
        return key_version
    
    def get_ig_app_id(self) -> str:
        request = requests.get(constants.IG_APP_ID_URL)
        if request.status_code == 200:
            splt = request.text.split(",")
            for i in splt:
                if "e.instagramWebDesktopFBAppId" in i:
                    app_id = i.split("=")[1].replace("'", "")
                    return app_id
    

if __name__ == "__main__":
    print(GetHeaders().get_ig_app_id())