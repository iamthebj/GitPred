''' Module for multiprocessing'''
import time
import os
import shutil
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler
from run import runner, app
import concurrent.futures
import pandas as pd
from fetching_data.fetching_data import Fetch
from store_model.store_model import StoreModel
from utils.utils import Utils
import sys
import traceback
FUTURES_LIST = []
def pulls_train_extract(owner, repository):
    '''Method to call the extract pull data'''
    #print(time.asctime(time.localtime(time.time())), " ", ' inside Process', os.getpid())
    try:
        Fetch().json_to_csv_conversion(owner, repository)
    except:
        traceback.print_exc()
def create_process(owner, repository):
    """ Function for creating processes. """
    with concurrent.futures.ProcessPoolExecutor(max_workers = 4) as executor:
        for owner_name, repository_name in zip(owner, repository):
            FUTURES_LIST.append(executor.submit(pulls_train_extract, owner_name, repository_name))
        concurrent.futures.wait(FUTURES_LIST)
        print("all csv's are prepared")
        Fetch().csv_append()
        StoreModel().storeData()
        #print(FUTURES_LIST)
    
def scheduled_job():
    """ Function for creating processes. """
    global PROCESS_LIST
    PROCESS_LIST = []
    start = time.time()
    #print(time.asctime(time.localtime(time.time())), ' inside thread(scheduled)', os.getpid())
    config = Utils().get_config_file('config.ini')
    csv_path = config.get('path', 'csv_path')
    if not os.path.isdir(os.path.join(csv_path)):
        os.mkdir(csv_path)
    sub_folders = os.listdir(csv_path)
    for sub_folder in sub_folders:
        shutil.rmtree('./git_csv/'+sub_folder)
    #full_name_list = ['d3/d3','sjain3097/new','subrahmanyamm/springboot']
    config = Utils().get_config_file('config.ini')
    file_name = config.get('file', 'csv_file_name', raw=True)
    data_frame = pd.read_csv(file_name)
    full_name_list = list(data_frame['repository_name'].unique())
    owner = []
    repository = []
    start = time.time()
    for full_name in full_name_list:
        owner_repository = full_name.split('/')
        owner.append(owner_repository[0])
        repository.append(owner_repository[1])
    create_process(owner, repository)
    print(concurrent.futures.as_completed(FUTURES_LIST))
if __name__ == '__main__':
    #print(time.asctime(time.localtime(time.time())), ' starting main thread')
    try:
        SCHED = BackgroundScheduler(daemon=True)
        #change this 23 hours
        SCHED.add_job(scheduled_job, 'interval', seconds=6, coalesce=True)
        StoreModel.storeData()
        SCHED.start()
        runner()
    except KeyboardInterrupt as e:
        print(e)  
