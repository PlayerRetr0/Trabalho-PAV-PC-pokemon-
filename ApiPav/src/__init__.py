from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from src.models.base import db
import os
from src.routes.endpoints import endpoints

#.\venv\Scripts\Activate.ps1
#flask --app manage run --host=0.0.0.0 --port=5001

def create_app() -> Flask:

    app = Flask(__name__)
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    api = Api(app)

    endpoints(api)

    with app.app_context():
        db.create_all()

    return app