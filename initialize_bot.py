# initialize_bot.py
import os
import sys
import argparse
import json

from instagram_util.hashtags import get_related_hashtags

def create_directory_structure(username):
    base_path = f"accounts/{username}"
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(f"{base_path}/queue", exist_ok=True)
    os.makedirs(f"{base_path}/archive", exist_ok=True)

    return base_path

def save_config(username, password, api_key, summary, hashtags, path):
    config = {
        "username": username,
        "password": password,
        "api_key": api_key,
        "summary": summary,
        "hashtags": hashtags
    }

    with open(f"{path}/config.json", "w") as config_file:
        json.dump(config, config_file, indent=2)

def create_prompt_file(username, summary, hashtags, path):
    with open("master_prompt.txt", "r") as master_prompt_file:
        master_prompt = master_prompt_file.read()

    master_prompt = master_prompt.replace("INSTAGRAM_USERNAME", username)
    master_prompt = master_prompt.replace("ACCOUNT_SUMMARY", summary)
    master_prompt = master_prompt.replace("RELATED_HASHTAGS", hashtags)

    with open(f"{path}/prompt.txt", "w") as prompt_file:
        prompt_file.write(master_prompt)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Instagram username")
    parser.add_argument("password", help="Instagram password")
    parser.add_argument("api_key", help="GPT API key")

    args = parser.parse_args()

    username = args.username
    password = args.password
    api_key = args.api_key

    summary = input("Please enter an account summary: ")

    # force at least one hashtag
    hashtags_input = ''
    while not hashtags_input.strip():
        hashtags_input = input("Please enter at least one related hashtag separated by commas: ")

    hashtags = get_related_hashtags([hashtag.strip().replace('#', '') for hashtag in hashtags_input.split(',')])

    path = create_directory_structure(username)
    save_config(username, password, api_key, summary, hashtags, path)
    create_prompt_file(username, summary, hashtags, path)

if __name__ == "__main__":
    main()
