# coding: utf-8

#　必要なモジュールのインポート
from flask import Flask, render_template, make_response, jsonify, request, Response
import requests
import json

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    # for challenge of slack api
    if 'challenge' in data:
        token = str(data['challenge'])
        return Response(token, mimetype='text/plane')
    # for events which you added
    if 'event' in data:
        print("get event")
        event = data['event']
        if 'user' in event:
            print("user = ", event["user"])
        if "text" in event:
            print("text = ", event["text"])
    return Response("nothing", mimetype='text/plane')
    '''
    json =  request.json
    print(json)
    d = {'challenge' : json["challenge"]}
    return jsonify(d)
    '''
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
    '''

if __name__ == '__main__':
    app.run(debug=True)