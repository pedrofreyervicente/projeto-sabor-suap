from flask import Blueprint, render_template
from models import Disciplinas

notas_bp = Blueprint("notas", __name__, url_prefix="/notas")

@notas_bp.route("")
def lista():
    disciplinas = Disciplinas.listar_disciplinas()
    return render_template("notas.html", disciplinas=disciplinas)