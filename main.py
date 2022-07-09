import requests, json, constants, pickle, os
from datetime import datetime
from InstagramAuth import InstagramAuth


# Get the id of the instagram user
def get_user_id(username: str, auth_session: requests.Session) -> str:
    url_to_request: str = constants.BASED_URL + username
    request: str = auth_session.get(url_to_request)
    if request.status_code == 200:
        return request.text.split('"id":"')[1].split('","')[0]
    else:
        return None

# Get the followers list of the user
def get_followers_list(user_id: str, auth_session: requests.Session) -> list:
    url_to_request: str = constants.BASED_URL + f"graphql/query/?query_id=17851374694183129&id={user_id}&first=10"
    request: str = auth_session.get(url_to_request)
    edges = []
    if request.status_code == 200:
        json_data = json.loads(request.text)
        #has_next_page = json_data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
        edges.append(json_data["data"]["user"]["edge_followed_by"]["edges"])
        """ while has_next_page:
            end_cursor = json_data["data"]["user"]["page_info"]["end_cursor"]
            url_to_request = constants.BASED_URL + f"graphql/query/?query_id=17851374694183129&id={user_id}&first=10&after={end_cursor}"
            request = auth_session.get(url_to_request)
            if request.status_code == 200:
                json_data = json.loads(request.text)
                has_next_page = json_data["data"]["user"]["page_info"]["has_next_page"]
                edges.append(json_data["data"]["user"]["edge_followed_by"]["edges"])
        edges.append(json_data["data"]["user"]["edge_followed_by"]["edges"]) """
        return edges
    else:
        return None

# Get the following list of the user
def get_following_list(user_id: str, auth_session: requests.Session) -> list:
    url_to_request: str = constants.BASED_URL + f"graphql/query/?query_id=17874545323001329&id={user_id}&first=10"
    request: str = auth_session.get(url_to_request)
    edges = []
    if request.status_code == 200:
        json_data = json.loads(request.text)
        has_next_page = json_data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
        edges.append(json_data["data"]["user"]["edge_follow"]["edges"])
        """ while has_next_page:
            end_cursor = json_data['data']['user']['edge_follow']['page_info']['end_cursor']
            url_to_request = constants.BASED_URL + f"graphql/query/?query_id=17874545323001329&id={user_id}&first=10&after={end_cursor}"
            request = auth_session.get(url_to_request)
            if request.status_code == 200:
                json_data = json.loads(request.text)
                has_next_page = json_data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
                edges.append(json_data["data"]["user"]["edge_follow"]["edges"])
        edges.append(json_data["data"]["user"]["edge_follow"]["edges"]) """
        return edges
    else:
        return None

#Load settings from the settings file
def load_settings() -> dict:
    with open (constants.SETTINGS_FILE_PATH, "r") as f:
        settings = json.loads(f.read())
    f.close()
    return settings

#Save the session in a file
def save_session(auth_session: requests.Session) -> None:
    with open(constants.SESSION_SAVE_FILE_PATH, "wb") as f:
        f.write(pickle.dumps(auth_session))
    f.close()

#Load the session from a file
def load_session() -> requests.Session:
    with open(constants.SESSION_SAVE_FILE_PATH, "rb") as f:
        session = pickle.loads(f.read())
    f.close()
    return session

#Check if the session save file exists
def check_session_save_file() -> bool:
    if os.path.exists(constants.SESSION_SAVE_FILE_PATH):
        return True
    else:
        return False

#Check if cookies didn't expire
def verify_cookies_expire(auth_session: requests.Session) -> bool:
    for cookie in auth_session.cookies:
        if cookie.is_expired():
            return True
        else:
            return False


settings = load_settings()

if check_session_save_file():
    print("SESSION FILE FOUND\nLOADING SESSION\n")
    auth_session = load_session()
    print("SESSION LOADED\nVERIFYING COOKIES\n")
    if verify_cookies_expire(auth_session) is False:
        print("COOKIES OK\n")
        print("LOGGED IN\n")
    else:
        print("COOKIES EXPIRED\n")
        print("LOGGING IN\n")
        auth_session = InstagramAuth(settings["username_account"], settings["password_account"]).get_session()
        print("LOGGED IN\n")
        save_session(auth_session)
        print("SESSION SAVED\n")
else:
    auth_session = InstagramAuth(settings["username_account"], settings["password_account"]).get_session()
    save_session(auth_session)


user_id = get_user_id(settings["username_target_account"], auth_session)
print(get_following_list(user_id, auth_session))

