"""
To train and test the model
"""
from ml_model import ml_file_model
if __name__ == '__main__':
    MODEL = ml_file_model.FileMLModel()
    DATA_FRAME = MODEL.model_init()
    TRAIN_TEST_DATA = MODEL.data_split(DATA_FRAME)
    MODEL.train_model(TRAIN_TEST_DATA[0], TRAIN_TEST_DATA[2])
    Y_PRED = MODEL.test_model(TRAIN_TEST_DATA[1])
    ACCURACY = MODEL.test_accuracy(TRAIN_TEST_DATA[3], Y_PRED)
