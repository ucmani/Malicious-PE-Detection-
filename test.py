# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#importing libraries
#import ijson
#import jsonlines
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#json extraction
filename = "train_features_0.jsonl"
data = []
#new_data = []
with open(filename) as f:
    for line in f:
       data.append(json.loads(line))
for i in range(len(data)):
  data[i]['histogram'] = None
  data[i]['byteentropy'] = None
  data[i]['strings'] = None
print(data[1])
#df_2 = pd.DataFrame(data='df' , columns = 'True')

#print(df[1])
#with open(filename) as f:
#    dict_train = json.loads(f)
#train = pd.dataFrame.from_dict(dict_train, orient = 'index')
#train.reset_index(level = 0,implace = 'True')
