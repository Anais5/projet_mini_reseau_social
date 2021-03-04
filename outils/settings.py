import os
import socket

APP_ROOT = os.path.dirname(os.path.dirname(__file__))
DB_NAME = 'mini_blog.db'
DB_DIR = os.path.join(APP_ROOT, DB_NAME)
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)