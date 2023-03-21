# coding: utf-8

import time
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)

def webscr(keywords):
    INTERVAL = "2"
    INTERVAL=int(INTERVAL)
    pages_num = 10 + 1
    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={keywords}'
    req = requests.get(url)
    time.sleep(INTERVAL)
    logging.debug('req.text='+str(req.text))
    soup = BeautifulSoup(req.text, "html.parser")
    logging.debug('soup='+str(soup))
    search_site_list = soup.select('div.kCrYT > a')
    logging.debug('search_site_list='+str(search_site_list))
    
    titles = []
    for rank, site in zip(range(1, pages_num), search_site_list):
        try:
            site_title = site.select('h3.zBAuLc')[0].text
            titles.append(site_title)
        except IndexError:
            site_title = site.select('img')[0]['alt']
        site_url = site['href'].replace('/url?q=', '')
    return titles


@app.route('/', methods = ['GET', 'POST'])
def input():
    search_key = 'TOEIC'
    title_sum = webscr(keywords=search_key)
    logging.debug('title_sum='+str(title_sum))
    title_ = 'ようこそ'
    message_ = 'MTVデザインパターンでWebアプリ作成'
    return render_template('index.html', title=title_, message=message_)

if __name__ == '__main__':
    app.run()