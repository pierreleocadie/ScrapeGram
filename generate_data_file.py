import os, constants, pickle, requests
from Queries import Queries

def generate_data_file(path: str, queries: Queries, get_followers_or_following: str, user_id: str, session: requests.Session, queries_parameters: dict) -> None:
    if not os.path.exists(path):
        print("No data found. Generating...")
        data: list = queries.get_followers_following_list(user_id, session, get_followers_or_following, queries_parameters)
        if not os.path.exists(constants.USER_OUTPUT_FOLDER_PATH):
            os.mkdir(constants.USER_OUTPUT_FOLDER_PATH)
        with open(path, 'wb') as f:
            pickle.dump(data, f)