from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import Turmas, RelacionamentoTurma
from views import ViewHome

cadastro_turma_bp = Blueprint("cadastro_turma", __name__, url_prefix="/cadastro/turma")

@cadastro_turma_bp.route("", methods=["GET", "POST"])
def listar_turmas():
    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()

    if request.method == "POST":
        id_turma_form = request.form.get("id_turma")
        nome_form = request.form.get("nome")
        ano_form = request.form.get("ano")

        if id_turma_form:
            turma_existente = Turmas.query.get(id_turma_form)
            if turma_existente:
                return redirect(url_for("cadastro_turma.listar_turmas"))

        nova_turma = Turmas(
            idTurma=int(id_turma_form) if id_turma_form else None,
            nome=nome_form,
            ano=int(ano_form) if ano_form else None
        )
        db.session.add(nova_turma)
        db.session.commit()

        return redirect(url_for("cadastro_turma.listar_turmas"))

    turmas = Turmas.listar_turmas()

    return render_template(
        "cadastro/lista-turmas.html",
        turmas=turmas,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )


@cadastro_turma_bp.route("/editar/<int:id_turma>", methods=["GET", "POST"])
def editar_turma(id_turma):
    turma = Turmas.query.get_or_404(id_turma)

    if request.method == "POST":
        turma.nome = request.form.get("nome")
        ano_form = request.form.get("ano")
        turma.ano = int(ano_form) if ano_form else None

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao editar turma: {e}")

        return redirect(url_for("cadastro_turma.listar_turmas"))

    turmas = Turmas.listar_turmas()

    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()

    return render_template(
        "cadastro/lista-turmas.html",
        turmas=turmas,
        turma_edicao=turma,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )


@cadastro_turma_bp.route("/deletar/<int:id_turma>", methods=["POST", "GET"])
def deletar_turma(id_turma):
    try:
        relacionamentos = RelacionamentoTurma.query.filter_by(idTurma=id_turma).all()
        for rel in relacionamentos:
            db.session.delete(rel)

        turma = Turmas.query.get(id_turma)
        if turma:
            db.session.delete(turma)
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar turma: {e}")

    return redirect(url_for("cadastro_turma.listar_turmas"))