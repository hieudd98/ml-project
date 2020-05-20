import torch
from fastai import *
from fastai.text import *
import pandas as pd


class HSD_PretrainedModel():
    def __init__(self, Config):
        # config
        self.thres = Config.threshold
        self.bs = Config.bs
        model_path = Path(Config.model_path)
        data_path = Path(Config.data_path)
        
        self.data_clas = self.load_data(data_path)
        self.model = (text_classifier_learner(self.data_clas, AWD_LSTM, pretrained=False)
                        .load(model_path, with_opt=False))
        
        
    def load_data(self, data_path):
        X_train = pd.read_csv(data_path/'02_train_text.csv')
        y_train = pd.read_csv(data_path/'03_train_label.csv')
        X_test = pd.read_csv(data_path/'04_test_text.csv')
        
        df = pd.concat([X_train, X_test], sort=False)
        train_df = pd.merge(X_train, y_train, on='id')

        data_lm = (TextList.from_df(df, cols='free_text')
                      .split_by_rand_pct(0.1, seed=42)
                      .label_for_lm()
                      .databunch(bs=self.bs, num_workers=1))
        return (TextList.from_df(train_df, vocab = data_lm.vocab, cols='free_text')
                        .split_by_rand_pct(0.3, seed=42)
                        .label_from_df(cols='label_id')
                        .databunch(bs=self.bs, num_workers=1))
    
    def predict(self, text):
        res = self.model.predict(text)[2].cpu().numpy()
        if res[2] > self.thres:
            return f'Hate speech detected! {res}'
        elif res[1] > self.thres:
            return f'Offensive language {res}'
        else: return f'Clean {res}'