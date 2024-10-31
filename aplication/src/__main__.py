from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.secret_key = os.getenv("KEY")
    


    from aplication.src.routes.home import home_
    app.register_blueprint(home_)


    return app