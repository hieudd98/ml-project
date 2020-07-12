import os
import pandas as pd


def set_start_url(url):
    with open('scraper-draft.py', 'r') as inFile, open('scraper.py', 'w') as outFile:
        lines = inFile.readlines()
        for idx, line in enumerate(lines):
            if idx != 5:
                outFile.write(line)
            else:
                line = line[:-2] + f"'{url}'" + line[-2:]
                outFile.write(line)

                
def run_spider(out_file='out.json'):
    if os.path.exists(out_file):
        os.remove(out_file)
    try:
        os.system(f'scrapy runspider -o {out_file} scraper.py')
    except:
        pass
    
    
def predict_posts(cls, file='out.json'):
    df = pd.read_json(file)
    cnt = 0
    
    out_df = pd.DataFrame(columns=['User', 'Post URL', 'Content', 'Is hate speech?', 'Ignore User'])
    for idx in range(1, df.shape[0]):
        line = df.iloc[idx]
        y_pred = cls.predict(line.text)[1].cpu().numpy()
        if y_pred != 0:
            if y_pred == 1:
                pred_text = 'Offensive Language'
            else: # y_pred == 2
                pred_text = 'Hate speech'
            
            out_df.loc[cnt] = [line.user, line.link, line.text, pred_text, line.ignore]
            cnt += 1
    
    return out_df