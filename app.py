from flask import Flask
import config as config
from database.configdb import db
from database.models import Manager
from database.configdb import engine
from sqlalchemy.orm import Session

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config.LocalDatabaseConfig)
    db.init_app(app)
    app.app_context().push()
    return app


app = create_app()


with Session(engine) as session:
    try:
        manager = session.query(Manager).filter_by(managername="admin").first()
        if manager is None:
            print("Creating new manager...")
            manager = Manager(managername="admin", password="admin")
            session.add(manager)
            session.commit()
            print("Manager created:",manager.managername)
        else:
            print("Manager found:",manager.managername)
    except Exception as e:
        print("Some error occured while checking manager",e)
        session.rollback()



from routes import *

if __name__ == "__main__":
    app.run()


