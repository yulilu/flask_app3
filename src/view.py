# coding: utf-8

from flask import Flask, render_template

from transformers import BertJapaneseTokenizer, BertModel
from sentence_transformers import SentenceTransformer
from sentence_transformers import models
from scipy.special import eval_sh_legendre
import torch
import numpy as np
import pandas as pd


app = Flask(__name__)


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


@app.route('/')
def index():
    MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
    tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)

    #df = pd.read_csv('src\\chatbot.csv',header=0,names=['No','Category', 'Title', 'question', 'answer'])
    df = pd.read_csv('chatbot.csv',header=0,names=['No','Category', 'Title', 'question', 'answer'])
    sentences = []
    answers = []
    for row in df.itertuples():
        sentences.append(row[4])
        answers.append(row[5])

    input_sentence="PulseSecureが開かないこととMerQNetが開かない"
    scores = calc_similarity(model, tokenizer, sentences, input_sentence)


    return render_template('index.html')


if __name__ == '__main__':
    app.run()
