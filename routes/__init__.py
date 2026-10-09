from .main import main_bp
from .turmas import turmas_bp
from .cadastro import cadastro_bp
from .notas import notas_bp

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(cadastro_bp)
    app.register_blueprint(notas_bp)