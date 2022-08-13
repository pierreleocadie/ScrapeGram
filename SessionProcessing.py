import json, constants, pickle, os, requests, logging
from InstagramAuth import InstagramAuth

class SessionProcessing:
    
    #Load settings from the settings file
    def load_settings(self) -> dict:
        with open (constants.SETTINGS_FILE_PATH, "r") as f:
            settings = json.loads(f.read())
            logging.info(f"Settings loaded from {constants.SETTINGS_FILE_PATH}")
        return settings
    
    #Save the session in a file
    def save_session(self, session: requests.Session) -> None:
        with open(constants.SESSION_SAVE_FILE_PATH, "wb") as f:
            f.write(pickle.dumps(session))
            logging.info(f"Session saved to {constants.SESSION_SAVE_FILE_PATH}")
    
    #Load the session from a file
    def load_session(self) -> requests.Session:
        with open(constants.SESSION_SAVE_FILE_PATH, "rb") as f:
            session = pickle.loads(f.read())
            logging.info(f"Session loaded from {constants.SESSION_SAVE_FILE_PATH}")
        return session
    
    #Check if the session save file exists
    def check_session_save_file(self) -> bool:
        if os.path.exists(constants.SESSION_SAVE_FILE_PATH):
            logging.info(f"Session save file found at {constants.SESSION_SAVE_FILE_PATH}")
            return True
        else:
            logging.info(f"Session save file not found at {constants.SESSION_SAVE_FILE_PATH}")
            return False
    
    #Check if cookies didn't expire
    def verify_cookies_expire(self, session: requests.Session) -> bool:
        for cookie in session.cookies:
            if cookie.is_expired():
                logging.info("Cookies expired")
                return True
            else:
                logging.info("Cookies not expired")
                return False
    
    def auth_session(self, settings) -> requests.Session:
        if self.check_session_save_file():
            session = self.load_session()
            if self.verify_cookies_expire(session) is False:
                logging.info("Session verified")
                logging.info("Logged in")
            else:
                session = InstagramAuth(settings["username_account"], settings["password_account"]).get_session()
                logging.info("Logged in")
                self.save_session(session)
        else:
            session = InstagramAuth(settings["username_account"], settings["password_account"]).get_session()
            logging.info("Logged in")
            self.save_session(session)
        return session

if __name__ == "__main__":
    print(SessionProcessing().load_settings())