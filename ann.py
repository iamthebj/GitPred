import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('github.csv')
dataset = dataset.dropna()
threshold = 2.628e+6
data_frame_open = dataset[dataset["state"] == 'Open']
for i in data_frame_open.index:
    open_pr_time = dataset.loc[i, 'open_pr_time']
    if open_pr_time > threshold:
        dataset.loc[i, 'state'] = 'Rejected'
dataset = dataset[dataset['state']  != 'Open']
X = dataset.iloc[:,:-1]
y = dataset.iloc[:,-1]
X = X.drop('repository_name',1)
X = X.drop('pull_numbers',1)
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
print(y)
y = labelencoder.fit_transform(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

classifier = Sequential()
classifier.add(Dense(units=7, kernel_initializer='uniform', activation='relu', input_dim=12))
classifier.add(Dense(units=7, kernel_initializer='uniform', activation='relu'))
classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
classifier.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

classifier.fit(X_train, y_train, batch_size=10, epochs=500, class_weight={0:1., 1:1.})

y_pred = classifier.predict(X_test)
y_pred = (y_pred>0.53)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


