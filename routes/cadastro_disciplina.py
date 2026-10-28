from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import Disciplinas, Turmas, RelacionamentoTurma
from views import ViewHome
from sqlalchemy import select, func

cadastro_disciplina_bp = Blueprint("cadastro_disciplina", __name__, url_prefix="/cadastro/disciplina")

@cadastro_disciplina_bp.route("", methods=["GET", "POST"])
def listar_disciplinas():
    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()
        
    if request.method == "POST":
        id_disciplina_form = request.form.get("id_disciplina")
        nome_form = request.form.get("nome")
        ids_turmas_form = request.form.getlist("id_turma")

        if id_disciplina_form:
            disciplina_existente = Disciplinas.query.get(id_disciplina_form)
            if disciplina_existente:
                return redirect(url_for("cadastro_disciplina.listar_disciplinas"))

        nova_disciplina = Disciplinas(
            idDisciplina=int(id_disciplina_form) if id_disciplina_form else None,
            nome=nome_form
        )
        db.session.add(nova_disciplina)
        db.session.flush()

        if ids_turmas_form:
            for id_turma in ids_turmas_form:
                rel_existente = RelacionamentoTurma.query.filter_by(
                    idTurma=id_turma,
                    idDisciplina=nova_disciplina.idDisciplina
                ).first()

                if not rel_existente:
                    relacionamento = RelacionamentoTurma(
                        idTurma=id_turma,
                        idDisciplina=nova_disciplina.idDisciplina
                    )
                    db.session.add(relacionamento)

        db.session.commit()
        return redirect(url_for("cadastro_disciplina.listar_disciplinas"))

    turmas = Turmas.listar_turmas() if hasattr(Turmas, 'listar_turmas') else Turmas.query.all()

    stmt = (
        select(
            Disciplinas, 
            func.group_concat(Turmas.nome.distinct()).label("nome_turma")
        )
        .outerjoin(RelacionamentoTurma, Disciplinas.idDisciplina == RelacionamentoTurma.idDisciplina)
        .outerjoin(Turmas, RelacionamentoTurma.idTurma == Turmas.idTurma)
        .group_by(Disciplinas.idDisciplina)
        .order_by(Disciplinas.nome)
    )
    
    resultados = db.session.execute(stmt).all()

    disciplinas = []
    for disciplina_obj, nome_turma in resultados:
        if nome_turma:
            disciplina_obj.turma_nome = ", ".join([t.strip() for t in nome_turma.split(",") if t.strip()])
        else:
            disciplina_obj.turma_nome = "Sem turma"

        disciplinas.append(disciplina_obj)

    return render_template(
        "cadastro/lista-disciplinas.html",
        disciplinas=disciplinas,
        turmas=turmas,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )


@cadastro_disciplina_bp.route("/editar/<int:id_disciplina>", methods=["GET", "POST"])
def editar_disciplina(id_disciplina):
    disciplina = Disciplinas.query.get_or_404(id_disciplina)

    if request.method == "POST":
        disciplina.nome = request.form.get("nome")
        ids_turmas_novas = request.form.getlist("id_turma")

        try:
            RelacionamentoTurma.query.filter_by(idDisciplina=id_disciplina).delete()

            if ids_turmas_novas:
                for id_turma in ids_turmas_novas:
                    rel = RelacionamentoTurma(
                        idTurma=id_turma,
                        idDisciplina=id_disciplina
                    )
                    db.session.add(rel)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao editar disciplina: {e}")

        return redirect(url_for("cadastro_disciplina.listar_disciplinas"))

    rels_atuais = RelacionamentoTurma.query.filter_by(idDisciplina=id_disciplina).all()
    disciplina.ids_turmas_atuais = [str(r.idTurma) for r in rels_atuais if r.idTurma]

    turmas = Turmas.listar_turmas() if hasattr(Turmas, 'listar_turmas') else Turmas.query.all()
    
    stmt = (
        select(
            Disciplinas, 
            func.group_concat(Turmas.nome.distinct()).label("nome_turma")
        )
        .outerjoin(RelacionamentoTurma, Disciplinas.idDisciplina == RelacionamentoTurma.idDisciplina)
        .outerjoin(Turmas, RelacionamentoTurma.idTurma == Turmas.idTurma)
        .group_by(Disciplinas.idDisciplina)
        .order_by(Disciplinas.nome)
    )
    resultados = db.session.execute(stmt).all()
    disciplinas = []
    for disciplina_obj, nome_turma in resultados:
        if nome_turma:
            disciplina_obj.turma_nome = ", ".join([t.strip() for t in nome_turma.split(",") if t.strip()])
        else:
            disciplina_obj.turma_nome = "Sem turma"

        disciplinas.append(disciplina_obj)

    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()

    return render_template(
        "cadastro/lista-disciplinas.html",
        disciplinas=disciplinas,
        turmas=turmas,
        disciplina_edicao=disciplina,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )


@cadastro_disciplina_bp.route("/deletar/<int:id_disciplina>", methods=["POST", "GET"])
def deletar_disciplina(id_disciplina):
    try:
        relacionamentos = RelacionamentoTurma.query.filter_by(idDisciplina=id_disciplina).all()
        for rel in relacionamentos:
            db.session.delete(rel)

        disciplina = Disciplinas.query.get(id_disciplina)
        if disciplina:
            db.session.delete(disciplina)
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar disciplina: {e}")

    return redirect(url_for("cadastro_disciplina.listar_disciplinas"))