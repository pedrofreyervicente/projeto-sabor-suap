from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import Professores, Disciplinas, Turmas, RelacionamentoProfessor, RelacionamentoTurma
from views import ViewHome
from sqlalchemy import select, func

cadastro_professor_bp = Blueprint("cadastro_professor", __name__, url_prefix="/cadastro/professor")

@cadastro_professor_bp.route("", methods=["GET", "POST"])
def listar_professores():
    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()
        
    if request.method == "POST":
        id_professor_form = request.form.get("id_professor")
        nome_form = request.form.get("nome")
        ids_turmas_form = request.form.getlist("id_turma")
        ids_disciplinas_form = request.form.getlist("id_disciplina")

        if id_professor_form:
            professor_existente = Professores.query.get(id_professor_form)
            if professor_existente:
                return redirect(url_for("cadastro_professor.listar_professores"))

        novo_professor = Professores(
            idProfessor=int(id_professor_form) if id_professor_form else None,
            nome=nome_form
        )
        db.session.add(novo_professor)
        db.session.flush()

        # Vincula Múltiplas Turmas x Múltiplas Disciplinas
        if ids_turmas_form and ids_disciplinas_form:
            for id_turma in ids_turmas_form:
                for id_disc in ids_disciplinas_form:
                    # 1. Garante que o vínculo Turma x Disciplina exista na RelacionamentoTurma
                    rel_t = RelacionamentoTurma.query.filter_by(
                        idTurma=id_turma, 
                        idDisciplina=id_disc
                    ).first()
                    if not rel_t:
                        db.session.add(RelacionamentoTurma(idTurma=id_turma, idDisciplina=id_disc))

                    # 2. Registra o Professor para aquela Turma + Disciplina
                    rel_p = RelacionamentoProfessor(
                        idProfessor=novo_professor.idProfessor,
                        idTurma=id_turma,
                        idDisciplina=id_disc
                    )
                    db.session.add(rel_p)

        elif ids_turmas_form:
            for id_turma in ids_turmas_form:
                rel_p = RelacionamentoProfessor(
                    idProfessor=novo_professor.idProfessor,
                    idTurma=id_turma,
                    idDisciplina=None
                )
                db.session.add(rel_p)

        db.session.commit()
        return redirect(url_for("cadastro_professor.listar_professores"))

    turmas = Turmas.listar_turmas() if hasattr(Turmas, 'listar_turmas') else Turmas.query.all()
    disciplinas = Disciplinas.listar_disciplinas() if hasattr(Disciplinas, 'listar_disciplinas') else Disciplinas.query.all()

    stmt = (
        select(
            Professores, 
            func.group_concat(Turmas.nome.distinct()).label("nome_turma"),
            func.group_concat(Disciplinas.nome.distinct()).label("nome_disciplina")
        )
        .outerjoin(RelacionamentoProfessor, Professores.idProfessor == RelacionamentoProfessor.idProfessor)
        .outerjoin(Turmas, RelacionamentoProfessor.idTurma == Turmas.idTurma)
        .outerjoin(Disciplinas, RelacionamentoProfessor.idDisciplina == Disciplinas.idDisciplina)
        .group_by(Professores.idProfessor)
        .order_by(Professores.nome)
    )
    
    resultados = db.session.execute(stmt).all()

    professores = []
    for professor_obj, nome_turma, nome_disciplina in resultados:
        if nome_turma:
            professor_obj.turma_nome = ", ".join([t.strip() for t in nome_turma.split(",") if t.strip()])
        else:
            professor_obj.turma_nome = "Sem turma"

        if nome_disciplina:
            professor_obj.disciplina_nome = ", ".join([d.strip() for d in nome_disciplina.split(",") if d.strip()])
        else:
            professor_obj.disciplina_nome = "Sem disciplina"

        professores.append(professor_obj)

    return render_template(
        "cadastro/lista-professores.html",
        professores=professores,
        turmas=turmas,
        disciplinas=disciplinas,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )


