# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:53:41 2019

@author: VrainsHacker
"""

import pandas as pd #for handling .csv files
import numpy as np

customer_data =pd.read_csv("pingpong_data_p2.csv")
customer_data.head(10) # show first ten samples of data

x=customer_data.iloc[1:,1:5].values
y=customer_data.iloc[1:,5:6].values


from sklearn.svm import SVR
regressor=SVR(gamma=0.005,C=20,epsilon=0.3)  
#gamma=0.01,C=25,epsilon=0.2 -->poor
#gamma=0.00075,C=15,epsilon=0.4
#gamma=0.001,C=20,epsilon=0.3      #gamma=0.0005,C=10,epsilon=0.5
regressor.fit(x,y)

y_predict=regressor.predict(x)
from sklearn.metrics import mean_squared_error
MSE=mean_squared_error(y,y_predict)
RMSE=np.sqrt(MSE)
print("MSE: %f " % MSE)
print("RMSE: %f " % RMSE)


#%% train your model here
#from xxx import ooo_model

#ooo=ooo_model()

#ooo.fit(x_train,y_train)
#neigh.fit(x_train,y_train)

#ooo.predict(x_test)

# check the acc to see how well you've trained the model
#acc=?




#import matplotlib.pyplot as plt
#plt.figure()
#plt.scatter(x[:,0,np.newaxis],y[:,np.newaxis],s=20,marker='o')
#plt.scatter(x[:,0,np.newaxis],y_predict[:,np.newaxis],s=30,marker='x')
#plt.title('RMSE= %f.2' % (RMSE))



#%% save model
import pickle

#filename="ooo_example0401.sav"
filename="pingpong_model_p2_svm_ver3.sav"
pickle.dump(regressor, open(filename, 'wb'))




## load model
#l_model=pickle.load(open(filename,'rb'))
#yp_l=l_model.predict(x_test)
#print("acc load: %f " % accuracy_score(yp_l, y_test))
    