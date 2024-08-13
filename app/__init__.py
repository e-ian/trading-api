from flask import Flask
from .config import Config
from .forex_ticker import api_blueprint
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = os.getenv('SECRET_KEY')

    app.register_blueprint(api_blueprint, url_prefix='/forex_tickers')

    return app