@cadastro_professor_bp.route("/editar/<int:id_professor>", methods=["GET", "POST"])
def editar_professor(id_professor):
    professor = Professores.query.get_or_404(id_professor)

    if request.method == "POST":
        professor.nome = request.form.get("nome")
        ids_turmas_novas = request.form.getlist("id_turma")
        ids_disciplinas_novas = request.form.getlist("id_disciplina")

        try:
            RelacionamentoProfessor.query.filter_by(idProfessor=id_professor).delete()

            if ids_turmas_novas and ids_disciplinas_novas:
                for id_turma in ids_turmas_novas:
                    for id_disc in ids_disciplinas_novas:
                        # 1. Garante o vínculo em RelacionamentoTurma
                        rel_t = RelacionamentoTurma.query.filter_by(
                            idTurma=id_turma, 
                            idDisciplina=id_disc
                        ).first()
                        if not rel_t:
                            db.session.add(RelacionamentoTurma(idTurma=id_turma, idDisciplina=id_disc))

                        # 2. Atualiza o vínculo do Professor
                        rel_p = RelacionamentoProfessor(
                            idProfessor=id_professor,
                            idTurma=id_turma,
                            idDisciplina=id_disc
                        )
                        db.session.add(rel_p)

            elif ids_turmas_novas:
                for id_turma in ids_turmas_novas:
                    rel_p = RelacionamentoProfessor(
                        idProfessor=id_professor,
                        idTurma=id_turma,
                        idDisciplina=None
                    )
                    db.session.add(rel_p)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao editar professor: {e}")

        return redirect(url_for("cadastro_professor.listar_professores"))

    rels_atuais = RelacionamentoProfessor.query.filter_by(idProfessor=id_professor).all()
    professor.ids_turmas_atuais = [str(r.idTurma) for r in rels_atuais if r.idTurma]
    professor.ids_disciplinas_atuais = [str(r.idDisciplina) for r in rels_atuais if r.idDisciplina]

    turmas = Turmas.listar_turmas() if hasattr(Turmas, 'listar_turmas') else Turmas.query.all()
    disciplinas = Disciplinas.listar_disciplinas() if hasattr(Disciplinas, 'listar_disciplinas') else Disciplinas.query.all()
    
    stmt = (
        select(
            Professores, 
            func.group_concat(Turmas.nome.distinct()).label("nome_turma"),
            func.group_concat(Disciplinas.nome.distinct()).label("nome_disciplina")
        )
        .outerjoin(RelacionamentoProfessor, Professores.idProfessor == RelacionamentoProfessor.idProfessor)
        .outerjoin(Turmas, RelacionamentoProfessor.idTurma == Turmas.idTurma)
        .outerjoin(Disciplinas, RelacionamentoProfessor.idDisciplina == Disciplinas.idDisciplina)
        .group_by(Professores.idProfessor)
        .order_by(Professores.nome)
    )
    resultados = db.session.execute(stmt).all()
    professores = []
    for professor_obj, nome_turma, nome_disciplina in resultados:
        if nome_turma:
            professor_obj.turma_nome = ", ".join([t.strip() for t in nome_turma.split(",") if t.strip()])
        else:
            professor_obj.turma_nome = "Sem turma"

        if nome_disciplina:
            professor_obj.disciplina_nome = ", ".join([d.strip() for d in nome_disciplina.split(",") if d.strip()])
        else:
            professor_obj.disciplina_nome = "Sem disciplina"

        professores.append(professor_obj)

    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()

    return render_template(
        "cadastro/lista-professores.html",
        professores=professores,
        turmas=turmas,
        disciplinas=disciplinas,
        professor_edicao=professor,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )

@cadastro_professor_bp.route("/deletar/<int:id_professor>", methods=["POST", "GET"])
def deletar_professor(id_professor):
    try:
        relacionamentos = RelacionamentoProfessor.query.filter_by(idProfessor=id_professor).all()
        for rel in relacionamentos:
            db.session.delete(rel)

        professor = Professores.query.get(id_professor)
        if professor:
            db.session.delete(professor)
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar professor: {e}")

    return redirect(url_for("cadastro_professor.listar_professores"))