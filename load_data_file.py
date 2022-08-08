import os
import pickle

def load_data_file(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data

if __name__ == "__main__":
    print(os.path.exists("OUTPUT/followers_data.pickle"))
    print(load_data_file("OUTPUT/followers_data.pickle"))