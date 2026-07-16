from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes.messages import messages_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # importar modelos
    from .models import message

    app.register_blueprint(messages_bp, url_prefix="/messages")

    return app