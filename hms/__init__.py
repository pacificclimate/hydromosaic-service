import connexion
from flask_cors import CORS

connexion_app = None
flask_app = None


def create_app():
    global connexion_app, flask_app
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/")
    flask_app = connexion_app.app

    CORS(flask_app)

    ## database initialization will go here.

    connexion_app.add_api("api-spec.yaml")

    return connexion_app, flask_app
