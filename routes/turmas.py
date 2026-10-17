from flask import Blueprint, render_template
from database import db
from models import Turmas
from views import ViewTurmas, DetalheTurma

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")

@turmas_bp.route("")
def lista():
    turmas = ViewTurmas().getTurmas()
    totalTurmas = ViewTurmas().getTotalTurmas()
    totalAlunos = ViewTurmas().getTotalAlunos()
    totalProfessores = ViewTurmas().getTotalProfessores()
    totalDisciplinas = ViewTurmas().getTotalDisciplinas()

    return render_template(
        "turmas/lista.html",
        turmas=turmas,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )

@turmas_bp.route("/<int:id>")
def detalhe(id):
    detalhe = DetalheTurma(id)
    dados_turma = detalhe.getDadosTurma()
    return render_template(
        "turmas/detalhe.html",
        dados=dados_turma
    )