"""
SPLITTING TRAINING AND TESTING
"""
import os
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
from utils.utils import Utils

class FileMLModel:
    """
    class for all model - DECISION TREE
    """
    decision_tree = tree.DecisionTreeClassifier(criterion='entropy',
                                                max_depth=3,
                                                random_state=0)

    def __init__(self):
        """
        no need
        """



    def model_init(self):
        """
        :return:
        """

        df_git_file = pd.read_csv('C:/Users/biswajit_nath/Desktop/text_gitpredictions/filelevelgithub.csv')
        df_git_file = df_git_file[pd.notnull(df_git_file['criticality'])]
        df_git_file[['commit_criticality']] = \
            df_git_file[['commit_criticality']].fillna(value='non critical')
        df_git_file['criticality'] = \
            df_git_file['criticality'] + ' ' + df_git_file['commit_criticality']
        df_file_name = df_git_file["filename"]
        df_critical = df_git_file["criticality"]
        df_per_change = df_git_file['perc_change_files']
        df_cyclomatic = df_git_file['cy_comp']
        df2_list1 = df_critical.tolist()
        list1 = df_file_name.tolist()
        list3 = df_per_change.tolist()
        list4 = df_cyclomatic.tolist()
        df1_list2 = [i.split(".")[-1] for i in list1]
        df_file = pd.DataFrame({"extension_name": df1_list2, 'perc_change_files': list3,
                                'cy_comp': list4, "criticality": df2_list1})
        df_file = df_file[['extension_name', 'perc_change_files', 'cy_comp', 'criticality']]
        df_file.to_csv('xyz.csv')
        df_file = self.data_transform(df_file)
        df_file.to_csv('abc.csv')
        return df_file

    @staticmethod
    def data_split(data_csv):
        """ method for splitting data"""
        x_data = data_csv.iloc[:, :-1]
        y_data = data_csv.iloc[:, -1]
        # 80:20 split for train: test
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1,
                                                            random_state=0)
        return x_train, x_test, y_train, y_test

    @staticmethod
    def data_transform(df_file):
        config = Utils().get_config_file('config.ini')
        programming_extension = config.get("extension_list", "programming_extension").split(',')
        config_extension = config.get("extension_list", "config_extension").split(',')
        text_file = config.get("extension_list", "text_file").split(',')
        programming_extension = list(map(lambda s: s.strip(), programming_extension))
        config_extension = list(map(lambda s: s.strip(), config_extension))
        text_file = list(map(lambda s: s.strip(), text_file))
        df_file.loc[~df_file['extension_name'].isin(programming_extension), 'extension_name'] = 0
        df_file.loc[df_file['extension_name'].isin(programming_extension), 'extension_name'] = 1
        df_file.loc[df_file['extension_name'].isin(config_extension), 'extension_name'] = 2
        df_file.loc[df_file['extension_name'].isin(text_file), 'extension_name'] = 3
        df_file.loc[df_file['perc_change_files'] >= 25, 'perc_change_files'] = 0
        df_file.loc[df_file['perc_change_files'] < 25, 'perc_change_files'] = 1
        return df_file

    def train_model(self, x_train, y_train):
        """training the model"""
        # train the decision tree
        self.decision_tree.fit(x_train, y_train)
        return self.decision_tree
    @staticmethod
    def test_model(x_test):
        """testing the model"""
        y_predicted = FileMLModel.decision_tree.predict(x_test)
        print(y_predicted)
        return y_predicted

    def test_accuracy(self, y_test, y_predicted):
        """return the accuracy of model"""
        count_misclassified = (y_test != y_predicted).sum()
        print("Predicted")
        print(y_predicted)
        print("Original")
        print(y_test)
        print('Misclassified samples: {}'.format(count_misclassified))
        accuracy = metrics.accuracy_score(y_test, y_predicted)
        print('Accuracy: {:.2f}'.format(accuracy))
        return accuracy
