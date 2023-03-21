# coding: utf-8

import os
import requests
import json

import slack
from flask import Flask, render_template, make_response, jsonify, request, Response
from slackeventsapi import SlackEventAdapter

from transformers import BertJapaneseTokenizer, BertModel
from sentence_transformers import SentenceTransformer
from sentence_transformers import models
from scipy.special import eval_sh_legendre
import torch
import numpy as np
import pandas as pd


SLACK_SIGNING_SECRET = '6f1a03ac213789637ea8b8169c998487'
SLACK_BOT_TOKEN = ''
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')


import logging
logging.basicConfig(
    level=logging.DEBUG, # ログの出力レベルを指定します。DEBUG, INFO, WARNING, ERROR, CRITICALから選択できます。
    format='%(asctime)s %(levelname)s %(message)s', # ログのフォーマットを指定します。
    datefmt='%Y-%m-%d %H:%M:%S' # ログの日付時刻フォーマットを指定します。
)


app = Flask(__name__)


client = slack.WebClient(token=SLACK_BOT_TOKEN)
BOT_USER_ID = client.api_call("auth.test")['user_id']
slack_event_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET,'/',app)


def sentence_to_vector(model, tokenizer, sentence):
    tokens = tokenizer(sentence)["input_ids"]
    input = torch.tensor(tokens).reshape(1,-1)
    with torch.no_grad():
        outputs = model(input, output_hidden_states=True)
        last_hidden_state = outputs.last_hidden_state[0]
        averaged_hidden_state = last_hidden_state.sum(dim=0) / len(last_hidden_state) 
    return averaged_hidden_state

def calc_similarity(model, tokenizer, sentences, sentence2):
    sentence_vector2 = sentence_to_vector(model, tokenizer, sentence2)
    scores = []
    for sentence in sentences:
            sentence_vector1 = sentence_to_vector(model, tokenizer, sentence)
            scores.append(torch.nn.functional.cosine_similarity(sentence_vector1, sentence_vector2, dim=0).detach().numpy().copy())
    return scores


@slack_event_adapter.on('message')
def respond_message(payload):
    logging.debug('☆start')
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

 
    MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
    tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)

    logging.debug('☆ checkpoint-1')
    #df = pd.read_csv('src\\chatbot.csv',header=0,names=['No','Category', 'Title', 'question', 'answer'])
    df = pd.read_csv('chatbot.csv',header=0,names=['No','Category', 'Title', 'question', 'answer'])
    sentences = []
    answers = []
    for row in df.itertuples():
        sentences.append(row[4])
        answers.append(row[5])

    input_sentence="PulseSecureが開かないこととMerQNetが開かない"
    logging.debug('☆ checkpoint-2')
    scores = calc_similarity(model, tokenizer, sentences, input_sentence)
    logging.debug('☆ checkpoint-3')


    if BOT_USER_ID != user_id:               
        client.chat_postMessage(channel=channel_id, text=text)
 

if __name__ == '__main__':
    app.run(debug=True)
