from Queries import Queries
from SessionProcessing import SessionProcessing
from utils.generate_data_file import generate_data_file
from utils.load_data_file import load_data_file
from utils.save_settings import save_settings
import requests, constants, logging, logging_config, sys

def follow_data_processing(follow_data: list) -> list:
    logging.info(f"Processing and printing followers/following data")
    for edge in follow_data:
        for follow in edge:
            print("{:<20}{:>20}".format(follow["node"]["id"], follow["node"]["username"]))

def main() -> None:
    session_processing = SessionProcessing()
    queries = Queries()

    if len(sys.argv) > 1 and sys.argv[1] == "-u" and sys.argv[3] == "-p" and sys.argv[5] == "-t":
        save_settings(sys.argv[2], sys.argv[4], sys.argv[6])
    settings: dict = session_processing.load_settings()
    session: requests.Session = session_processing.auth_session(settings)
    user_id: str = queries.get_user_id(settings["username_target_account"], session)
    
    queries_parameters: dict = settings["queries_parameters"]
    
    generate_data_file(constants.USER_OUTPUT_FOLLOWERS_DATA_FILE_PATH, queries, "followers", user_id, session, queries_parameters)
    generate_data_file(constants.USER_OUTPUT_FOLLOWING_DATA_FILE_PATH, queries, "following", user_id, session, queries_parameters)
    
    followers_data: dict = load_data_file(constants.USER_OUTPUT_FOLLOWERS_DATA_FILE_PATH)
    following_data: dict = load_data_file(constants.USER_OUTPUT_FOLLOWING_DATA_FILE_PATH)
    
    print("FOLLOWERS : ")
    follow_data_processing(followers_data)
    print("\nFOLLOWING : ")
    follow_data_processing(following_data)
    print("\n")
    print("Target profile private ? ", queries.is_user_profile_private(settings["username_target_account"], session))
    print("Number of followers : ", queries.get_number_of_followers(settings["username_target_account"], session))
    print("Number of following : ", queries.get_number_of_following(settings["username_target_account"], session))
    print("Bio : ", queries.get_biography(settings["username_target_account"], session))
    print("Done")

if __name__ == "__main__":
    main()
