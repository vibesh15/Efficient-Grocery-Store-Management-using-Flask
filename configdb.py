
from flask_sqlalchemy import SQLAlchemy
import config as config
from sqlalchemy import create_engine
    
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy()