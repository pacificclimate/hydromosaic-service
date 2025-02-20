import os
import connexion
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

connexion_app = None
flask_app = None


def create_app():
    global connexion_app, flask_app, app_db
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/")
    flask_app = connexion_app.app

    CORS(flask_app)

    flask_app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("HMS_DSN", ""),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=False,
        )
    app_db = SQLAlchemy(flask_app)


    connexion_app.add_api("api-spec.yaml")

    return connexion_app, flask_app, app_db

def get_app_session():
    return app_db.session