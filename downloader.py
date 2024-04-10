import urllib.request
import json
import os
from urllib.parse import unquote
from datetime import datetime


def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def download_file(f, challenge, year):
    file_name = unquote(f["name"])
    file_path = f"files/{year}/{challenge['id']}/{file_name}"

    if not os.path.exists(f"files/{year}/{challenge['id']}"):
        os.makedirs(f"files/{year}/{challenge['id']}")

    if not os.path.exists(file_path):
        print(f"Downloading {file_name} ({f['url']})...")
        with open(file_path, "wb") as file:
            try:
                response = urllib.request.urlopen(
                    urllib.request.Request(
                        f["url"], headers={"User-Agent": "Mozilla/5.0"}
                    )
                )
                file.write(response.read())
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")
                os.remove(file_path)
    else:
        print(f"{file_name} already exists. Skipping download...")


def download_challenge_files(data, year):
    for challenge in data["data"]:
        if "files" in challenge:
            for file in challenge["files"]:
                download_file(file, challenge, year)


def main():
    year = datetime.now().year
    data = load_data(f"{year}/data.json")

    if not os.path.exists(f"files/{year}"):
        os.makedirs(f"files/{year}")

    download_challenge_files(data, year)

    print("Everything has been downloaded successfully.")


if __name__ == "__main__":
    main()
