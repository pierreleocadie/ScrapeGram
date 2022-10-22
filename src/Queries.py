import requests, json, constants, logging, os
from GetHeader import GetHeader
from utils.random_sleep_timer import random_sleep_timer

class Queries:
    
    # Get the id of the instagram target user
    def get_user_id(self, username: str, auth_session: requests.Session) -> str:
        url_to_request: str = f"{constants.BASED_URL}/{username}"
        request: str = auth_session.get(url_to_request)
        if request.status_code == 200:
            user_id: str = request.text.split('"id":"')[1].split('","')[0]
            logging.debug(f"User id: {user_id}")
            logging.info(f"User id found for {username} : {user_id}")
            return user_id
        else:
            return None
    
    # Get the followers list or the following list of the target user
    def get_followers_following_list(self, user_id: str, auth_session: requests.Session, get_followers_or_following: str, queries_parameters: dict) -> list:
        edges: list = []
        url_to_request: str = f"""{constants.BASED_URL}/graphql/query/?query_id={constants.GET_FOLLOWERS_LIST_QUERY_ID if get_followers_or_following == "followers" else constants.GET_FOLLOWING_LIST_QUERY_ID}&id={user_id}&first={queries_parameters['number_of_followers_following_to_get_per_edge']}"""
        for _ in range(queries_parameters["max_number_of_edges_to_get"]):
            request: str = auth_session.get(url_to_request)
            if request.status_code == 200:
                json_data: dict = json.loads(request.text)
                based_dict: dict = json_data["data"]["user"]
                based_dict = based_dict["edge_followed_by"] if get_followers_or_following == "followers" else based_dict["edge_follow"]
                has_next_page: bool = based_dict["page_info"]["has_next_page"]
                edges.append(based_dict["edges"])
                if has_next_page and queries_parameters["max_number_of_edges_to_get"] > 1:
                    end_cursor: str = based_dict["page_info"]["end_cursor"]
                    url_to_request + f"&after={end_cursor}"
                    random_sleep_timer(queries_parameters["min_delay_between_request"], 
                                            queries_parameters["max_delay_between_request"])
                else:
                    break
            else:
                return None
        return edges
    
    # Duplicate the session, keep only csrftoken, ig_did, mid and return the new session
    def duplicate_session(self, auth_session: requests.Session) -> requests.Session:
        new_auth_session: requests.Session = requests.Session()
        new_auth_session.cookies = auth_session.cookies
        # The issue here, is that we have two csrftoken cookies,
        # one have a value and the other one is empty, so we have to identify the one empty and delete it
        for cookie in new_auth_session.cookies:
            if cookie.name == "csrftoken" and cookie.domain == "":
                cookie.name = f"csrftoken0"
        new_auth_session.cookies.pop("ds_user_id")
        new_auth_session.cookies.pop("rur")
        new_auth_session.cookies.pop("sessionid")
        auth_session_cookies_copy: requests.cookies.RequestsCookieJar = new_auth_session.cookies.copy()
        auth_session_cookies_copy.clear()
        auth_session_cookies_copy.set(new_auth_session.cookies.keys()[1], new_auth_session.cookies.values()[1])
        auth_session_cookies_copy.set(new_auth_session.cookies.keys()[2], new_auth_session.cookies.values()[2])
        auth_session_cookies_copy.set(new_auth_session.cookies.keys()[3], new_auth_session.cookies.values()[3])
        new_auth_session.cookies = auth_session_cookies_copy
        return new_auth_session

    # Download the target user web profile info to avoid doing too many requests
    def download_web_profile_info(self, username_target_account: str, auth_session: requests.Session) -> None:
        url_to_request: str = constants.WEB_PROFILE_INFO_URL(username_target_account)
        new_auth_session: requests.Session = self.duplicate_session(auth_session)
        logging.debug(f"URL to request: {url_to_request}")
        logging.debug(f"Session duplicated, Session cookies: {new_auth_session.cookies.keys()}")
        request: str = requests.get(url_to_request, cookies=new_auth_session.cookies, headers={"X-IG-App-ID": GetHeader().get_ig_app_id()})
        if request.status_code == 200:
            json_data: dict = json.loads(request.text)
            if not os.path.exists(constants.TMP_FOLDER_PATH):
                os.mkdir(constants.TMP_FOLDER_PATH)
            with(open(constants.USER_WEB_PROFILE_INFO_FILE_PATH(username_target_account), "w")) as file:
                file.write(json.dumps(json_data, indent=4))
            return True
        else:
            return False
    
    # Load the target user web profile info from the file
    def load_web_profile_info(self, username_target_account: str) -> dict:
        with(open(constants.USER_WEB_PROFILE_INFO_FILE_PATH(username_target_account), "r")) as file:
            json_data: dict = json.loads(file.read())
        return json_data
    
    # Delete the target user web profile info file
    def delete_web_profile_info(self, username_target_account: str) -> None:
        if os.path.exists(constants.USER_WEB_PROFILE_INFO_FILE_PATH(username_target_account)):
            os.remove(constants.USER_WEB_PROFILE_INFO_FILE_PATH(username_target_account))
    
    # Check if the target user web profile info is already downloaded
    def check_if_web_profile_info_is_already_downloaded(self, username_target_account: str) -> bool:
        return os.path.exists(constants.USER_WEB_PROFILE_INFO_FILE_PATH(username_target_account))
    
    # Return the target user web profile info
    def get_web_profile_info(self, username_target_account: str, auth_session: requests.Session) -> dict:
        if self.check_if_web_profile_info_is_already_downloaded(username_target_account):
            return self.load_web_profile_info(username_target_account)["data"]["user"]
        else:
            self.download_web_profile_info(username_target_account, auth_session)
            return self.load_web_profile_info(username_target_account)["data"]["user"]
    
    # Check if the target user profile is private
    def is_user_profile_private(self, username_target_account: str, auth_session: requests.Session) -> bool:
        return self.get_web_profile_info(username_target_account, auth_session)["is_private"]
    
    # Get the number of followers of the target user
    def get_number_of_followers(self, username_target_account: str, auth_session: requests.Session) -> int:
        return self.get_web_profile_info(username_target_account, auth_session)["edge_followed_by"]["count"]
    
    # Get the number of following of the target user
    def get_number_of_following(self, username_target_account: str, auth_session: requests.Session) -> int:
        return self.get_web_profile_info(username_target_account, auth_session)["edge_follow"]["count"]
    
    # Get the biography of the target user
    def get_biography(self, username_target_account: str, auth_session: requests.Session) -> str:
        biography: str = self.get_web_profile_info(username_target_account, auth_session)["biography"]
        biography_links: list = self.get_web_profile_info(username_target_account, auth_session)["bio_links"]
        biography_with_entities: str = self.get_web_profile_info(username_target_account, auth_session)["biography_with_entities"]["entities"]
        return biography, biography_links, biography_with_entities


if __name__ == "__main__":
    pass