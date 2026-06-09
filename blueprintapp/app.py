from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_equipo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key ="holabb"
    
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from blueprintapp.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 1. Importación del blueprint (Para cada modulo)
    from blueprintapp.auth.routes import auth_bp
    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea
    
    # 2. Registrar el blueprint (Para cada modulo)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_miembro,url_prefix="/miembros")
    app.register_blueprint(bp_core,url_prefix="/")
    app.register_blueprint(bp_tarea,url_prefix="/tareas")
    
    return app