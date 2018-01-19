import pandas
import pandas as pd
import numpy as np
import sklearn
import sklearn.ensemble
model=sklearn.ensemble.GradientBoostingClassifier()
para={'loss':['deviance','exponential'],'learning_rate':[0.1,0.01,0.001],'n_estimators':[100,200,300,500,800],'max_depth':[3,4,5],'min_samples_split':[2,3,5,8],'max_features':['auto','log2']}
ftwo=sklearn.metrics.make_scorer(sklearn.metrics.fbeta_score,beta=0.5)
col=['open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
       'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover', 'code',
       'close_range', 'volume_range', 'close15', 'close_std15',
       'close_range15', 'close_range_std15', 'volume15', 'volume_std15',
       'volume_range15', 'volume_range_std15', 'close30', 'close_std30',
       'close_range30', 'close_range_std30', 'volume30', 'volume_std30',
       'volume_range30', 'volume_range_std30', 'close60', 'close_std60',
       'close_range60', 'close_range_std60', 'volume60', 'volume_std60',
       'volume_range60', 'volume_range_std60', 'close90', 'close_std90',
       'close_range90', 'close_range_std90', 'volume90', 'volume_std90',
       'volume_range90', 'volume_range_std90', 'close120', 'close_std120',
       'close_range120', 'close_range_std120', 'volume120', 'volume_std120',
       'volume_range120', 'volume_range_std120', 'std20', 'boll_up',
       'boll_down', 'boll_range', 'boll_range_p', 'boll_change',
       'boll_range_p20', 'macd', 'isOK_5', 'change_5', 'isOK_10', 'change_10',
       'isOK_15', 'change_15', 'isOK_30', 'change_30', 'rsi',
       'close_gradient5', 'close_gradient10', 'close_gradient15',
       'close_gradient30']
data=pd.read_csv('data.csv',names=col)
cols=['open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
       'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover', 'code',
       'close_range', 'volume_range', 'close15', 'close_std15',
       'close_range15', 'close_range_std15', 'volume15', 'volume_std15',
       'volume_range15', 'volume_range_std15', 'close30', 'close_std30',
       'close_range30', 'close_range_std30', 'volume30', 'volume_std30',
       'volume_range30', 'volume_range_std30', 'close60', 'close_std60',
       'close_range60', 'close_range_std60', 'volume60', 'volume_std60',
       'volume_range60', 'volume_range_std60', 'close90', 'close_std90',
       'close_range90', 'close_range_std90', 'volume90', 'volume_std90',
       'volume_range90', 'volume_range_std90', 'close120', 'close_std120',
       'close_range120', 'close_range_std120', 'volume120', 'volume_std120',
       'volume_range120', 'volume_range_std120', 'std20', 'boll_up',
       'boll_down', 'boll_range', 'boll_range_p', 'boll_change',
       'boll_range_p20', 'macd', 'rsi',
       'close_gradient5', 'close_gradient10', 'close_gradient15',
       'close_gradient30']

x_train,x_test,y_train,y_test=sklearn.cross_validation.train_test_split(data[cols],data.isOK_5,test_size=0.3)

grid=sklearn.grid_search.GridSearchCV(model,para,scoring=ftwo,n_jobs=8,cv=10)
