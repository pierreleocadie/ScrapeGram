from Queries import Queries
from SessionProcessing import SessionProcessing

def main() -> None:
    session_processing = SessionProcessing()
    queries = Queries()

    settings = session_processing.load_settings()
    session = session_processing.auth_session(settings)
    user_id = queries.get_user_id(settings["username_target_account"], session)
    print(queries.get_following_list(user_id, session))

if __name__ == "__main__":
    main()
