from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
from  ml_model.ml_model import MLModel
from flask import Flask
from datetime import datetime
import time
import threading
from store_model.store_model import StoreModel

app = Flask(__name__)
#StoreModel.storeData()
from web_git_prediction.views import *
