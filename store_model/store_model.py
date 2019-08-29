'''module to store model'''
from sklearn.externals import joblib
from ml_model.ml_file_model import FileMLModel
import logging
from utils.utils import Utils
import os

logger = Utils().user_path()
logging.basicConfig(filename=logger, level=logging.DEBUG)


class StoreModel:
    '''class for storing model'''

    def __init__(self):
        pass

    @classmethod
    def storeData(cls):
        '''initializing data to be stored in db '''
        model = FileMLModel()
        data_frame = model.model_init()
        t = model.data_split(data_frame)
        model.train_model(t[0], t[2])
        print("storing the model ", os.getpid())
        joblib.dump(model, 'model.joblib')
        logging.debug("storing the model ")

    @classmethod
    def loadData(cls):
        '''method for loading data'''
        print('loading the model')
        model = joblib.load('model.joblib')
        logging.debug("loading the model")
        return model
