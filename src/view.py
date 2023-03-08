# coding: utf-8

#　必要なモジュールのインポート
from flask import Flask, render_template, make_response, jsonify, request, Response
import requests
import json

import logging
logging.basicConfig(
    level=logging.DEBUG, # ログの出力レベルを指定します。DEBUG, INFO, WARNING, ERROR, CRITICALから選択できます。
    format='%(asctime)s %(levelname)s %(message)s', # ログのフォーマットを指定します。
    datefmt='%Y-%m-%d %H:%M:%S' # ログの日付時刻フォーマットを指定します。
)

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    #logging.debug('request.data=' + str(request.data))
    #logging.debug('request.get_data=' + str(request.get_data()))
    #print('request.data=' + str(request.data))
    #print('request.get_data=' + str(request.get_data()))
    
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