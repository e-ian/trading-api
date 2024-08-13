from flask import Flask
from .config import Config
from .forex_ticker import api_blueprint
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = os.getenv('SECRET_KEY', 'eebd61a1c94d7fe7696f584cd523418e06d4a247a1ff29fb')

    app.register_blueprint(api_blueprint, url_prefix='/forex_tickers')

    return app
