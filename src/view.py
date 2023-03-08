# coding: utf-8

#　必要なモジュールのインポート
from flask import Flask, render_template, make_response, jsonify
import requests

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    '''
    json =  request.json
    print(json)
    d = {'challenge' : json["challenge"]}
    return jsonify(d)
    '''
    url = "https://slack.com/api/chat.postMessage"
    token = "xoxb-3967341434739-4908753847316-hGvmqsRA7VTd3seUuGbHzq0E"# tokenを入れてください

    header={
        "Authorization": "Bearer {}".format(token)
    }

    data  = {
        "channel" : "C04SXDS7N2W",# Conversation IDを入れてください
        "text" : "Hello World!"
        }

    res = requests.post(url, headers=header, json=data)

    resonse_json = res.json()
    print(resonse_json)

if __name__ == '__main__':
    app.run(debug=True)