import os

HOST = os.getenv('HOST_NAME', '127.0.0.1')
PORT = os.getenv('PORT', '5005')
USE_RELOADER = os.getenv('USE_RELOADER', 'False')
DEBUG = os.getenv('DEBUG', 'True')

