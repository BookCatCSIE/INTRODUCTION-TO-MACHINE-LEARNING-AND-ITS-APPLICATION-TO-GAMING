# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:53:41 2019

@author: VrainsHacker
"""

import pandas as pd #for handling .csv files
import numpy as np

customer_data =pd.read_csv("game_12367_all_data.csv")
customer_data.head(10) # show first ten samples of data

x=customer_data.iloc[:,1:3].values
y=customer_data.iloc[:,3:4].values


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

#%% train your model here
#from xxx import ooo_model
from sklearn.neighbors import KNeighborsClassifier
#ooo=ooo_model()
neigh = KNeighborsClassifier(n_neighbors=1)
#ooo.fit(x_train,y_train)
#neigh.fit(x_train,y_train)
neigh.fit(x,y)
#ooo.predict(x_test)
y_knn=neigh.predict(x)
# check the acc to see how well you've trained the model
#acc=?
from sklearn.metrics import accuracy_score
acc=accuracy_score(y_knn,y)


#%% save model
import pickle

#filename="ooo_example0401.sav"
filename="neigh_knn_game12367_0523.sav"
pickle.dump(neigh, open(filename, 'wb'))

# load model
l_model=pickle.load(open(filename,'rb'))
yp_l=l_model.predict(x_test)
print("acc load: %f " % accuracy_score(yp_l, y_test))
    