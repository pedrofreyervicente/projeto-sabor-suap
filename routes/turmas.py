from flask import Blueprint, render_template
from database import db
from models import Turmas
from views import ViewTurmas

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
    turma = db.get_or_404(Turmas, id)
    return render_template("turmas/detalhe.html", turma=turma)