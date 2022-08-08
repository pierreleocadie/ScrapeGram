from Queries import Queries
from SessionProcessing import SessionProcessing
from utils.generate_data_file import generate_data_file
from utils.load_data_file import load_data_file
import requests, constants, logging

def follow_data_processing(follow_data: list) -> list:
    for edge in follow_data:
        for follow in edge:
            print("{:<20}{:>20}".format(follow["node"]["id"], follow["node"]["username"]))

def main() -> None:
    session_processing = SessionProcessing()
    queries = Queries()

    settings: dict = session_processing.load_settings()
    session: requests.Session = session_processing.auth_session(settings)
    user_id: str = queries.get_user_id(settings["username_target_account"], session)
    
    queries_parameters: dict = settings["queries_parameters"]
    
    generate_data_file(constants.USER_OUTPUT_FOLLOWERS_DATA_FILE_PATH, queries, "followers", user_id, session, queries_parameters)
    generate_data_file(constants.USER_OUTPUT_FOLLOWING_DATA_FILE_PATH, queries, "following", user_id, session, queries_parameters)
    
    followers_data: dict = load_data_file(constants.USER_OUTPUT_FOLLOWERS_DATA_FILE_PATH)
    following_data: dict = load_data_file(constants.USER_OUTPUT_FOLLOWING_DATA_FILE_PATH)
    
    follow_data_processing(followers_data)
    print("\n")
    follow_data_processing(following_data)

if __name__ == "__main__":
    main()
