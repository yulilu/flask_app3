# coding: utf-8

import time
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

import logging
logging.basicConfig(
    level=logging.DEBUG, # ログの出力レベルを指定します。DEBUG, INFO, WARNING, ERROR, CRITICALから選択できます。
    format='%(asctime)s %(levelname)s %(message)s', # ログのフォーマットを指定します。
    datefmt='%Y-%m-%d %H:%M:%S' # ログの日付時刻フォーマットを指定します。
)

# appという変数名で Flask オブジェクトをインスタンス化
app = Flask(__name__)

# --- View側の設定 ---

def webscr(keywords):
    INTERVAL = "2"
    INTERVAL=int(INTERVAL)
    
    # 上位から何件までのサイトを抽出するか指定する
    pages_num = 10 + 1
    
    print(f'【検索ワード】{keywords}')
    
    # Googleから検索結果ページを取得する
    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={keywords}'
    req = requests.get(url)# 検索を実行
    
    time.sleep(INTERVAL)
    print("2秒待ちな") 
    
    # Googleのページ解析を行う
    soup = BeautifulSoup(req.text, "html.parser")
    search_site_list = soup.select('div.kCrYT > a')
    
    #検索結果の一覧を取得する
    titles = []
    #links = []
    
    #result = {
    #'タイトル': titles,
    #'URL': links
    #}
    
    # ページ解析と結果の出力
    for rank, site in zip(range(1, pages_num), search_site_list):
        try:
            site_title = site.select('h3.zBAuLc')[0].text
            titles.append(site_title)
            #links.append(site_url)
        except IndexError:
            site_title = site.select('img')[0]['alt']
        site_url = site['href'].replace('/url?q=', '')
        # 結果を出力する
        print(str(rank) + "位: " + site_title + ": " + site_url)
    
    return titles
    #return links
    #return result


@app.route('/', methods = ['GET', 'POST'])
def input():
    search_key = 'TOEIC'
    title_sum = webscr(keywords=search_key)
    logging.debug('title_sum='+str(title_sum))

#    return render_template('result.html', outputname=ai_title)
    # DBから以下の変数を読み込んできたと仮定
    title_ = 'ようこそ'
    message_ = 'MTVデザインパターンでWebアプリ作成'
    return render_template('index.html', title=title_, message=message_)


# メイン関数
if __name__ == '__main__':
    app.run()