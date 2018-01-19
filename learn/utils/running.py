import numpy as np
import pandas as pd

cols=['code', 'boll_diff', 'volDiff', 'volBreak', 'boll_gradient', 'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient', 'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient', 'change', 'type']
data=pd.read_csv('cookie.csv',names=cols)
train=data.dropna()
feature=['boll_diff', 'volDiff', 'volBreak', 'boll_gradient', 'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient', 'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient']
x=['code', 'boll_diff', 'volDiff', 'volBreak', 'boll_gradient',
       'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient',
       'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient',
       'change']
X=train[x]
Y=train.type
import sklearn
import sklearn.cross_validation
x=x[:-1]
x_train,x_test,y_train,y_test=sklearn.cross_validation.train_test_split(train[x],train.type,test_size=0.3)
from sklearn.ensemble import ExtraTreesClassifier
clf3=ExtraTreesClassifier(n_estimators=200,max_features='auto',n_jobs=2,verbose=3)
clf3.fit(x_train,y_train)

cols=['code', 'boll_diff', 'volDiff', 'volBreak', 'boll_gradient', 'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient', 'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient', 'change', 'type']
data=pd.read_csv('today.csv',names=cols)
x=['code', 'boll_diff', 'volDiff', 'volBreak', 'boll_gradient',
       'bollBreak', 'lineBreak', 'mean15_gradient', 'mean30_gradient',
       'gradientBreak', 'rate60', 'rate90', 'lineDiff', 'dea', 'dea_gradient']
test=data[x]
t=test.dropna()
m=clf3.predict(t)
t['type']=m
s=t[t.type>1]

j=test[test.volBreak]
q=j[j.bollBreak]
p=q[q.lineBreak]
