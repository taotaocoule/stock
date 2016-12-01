import pandas as pd
import numpy as np
import get_clean as gc
import sklearn
from utils import classify_test as ct

a=gc.cleanData('600000')
col=np.append(a.columns,['code','target'])

def new_clean_data():
	data=pd.read_csv(r'data.csv',names=col)	
	return data

train=new_clean_data()
clean=train.copy()
clean.replace([np.inf, -np.inf], np.nan,inplace=True)
clean.dropna(inplace=True)


X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(clean[col[:-2]],clean.target,test_size=0.4, random_state=0)

ct.classify_test(X_train,y_train,X_test,y_test)