from flask import Blueprint, render_template
from database import db
from models import Professores, Alunos

cadastro_bp = Blueprint("cadastro", __name__, url_prefix="/cadastro")

@cadastro_bp.route("")
def lista():
    professores = Professores.listar_professores()
    alunos = Alunos.listar_alunos()
    return render_template("cadastro/lista.html", professores=professores, alunos=alunos)

@cadastro_bp.route("/aluno/<int:id>")
def aluno(id):
    aluno = db.get_or_404(Alunos, id)
    return render_template("cadastro/aluno.html", aluno=aluno)

@cadastro_bp.route("/professor/<int:id>")
def professor(id):
    professor = db.get_or_404(Professores, id)
    return render_template("cadastro/professor.html", professor=professor)