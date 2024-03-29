from flatten_json import flatten
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from xgboost import plot_importance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sklearn.metrics
from matplotlib import pyplot as py
from sklearn.model_selection import train_test_split
import sklearn
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
data = []
new_data = []
count_0 = 0
count_1 = 0
with open("data") as f:
   for line in f:
       data.append(json.loads(line))
for i in range(len(data)):
   del data[i]['sha256']
   del data[i]['histogram'] 
   del data[i]['byteentropy']
   del data[i]['strings']['printabledist']
   del data[i]['exports']
   del data[i]['header']['coff']['characteristics']
   del data[i]['header']['optional']['dll_characteristics']
   del data[i]['imports']
   del data[i]['appeared']
   for j in range(len(data[i]['section']['sections'])):
      del data[i]['section']['sections'][j]['props']   
for i in range(70000):
    if(data[i]['label'] != -1):
      new_data.append(data[i])
    if(data[i]['label'] == 0): #counting benign samples
      count_0 += 1
    if(data[i]['label'] == 1): #counting malicious samples
      count_1 += 1
#To plot a pie chart of sample distribution
counts = [count_0, count_1]
labels = ['Benign', 'Malicious']
explode = [0, 0.1]
colors = ['lightgreen','lightblue']
plt.pie(counts,labels = labels, explode=explode,shadow='True',colors = colors, startangle = 90,autopct='%.1f%%')
plt.axis('equal')
plt.text(0.5,1.25, family="serif")
plt.show()
#De-nesting json data
flattened_json = (flatten(d) for d in new_data)
df1 = pd.DataFrame(flattened_json)#initial dataframe
features_label = np.array(df1.label)
df1 = df1.drop('label',axis =1)
#dealing with categorical variables
df1 = pd.get_dummies(df1) #get dummies for categorical variables
feature_list = df1.columns
df1 = df1.fillna(0) #filling missing values with 0 for now
train_features, test_features, train_labels, test_labels = train_test_split(df1, features_label, test_size = 0.25, random_state = 42)# splitting data into train set and test set
#Bernoulli's Naive Bayes Model
model = BernoulliNB(alpha = 0.1, binarize = 0.8, fit_prior = True)
model.fit(train_features,train_labels)      
preds = model.predict(test_features)
probpredBNB = model.predict_proba(test_features)[:, 1]
print("Accuracy for model : %.2f" % (accuracy_score(test_labels, preds) * 100))
#Logistic Regression Model
model3 = LogisticRegression()
model3.fit(train_features,train_labels)      
predsLR = model3.predict(test_features)
probpredLR = model3.predict_proba(test_features)[:, 1]
print("Accuracy for model : %.2f" % (accuracy_score(test_labels, predsLR) * 100))
#AdaBoost Model
model4 = AdaBoostClassifier()
model4.fit(train_features,train_labels)
predsAda = model4.predict(test_features)
probpredAda = model4.predict_proba(test_features)[:, 1]
print("Accuracy for model : %.2f" % (accuracy_score(test_labels, predsAda) * 100))
#Random Forest Model
model5 = RandomForestClassifier(n_estimators = 500,bootstrap = True)
model5.fit(train_features,train_labels)      
probpredRF = model5.predict_proba(test_features)[:, 1]
predsRF = model5.predict(test_features)
y_scoreRF = model5.score(test_features,test_labels)
pri = model5.predict_proba(test_features)
print("Accuracy for model : %.2f" % (accuracy_score(test_labels, predsRF) * 100))
#XGBoost Model
model6 = XGBClassifier()
model6.fit(train_features,train_labels)      
predsXG = model6.predict(test_features)
probpredXGB = model6.predict_proba(test_features)[:, 1]
print("Accuracy for model : %.2f" % (accuracy_score(test_labels, predsXG) * 100))
#Plotting the area under the reciever operating characteristics curve
tn,fp,fn,tp = metrics.confusion_matrix(test_labels, predsRF).ravel()
tp2 = tp / (tp + fn)
fp2 = fp / (fp + tn)
fpr, tpr, thresholds = roc_curve(test_labels, probpredBNB)
roc_auc = auc(fpr, tpr)
fpr2,tpr2,thresholds2 = roc_curve(test_labels, probpredAda)
roc_auc2 = auc(fpr2,tpr2)
fpr4,tpr4,thresholds4 = roc_curve(test_labels, probpredLR)
roc_auc4 = auc(fpr4,tpr4)
fpr5,tpr5,thresholds5 = roc_curve(test_labels, probpredRF )
roc_auc5 = auc(fpr5,tpr5)
fpr6,tpr6,thresholds6 = roc_curve(test_labels, probpredXGB)
roc_auc6 = auc(fpr6,tpr6)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=1, label='Naive Bayes' % roc_auc)
#plt.plot(fpr1, tpr1, color='darkred', lw=1, label='MNB curve (area = %0.2f)' % roc_auc1)
plt.plot(fpr2, tpr2, color='darkgreen', lw=1, label='Adaptive Boost ' % roc_auc2)
#plt.plot(fpr3, tpr3, color='pink', lw=1, label='GNB curve (area = %0.2f)' % roc_auc3)
plt.plot(fpr4, tpr4, color='blue', lw=1, label='Logistic Regression' % roc_auc4)
plt.plot(fpr5, tpr5, color='darkviolet', lw=1, label='Our Model (area = %0.6f)' % roc_auc5)
plt.plot(fpr6, tpr6, color='black', lw=1, label='eXtreme Gradient Boosting' % roc_auc6)
plt.plot([0, 1], [0, 1], color='navy', lw=3, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.10])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves')
plt.legend(loc="lower right")
plt.show()
# To save as a pickle file
saved_model = pickle.dumps(model5) 
filename = '/content/drive/My Drive/Colab Notebooks/test.pickle' 
outfile = open(filename,'wb')
pickle.dump(saved_model,outfile)
outfile.close()
