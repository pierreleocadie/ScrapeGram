import requests, json, constants, time, random, logging

class Queries:
    
    def random_sleep_timer(self, min_delay_between_request: int, max_delay_between_request: int) -> None:
        timer: int = random.randint(min_delay_between_request, max_delay_between_request)
        logging.debug(f"Sleeping for {timer} seconds")
        time.sleep(timer)
    
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
                number_of_followers: int = based_dict["count"]
                edges.append(based_dict["edges"])
                if has_next_page and queries_parameters["max_number_of_edges_to_get"] > 1:
                    end_cursor: str = based_dict["page_info"]["end_cursor"]
                    url_to_request + f"&after={end_cursor}"
                    self.random_sleep_timer(queries_parameters["min_delay_between_request"], 
                                            queries_parameters["max_delay_between_request"])
                else:
                    break
            else:
                return None
        return edges