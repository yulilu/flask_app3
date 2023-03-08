# coding: utf-8

#　必要なモジュールのインポート
from flask import Flask, render_template, make_response

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

# --- View側の設定 ---
# ルートディレクトリにアクセスした場合の挙動
@app.route('/', methods=['GET', 'POST'])
# def以下がアクセス後の操作
def index():
    #return '3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P'
    #return render_template('index.html') #追加
    response = make_response('3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P')
    response.headers['Content-type'] = 'text/plain'
    return response

if __name__ == '__main__':
    app.run()