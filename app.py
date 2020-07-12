import os
from flask import Flask, render_template, request
from config import Config
from model import HSD_PretrainedModel
from utils import *
import pandas as pd


app = Flask(__name__)
cls = HSD_PretrainedModel(Config)


@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.DataFrame()
    if request.method == "POST":
        # get url that the person has entered
        url = request.form['input_text']
        set_start_url(url)
        run_spider()
#         df = pd.read_json('out.json').loc[1:]
        df = predict_posts(cls)
           
    return render_template('index.html', tables=[df.to_html(classes='data', escape=False)], titles=df.columns.values)


if __name__ == '__main__':
    app.run()
