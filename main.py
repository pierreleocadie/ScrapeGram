from Queries import Queries
from SessionProcessing import SessionProcessing
import pickle, os

def follow_data_processing(follow_data: list) -> list:
    for edge in follow_data:
        for follow in edge:
            print("{:<20}{:>20}".format(follow["node"]["id"], follow["node"]["username"]))

def main() -> None:
    session_processing = SessionProcessing()
    queries = Queries()

    settings = session_processing.load_settings()
    session = session_processing.auth_session(settings)
    user_id = queries.get_user_id(settings["username_target_account"], session)
    
    if not os.path.exists("data/followers_data.pickle"):
        print("No followers data found. Generating...")
        followers_data = queries.get_followers_list(user_id, 
                                                    session, 
                                                    settings["max_number_of_edges_to_get"], 
                                                    settings["min_delay_between_requests"], 
                                                    settings["max_delay_between_requests"])
        if not os.path.exists("data"):
            os.mkdir("data")
        with open("data/followers_data.pickle", 'wb') as f:
            pickle.dump(followers_data, f)
    else:
        print("Followers data found. Loading...")
        with open("data/followers_data.pickle", 'rb') as f:
            followers_data = pickle.load(f)
    
    
    if not os.path.exists("data/following_data.pickle"):
        print("No following data found. Generating...")
        following_data = queries.get_following_list(user_id, 
                                                    session, 
                                                    settings["max_number_of_edges_to_get"], 
                                                    settings["min_delay_between_requests"], 
                                                    settings["max_delay_between_requests"])
        if not os.path.exists("data"):
            os.mkdir("data")
        with open("data/following_data.pickle", 'wb') as f:
            pickle.dump(following_data, f)
    else:
        print("Following data found. Loading...")
        with open("data/following_data.pickle", 'rb') as f:
            following_data = pickle.load(f)
    
    follow_data_processing(followers_data)
    print("\n")
    follow_data_processing(following_data)

if __name__ == "__main__":
    main()
