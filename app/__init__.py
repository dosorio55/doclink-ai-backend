from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes.uploads import uploads_bp
from .routes.files import files_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(files_bp)
    return app
