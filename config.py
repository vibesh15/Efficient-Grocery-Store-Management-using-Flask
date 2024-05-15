
DEBUG = True
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join( BASE_DIR , './api_database.sqlite3' )
DATABASE_CONNECT_OPTIONS = {}

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATION = False

class LocalDatabaseConfig(Config):
    SQLITE_DB_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join( BASE_DIR , './api_database.sqlite3' )
    DEBUG = True



# SECRET_KEY = 'Same as Session Key'