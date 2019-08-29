from web_git_prediction.app import app
from web_git_prediction.config import HOST, PORT, DEBUG, USE_RELOADER
from store_model.store_model import StoreModel
from apscheduler.schedulers.background import BackgroundScheduler
import multiple_process
from fetching_file_data.helper import Helper
from fetching_file_data.fetching_file_data import Fetch_file
from ml_model import ml_filelevel_model


def runner():
    app.run(host=HOST,port=PORT, debug=DEBUG, use_reloader=False)


if __name__ == '__main__':
    SCHED = BackgroundScheduler(daemon=True)
    #  change this 23 hours
    SCHED.add_job(multiple_process.scheduled_job, 'interval', seconds=6, coalesce=True)
    StoreModel.storeData()
    SCHED.start()
    StoreModel.storeData()
    fetch_obj = Fetch_file()
    helper_obj = Helper()
    # critical_dict = helper_obj.data_output(fetch_obj)
    MODEL = ml_filelevel_model.FileMLModel()
    DATA_FRAME = MODEL.model_init()
    X_TRAIN = DATA_FRAME.iloc[:, :-1]
    Y_TRAIN = DATA_FRAME.iloc[:, -1]
    MODEL.train_model(X_TRAIN, Y_TRAIN)
    app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)
