from flask import Blueprint, render_template
from views import ViewHome

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()
    return render_template("home.html", totalTurmas=totalTurmas, totalAlunos=totalAlunos, totalProfessores=totalProfessores, totalDisciplinas=totalDisciplinas)