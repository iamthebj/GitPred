'''module for training ml model'''
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.exceptions import NotFittedError
import labels
from utils.utils import Utils
class MLModel:
    '''class for ML model'''
    config = Utils().get_config_file('config.ini')
    file_name = config.get('file', 'csv_file_name', raw=True)
    classifier = SVC()
    scaler = StandardScaler()
    def __init__(self):
        pass
    def model_init(self):
        '''method for removing unnecessary data'''
        data_frame = pd.read_csv(self.file_name)
        threshold = 2.628e+6
        data_frame_open = data_frame[data_frame["state"] == 'Open']
        for i in data_frame_open.index:
            open_pr_time = data_frame.loc[i, 'open_pr_time']
            if open_pr_time > threshold:
                data_frame.loc[i, 'state'] = 'Rejected'
        data_frame = data_frame.drop(data_frame[data_frame["state"] == 'Open'].index)
        data_frame['state'] = data_frame['state'].map({'Accepted':0, 'Rejected':1})
        data_frame = data_frame.drop("repository_name", 1)
        data_frame = data_frame.drop("pull_numbers", 1)
        data_frame = data_frame.drop("pull_request_acceptance_rate", 1)
        data_frame = data_frame.drop("open_pr_time", 1)
        data_frame = data_frame.drop("contributor_acceptance_rate", 1)
        data_frame = data_frame.drop("changes", 1)
        data_frame = data_frame.sample(frac=1)
        data_frame = data_frame.dropna()
        data_frame['state'].map({'Accepted':0, 'Rejected':1})
        return data_frame

    def data_split(self, data_frame):
        '''method for spliting data'''
        X = data_frame.iloc[:, :-1]
        y = data_frame.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.scaler.fit(X_train)
        X_train = self.scaler.transform(X_train)
        return (X_train, X_test, y_train, y_test)

    def train_model(self, classifier, X_train, y_train):
        ''' method for training model'''
        classifier.fit_transform(X_train, y_train)
        return classifier

    def test_model(self, X_test):
        '''method for testing model'''
        try:
            self.scaler.fit(X_test)
            X_S_test = self.scaler.transform(X_test)
            print(X_S_test)
            y_pred = MLModel.classifier.predict(X_S_test)
            return y_pred
        except NotFittedError as e:
            print(repr(e))

    def test_accuracy(self, y_test, y_pred):
        '''method for testing accuracy'''
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print(' Accuracy: {}'.format(metrics.accuracy_score(y_test, y_pred)))
        return accuracy
