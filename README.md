# python-json-to-x-auto-post

外部 URL に設置した投稿データ用の JSON ファイルから投稿内容を取得し、X （Twitter） API v2 を使用して、X に投稿する Python スクリプトです。

GitHub Actions を使用することで、定期的にスクリプトを実行し、決められたタイミングで自動投稿していくことができます。

投稿用の JSON データからランダムに1件を取得して投稿します。JSON データ内の各投稿が1回ずつ投稿されるまでは同じ投稿が重複しないようにしてあります。

## 投稿用データの準備

`entry_data_sample.json` のフォーマットを参考に投稿用データを入れた JSON データを作成し、外部からアクセス可能な URL に設置します。

GitHub リポジトリの設定からシークレット（Secret）設定画面に進み、`JSON_URL` の値として、設置した JSON データの URL を設定してください。

## X （Twitter） API 認証情報の取得と設定

X の API から、各種キー（`API Key`, `API secret key`, `Access token`, `Access token secret`, `Bearer token`）を取得し、それぞれ、GitHub リポジトリのシークレットとして下記のように設定します。

- `X_ACCESS_TOKEN` = `Access token`
- `X_ACCESS_TOKEN_SECRET` = `Access token secret`
- `X_API_KEY` = `API Key`
- `X_API_KEY_SECRET` = `API secret key`
- `X_BEARER_TOKEN` = `Bearer token`

## GitHub Actions の設定

`.github/workflows/auto_post.yml.sample` を `auto_post.yml` にリネームします。

```
on:
  schedule:
    - cron: '30 1 * * 1'
```

初期状態では、スケジュールが日本時間（`UTC+9`）における毎週、月曜日の 10:30 に実行されるようになっています。必要に応じて cron の設定を変更してください。

## 自動投稿

設定が正しく行われると、GitHub Actions が実行され、X に投稿されると同時に、投稿履歴管理用の JSON ファイル（`post_history.json`）が作成、更新されてリポジトリにコミットされます。

# python-json-to-x-auto-post

This Python script retrieves post content from a JSON file hosted at an external URL and posts it to X (Twitter) using the X API v2.

By utilizing GitHub Actions, you can schedule the script to run periodically and automatically post content at specified times.

The script randomly selects one post from the JSON data and ensures that each post is published only once until all posts have been used.

## Preparing the Post Data

Create a JSON file containing the post data, using the format provided in `entry_data_sample.json` as a reference. Host this JSON file at a publicly accessible URL.

In your GitHub repository settings, navigate to the Secrets section and add the URL of the JSON data as a secret with the name `JSON_URL`.

## Obtaining and Configuring X (Twitter) API Credentials

Obtain the necessary API keys (`API Key`, `API Secret Key`, `Access Token`, `Access Token Secret`, `Bearer Token`) from X. Then, add these keys as secrets in your GitHub repository settings as follows:

- `X_ACCESS_TOKEN` = `Access Token`
- `X_ACCESS_TOKEN_SECRET` = `Access Token Secret`
- `X_API_KEY` = `API Key`
- `X_API_KEY_SECRET` = `API Secret Key`
- `X_BEARER_TOKEN` = `Bearer Token`

## Setting Up GitHub Actions

Rename `.github/workflows/auto_post.yml.sample` to `auto_post.yml`.

```
on:
  schedule:
    - cron: '30 1 * * 1'
```

By default, the schedule is set to run every Monday at 10:30 AM JST (`UTC+9`). Adjust the cron settings as needed to fit your desired schedule.

## Automatic Posting

Once the setup is complete, GitHub Actions will execute the script, post to X, and simultaneously create or update a JSON file (`post_history.json`) that manages the posting history. This file will be committed to the repository.
