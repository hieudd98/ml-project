import os
from flask import Flask, render_template, request
from config import Config
from model import HSD_PretrainedModel


app = Flask(__name__)
model = HSD_PretrainedModel(Config)


@app.route('/', methods=['GET', 'POST'])
def index():
    text = []
    if request.method == "POST":
        # get url that the person has entered
        try:
            line = request.form['input_text']
            if line:
                text = [line, model.predict(line)]
        except:
            text.append(
                "Please make sure text is valid and try again."
            )
            return render_template('index.html', text=text)
    return render_template('index.html', text=text)


if __name__ == '__main__':
    app.run()
