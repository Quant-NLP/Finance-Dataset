import numpy as np
import pandas as pd
import os
import json

import time
from datetime import datetime,timedelta
from sklearn import preprocessing
import sys

import warnings
warnings.filterwarnings('ignore')

tweetpath = 'dataset/tweet/preprocessed/'
pricepath = 'dataset/price/raw/'
resultspath = 'results/'

stockname = sys.argv[1]

def Gendf_stock(day, stockname):
    newstr = []
    
    path = tweetpath + stockname
    files= os.listdir(path)

    for file in files:
        if datetime.strptime(file, "%Y-%m-%d") == day:
            all_data = [json.loads(line) for line in open(path+"/"+file, 'r')]
            for each_dictionary in all_data:
                text = each_dictionary['text']
                newstr += text
                newstr += '\n'
            break    
                
    return [newstr]

price = pd.read_csv(pricepath + stockname + '.csv')

for i in range(len(price)):
    price['Date'][i] = price['Date'][i].replace('-', '')

price = price.dropna().reset_index(drop=True)

day = datetime(2014, 1, 1)
end = datetime(2016, 1, 1)

tw = pd.DataFrame()

while day < end:
    temptw = pd.DataFrame()
    temptw['content'] = Gendf_stock(day, stockname)
    temptw['Date'] = day.strftime("%Y%m%d")
    tw = pd.concat([tw, temptw]) 
    day = day + timedelta(days=1)

tw = tw.reset_index(drop = True)


tw['Text'] = 0

for i in range(len(tw)):
    tw_str = str()
    for char in tw['content'][i]:
        tw_str += char + ' '
    tw['Text'][i] = tw_str
    tw['Text'][i] = tw['Text'][i].replace('$', '')
    tw['Text'][i] = tw['Text'][i].replace('URL', '')
    tw['Text'][i] = tw['Text'][i].replace('rt', '')
    tw['Text'][i] = tw['Text'][i].replace('AT_USER', '')
    tw['Text'][i] = tw['Text'][i].replace('->', '')
    tw['Text'][i] = tw['Text'][i].replace('@', '')
    
df = pd.merge(tw, price, on = 'Date', how = 'left')
df = df.dropna().reset_index(drop=True)

df.to_csv(resultspath + stockname + '.csv', index = 0)
