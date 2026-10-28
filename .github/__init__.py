from .main import main_bp
from .turmas import turmas_bp
from .cadastro_aluno import cadastro_aluno_bp
from .cadastro_professor import cadastro_professor_bp

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(cadastro_aluno_bp)
    app.register_blueprint(cadastro_professor_bp)