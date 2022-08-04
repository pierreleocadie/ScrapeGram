import requests, json, constants, time, random

class Queries:
    
    def random_sleep_timer(self) -> None:
        timer: int = random.randint(3, 10)
        print(f"Sleeping for {timer} seconds")
        time.sleep(timer)
    
    # Get the id of the instagram user
    def get_user_id(self, username: str, auth_session: requests.Session) -> str:
        url_to_request: str = constants.BASED_URL + username
        request: str = auth_session.get(url_to_request)
        if request.status_code == 200:
            return request.text.split('"id":"')[1].split('","')[0]
        else:
            return None
    
    # Get the followers list of the user
    def get_followers_list(self, user_id: str, auth_session: requests.Session) -> list:
        url_to_request: str = constants.BASED_URL + f"graphql/query/?query_id=17851374694183129&id={user_id}&first=10"
        request: str = auth_session.get(url_to_request)
        edges = []
        if request.status_code == 200:
            json_data = json.loads(request.text)
            has_next_page = json_data["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]
            numbers_of_followers = json_data["data"]["user"]["edge_followed_by"]["count"]
            edges.append(json_data["data"]["user"]["edge_followed_by"]["edges"])
            """ while has_next_page:
                end_cursor = json_data["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                url_to_request = constants.BASED_URL + f"graphql/query/?query_id=17851374694183129&id={user_id}&first=10&after={end_cursor}"
                self.random_sleep_timer()
                request = auth_session.get(url_to_request)
                if request.status_code == 200:
                    json_data = json.loads(request.text)
                    has_next_page = json_data["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]
                    edges.append(json_data["data"]["user"]["edge_followed_by"]["edges"])
            edges.append(json_data["data"]["user"]["edge_followed_by"]["edges"]) """
            return edges
        else:
            return None
    
    # Get the following list of the user
    def get_following_list(self, user_id: str, auth_session: requests.Session) -> list:
        url_to_request: str = constants.BASED_URL + f"graphql/query/?query_id=17874545323001329&id={user_id}&first=10"
        request: str = auth_session.get(url_to_request)
        edges = []
        if request.status_code == 200:
            json_data = json.loads(request.text)
            print(json_data)
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
    
    def get_followers_following_data(self, follow_list: list[list]):
        for edge in follow_list:
            for follower in edge:
                print(follower)