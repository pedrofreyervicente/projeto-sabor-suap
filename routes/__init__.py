from .main import main_bp
from .turmas import turmas_bp
from .cadastro_aluno import cadastro_aluno_bp
from .cadastro_professor import cadastro_professor_bp
from .cadastro_disciplina import cadastro_disciplina_bp
from .cadastro_turma import cadastro_turma_bp
from .notas import notas_bp

def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(notas_bp)
    app.register_blueprint(cadastro_aluno_bp)
    app.register_blueprint(cadastro_professor_bp)
    app.register_blueprint(cadastro_disciplina_bp)
    app.register_blueprint(cadastro_turma_bp)