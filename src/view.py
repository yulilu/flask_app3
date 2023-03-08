# coding: utf-8

import slack
from flask import Flask, render_template, make_response, jsonify, request, Response
import requests
import json
from slackeventsapi import SlackEventAdapter
SLACK_SIGNING_SECRET = '6f1a03ac213789637ea8b8169c998487'
SLACK_BOT_TOKEN = 'xoxb-3967341434739-4908753847316-hGvmqsRA7VTd3seUuGbHzq0E'

import logging
logging.basicConfig(
    level=logging.DEBUG, # ログの出力レベルを指定します。DEBUG, INFO, WARNING, ERROR, CRITICALから選択できます。
    format='%(asctime)s %(levelname)s %(message)s', # ログのフォーマットを指定します。
    datefmt='%Y-%m-%d %H:%M:%S' # ログの日付時刻フォーマットを指定します。
)

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

# トークンを指定してWebClientのインスタンスを生成
client = slack.WebClient(token=SLACK_BOT_TOKEN)
# ボットのユーザーIDを取得
BOT_USER_ID = client.api_call("auth.test")['user_id']

slack_event_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET,'/slack/events',app)

@slack_event_adapter.on('message')
def respond_message(payload):
    logging.debug('☆start')
    # payloadの中の'event'に関する情報を取得し、もし空なら空のディクショナリ{}をあてがう
    event = payload.get('event', {})
    # 投稿のチャンネルID、ユーザーID、投稿内容を取得
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
 
    # もしボット以外の人からの投稿だった場合
    if BOT_USER_ID != user_id:               
        # chat_postMessageメソッドでオウム返しを実行
        client.chat_postMessage(channel=channel_id, text=text)
 

if __name__ == '__main__':
    app.run(debug=True)