# start_bot.py
import argparse
import json
import os
import random
import re
import time
import uuid
from datetime import datetime

import openai
from instagrapi import Client
from PIL import Image

from instagram_util.feedback import get_post_metrics
from instagram_util.convert_jpg import convert_to_jpg

def load_config(account_dir):
    try:
        with open(f"accounts/{account_dir}/config.json") as config_file:
            config = json.load(config_file)
        return config
    except:
        raise ValueError(f'Could not find an account with the name {account_dir}. please create an account first with initialize_bot.py')

def should_post(prompt, post_count=3):
    if re.search(r"\[POST [a-z0-9]{19}\]", prompt) is None:
        return True
    message = f"Should we post another photo, dont post more than {post_count} times per day? the current time and date are {datetime.now().strftime('%A, %B %d, %H:%M')}. Answer with just 'yes or 'no'"
    response = run_gpt(prompt, message)
    if 'yes' in response.strip().lower():
        return True
    return False

def start_post(prompt, project_name):
    id = uuid.uuid4().hex
    prompt = prompt + f"\n\n[POST {id}]"
    image_path, description = get_image(project_name)
    prompt = prompt + f"\nIMAGE: {image_path}"
    prompt, caption = get_caption(prompt, description)
    prompt = get_timestamp(prompt)
    prompt = prompt + f"\nLIKE_COUNT: "
    prompt = prompt + f"\nCOMMENT_COUNT: "
    return prompt, caption, image_path

def get_image(project_name):
    images = os.listdir(os.path.join("accounts", project_name, "queue"))
    if len(images) == 0:
        raise ValueError("Please add images with descriptive names with words separated by _ (ie. photo_of_house_in_san_francisco.jpg) to accounts/USERNAME/queue")
    image_fn = random.choice(images)
    image_description = image_fn.split('.')[0].split('_')
    image_description = ' '.join(image_description)
    # convert to jpg if other filetype
    image_path = convert_to_jpg(os.path.join("accounts", project_name, "queue", image_fn))
    return image_path, image_description

def get_caption(prompt, description):
    message = f"create the instagram post from the image description. \ndescription: {description}. Write the caption in the following format. Include nothing but the caption. \nie. CAPTION: [write caption here]"
    caption = run_gpt(prompt, message)
    caption = caption.replace("Caption:", "").replace("CAPTION:", "").replace('"', "").strip()
    prompt = prompt + "\nCAPTION: {}".format(caption)
    return prompt, caption

def get_timestamp(prompt):
    timestamp = datetime.now().strftime('%A, %B %d, %H:%M')
    return prompt + f"\nPOST TIMESTAMP: {timestamp}"

def run_gpt(prompt, message):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content']

def post_to_instagram(post_content, image_path, client):
    with open(image_path, 'rb') as image_file:
        return client.photo_upload(image_file.name, caption=post_content)


def replace_uuid_with_pk(text, response_pk):
    pattern = r'\[POST (\w{32})\]'
    matches = list(re.finditer(pattern, text))

    if not matches:
        raise ValueError("No POST entries found.")

    last_match = matches[-1]
    uuid = last_match.group(1)

    return text[:last_match.start(1)] + response_pk + text[last_match.end(1):]

def update_metrics(prompt):
    metrics = get_post_metrics(INSTAGRAM_USERNAME, instagram_client)
    prompt_lines = prompt.split('\n')
    updated_prompt = []

    for line in prompt_lines:
        if line.startswith("[POST "):
            post_id = line[6:-1]
            post_metrics = next((m for m in metrics if m['id'].split('_')[0] == post_id), None)
            if post_metrics:
                updated_prompt.append(line)
                continue

        if "LIKE_COUNT:" in line:
            if post_metrics:
                line = f"LIKE_COUNT: {post_metrics['likes']}"
        elif "COMMENT_COUNT:" in line:
            if post_metrics:
                line = f"COMMENT_COUNT: {post_metrics['comments']}"

        updated_prompt.append(line)

    return "\n".join(updated_prompt)


def main_job(project_name, post_count):
    prompt = open(f"accounts/{project_name}/prompt.txt", "r").read()
    if should_post(prompt, post_count): # and there are images in the queue
        print(f"Posting - {project_name}")
        prompt = update_metrics(prompt)
        prompt, post_content, image_path = start_post(prompt, project_name)

        try:
            response = post_to_instagram(post_content, image_path, instagram_client)
            prompt = replace_uuid_with_pk(prompt, response.pk)
            if not isinstance(response, Exception):
                with open(f"accounts/{project_name}/prompt.txt", "w") as f:
                    f.write(prompt)
            # move image to archive dir
            os.rename(image_path, os.path.join('accounts', project_name, 'archive', os.path.basename(image_path)))
        except Exception as e:
            print(e)
    else:
        print(f"Not posting - {project_name}")
        prompt = update_metrics(prompt)
        with open(f"accounts/{project_name}/prompt.txt", "w") as f:
            f.write(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("account_dir", help="Account directory path")
    parser.add_argument("post_count", help="Number of times the bot should post per day", type=int)
    args = parser.parse_args()
    account_dir = args.account_dir
    post_count = args.post_count

    config = load_config(account_dir)
    openai.api_key = config['api_key']
    INSTAGRAM_USERNAME = config['username']
    INSTAGRAM_PASSWORD = config['password']

    instagram_client = Client()
    time.sleep(5)  # Wait for 5 seconds before logging in to prevent rate limiting
    instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

    project_name = account_dir.rstrip('/')  # Use the account directory as the project_name

    while True:
        main_job(project_name, post_count)
        time.sleep(3600)
