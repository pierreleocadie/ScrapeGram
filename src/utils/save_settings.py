import json, constants

def save_settings(username: str, password: str, target_account: str) -> None:
    with open(constants.SETTINGS_FILE_PATH, "r") as f:
        settings = json.loads(f.read())
    settings["username_account"] = username
    settings["password_account"] = password
    settings["username_target_account"] = target_account
    with open(constants.SETTINGS_FILE_PATH, "w") as f:
        f.write(json.dumps(settings, indent=4))

if __name__ == "__main__":
    save_settings("username", "password", "target_account")