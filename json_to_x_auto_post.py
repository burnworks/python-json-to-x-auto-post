import json
import random
import requests
import tweepy
import os
import hashlib
from requests.exceptions import RequestException

# X API認証情報 (X Authorization)
api_key = os.environ.get('X_API_KEY')
api_secret = os.environ.get('X_API_KEY_SECRET')
access_token = os.environ.get('X_ACCESS_TOKEN')
access_token_secret = os.environ.get('X_ACCESS_TOKEN_SECRET')
bearer_token = os.environ.get('X_BEARER_TOKEN')

# JSONデータのURL (JSON data URL)
json_url = os.environ.get('JSON_URL')

# 投稿履歴ファイル (Posting history JSON file name)
history_file = "post_history.json"

# X の文字制限 (Character limit (280 characters) of X)
CHARACTER_LIMIT = 280 # 0 を指定すると文字制限処理をスキップ (Set to 0 to skip character limit processing)

# X API認証情報が環境変数から正しく取得できるか検証 (Validate if X API credentials are correctly retrieved from environment variables)
def validate_env_vars():
    if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
        print("Missing required environment variables.")
        exit(1)

# 投稿データ用のJSONを取得 (Get JSON file)
def get_posts():
    if not json_url:
        print("JSON URL is not set.")
        return []
    try:
        response = requests.get(json_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Error fetching JSON data: {e}")
        return []

# 投稿履歴用のJSONを取得 (Get posting history JSON file)
def get_post_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading history file: {e}")
            return []
    return []

# 投稿履歴用のJSONを更新 (Update posting history JSON file)
def update_post_history(post_hash):
    history = get_post_history()
    history.append(post_hash)
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f)
    except IOError as e:
        print(f"Error writing to history file: {e}")

# 投稿を選択 (Select post)
def select_post(posts, history):
    # ハッシュ値が履歴に存在しない投稿をフィルタリング (Filtering posts where the hash value does not exist in the history)
    available_posts = [col for col in posts if hashlib.md5(col['text'].encode()).hexdigest() not in history]
    if not available_posts:
        # 重複しないハッシュ値が見つからない場合は1周したと判断し、履歴をリセット (If no duplicate hash value is found, the posting cycle is considered complete, and the history is reset)
        history.clear()
        with open(history_file, 'w') as f:
            json.dump(history, f)
        available_posts = posts
    # 重複していない投稿の中からランダムに1つ選ぶ (Randomly select one of the non-duplicate submissions.)
    return random.choice(available_posts)

# X の文字数制限を考慮してテキストを切り詰める (Truncate text considering the character limit of X)
def truncate_text(text, limit):
    if limit > 0 and len(text) > limit:
        return text[:limit-3] + "..."
    return text

# Xに投稿
def post_to_x(post_text):
    try:
        client = tweepy.Client(
            consumer_key=api_key, 
            consumer_secret=api_secret,
            access_token=access_token, 
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )
        client.create_tweet(text=post_text)
    except tweepy.errors.TweepyException as e:
        print(f"Error posting to X: {e}")

# メインの処理 (Main function)
def main():
    # 環境変数の検証 (Validate environment variables)
    validate_env_vars()

    # 投稿データを取得 (Get post data)
    posts = get_posts()
    if not posts:
        print("No posts data.")
        return
    
    # 投稿履歴を取得 (Get posting history)
    history = get_post_history()
    
    # 投稿を選択し、投稿用テキストを作成 (Select a post and create post text)
    selected_post = select_post(posts, history)
    post_text = truncate_text(selected_post['text'], CHARACTER_LIMIT)
    
    # Xに投稿 (Post to X)
    post_to_x(post_text)

    # 投稿履歴を更新 (Update posting history JSON file)
    update_post_history(hashlib.md5(selected_post['text'].encode()).hexdigest())

if __name__ == "__main__":
    main()
