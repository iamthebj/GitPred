import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn import metrics


class FileMLModel:
    classifier = LinearSVC()
    count_vect = None
    def __init__(self):
        pass
    def model_init(self):
        path=r"C:/Users/biswajit_nath/Desktop/text_gitpredictions/filelevelgithub.csv"
        df = pd.read_csv(path)
        df = df[pd.notnull(df['criticality'])]
        df1 = df["filename"]
        df2 = df["criticality"]
        df2_list1 = df2.tolist()
        list1 = df1.tolist()
        df1_list2 = [i.split(".")[-1] for i in list1]
        df_file = pd.DataFrame({"extension_name":df1_list2,"criticality":df2_list1})
        df_file['category_id'] = df_file['criticality'].factorize()[0]
        return (df_file)

    def data_split(self, data_frame):
        X_train, X_test, y_train, y_test = train_test_split(data_frame['extension_name'],
        data_frame['criticality'], random_state = 0,test_size=0.2)
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        self.tfidf_transformer = TfidfTransformer()
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)
        return (X_train_tfidf, X_test, y_train, y_test)
    
    def train_model(self, X_train_tfidf, y_train):
       self.classifier = self.classifier.fit(X_train_tfidf, y_train)
       return self.classifier


    def test_model(self, X_test):
        y_pred = self.classifier.predict(self.count_vect.transform(X_test))
        print(y_pred)
        return y_pred
        
        
    def test_accuracy(self, y_test, y_pred):
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print(' Accuracy: {}'.format(metrics.accuracy_score(y_test, y_pred)))
        return accuracy
