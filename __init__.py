from flask import Flask
from main import bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'
    app.register_blueprint(bp)
    return app