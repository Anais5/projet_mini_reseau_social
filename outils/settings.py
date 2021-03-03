import os

APP_ROOT = os.path.dirname(os.path.dirname(__file__))
DB_NAME = 'mini_blog.db'
DATABASE = os.path.join(APP_ROOT, DB_NAME)
PORT = 40000