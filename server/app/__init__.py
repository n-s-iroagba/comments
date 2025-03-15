from flask import Flask
from flask_migrate import Migrate
from .models import db
import config
from .controllers.job_controller import jobs_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    app.app_context().push()
    db.init_app(app)
    app.register_blueprint(jobs_bp)
    db.create_all()
    Migrate(app, db)
    
    return app


