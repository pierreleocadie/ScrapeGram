import json, constants, pickle, os, requests
from InstagramAuth import InstagramAuth

class SessionProcessing:
    
    #Load settings from the settings file
    def load_settings(self) -> dict:
        with open (constants.SETTINGS_FILE_PATH, "r") as f:
            settings = json.loads(f.read())
        f.close()
        return settings
    
    #Save the session in a file
    def save_session(self, session: requests.Session) -> None:
        with open(constants.SESSION_SAVE_FILE_PATH, "wb") as f:
            f.write(pickle.dumps(session))
        f.close()
    
    #Load the session from a file
    def load_session(self) -> requests.Session:
        with open(constants.SESSION_SAVE_FILE_PATH, "rb") as f:
            session = pickle.loads(f.read())
        f.close()
        return session
    
    #Check if the session save file exists
    def check_session_save_file(self) -> bool:
        if os.path.exists(constants.SESSION_SAVE_FILE_PATH):
            return True
        else:
            return False
    
    #Check if cookies didn't expire
    def verify_cookies_expire(self, session: requests.Session) -> bool:
        for cookie in session.cookies:
            if cookie.is_expired():
                return True
            else:
                return False
    
    def auth_session(self, settings) -> requests.Session:
        if self.check_session_save_file():
            print("SESSION FILE FOUND\nLOADING SESSION")
            session = self.load_session()
            print("SESSION LOADED\nVERIFYING COOKIES")
            if self.verify_cookies_expire(session) is False:
                print("COOKIES OK\nLOGGED IN\n")
            else:
                print("COOKIES EXPIRED\nLOGGING IN")
                session = InstagramAuth(settings["username_account"], settings["password_account"]).get_session()
                print("LOGGED IN")
                self.save_session(session)
                print("SESSION SAVED")
        else:
            session = InstagramAuth(settings["username_account"], settings["password_account"]).get_session()
            self.save_session(session)
        return session

if __name__ == "__main__":
    print(SessionProcessing().load_settings())
