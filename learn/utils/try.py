headers=['date','close', 'volume', 'turnover', 'day_diff', 'MA_15', 'MA_30', 'MA_60',
       'MA_90', 'MA_120', 'Vol_15', 'Vol_30', 'Vol_60', 'Vol_90', 'Vol_120',
       'Day_diff_15', 'Day_diff_30', 'Day_diff_60', 'Day_diff_90',
       'Day_diff_120', 'turnover_15', 'turnover_30', 'turnover_60',
       'turnover_90', 'turnover_120', 'macd', 'macd_15', 'macd_30', 'macd_60',
       'macd_90', 'macd_120' , 'code' , 'target']
import numpy as np
import pandas as pd
train=pd.read_csv(r'data.csv',names=headers)
needDelete=['date','close', 'volume', 'turnover', 'day_diff' , 'code']
train.drop(needDelete,axis=1,inplace=True)
train.replace([np.inf, -np.inf], np.nan,inplace=True)
train.fillna(1,inplace=True)
target=train.target

diff=['Vol_15','Vol_30','Vol_60','Vol_90','Vol_120','turnover_15','turnover_30','turnover_60','turnover_90','turnover_120','macd','macd_15','macd_30','macd_60','macd_90','macd_120']

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, log_loss
import sklearn
train_test_split=sklearn.cross_validation.train_test_split
X_train, X_test, y_train, y_test = train_test_split(data,target,test_size=0.4,random_state=0)
clf=GradientBoostingClassifier()
clf.fit(X_train, y_train)
train_predictions = clf.predict(X_test)
acc = accuracy_score(y_test, train_predictions)
