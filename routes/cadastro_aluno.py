from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import Professores, Alunos, Disciplinas, Turmas, RelacionamentoAluno
from views import ViewHome
from sqlalchemy import select

cadastro_aluno_bp = Blueprint("cadastro", __name__, url_prefix="/cadastro/alunos")

@cadastro_aluno_bp.route("", methods=["GET", "POST"])
def listar_alunos():
    totalTurmas = ViewHome().turmas.query.count()
    totalAlunos = ViewHome().getTotalAlunos()
    totalProfessores = ViewHome().getTotalProfessores()
    totalDisciplinas = ViewHome().getTotalDisciplinas()
        
    if request.method == "POST":
        id_aluno_form = request.form.get("id_aluno")
        nome_form = request.form.get("nome")
        data_form = request.form.get("data_nascimento")
        id_turma_form = request.form.get("id_turma")

        aluno_existente = Alunos.query.get(id_aluno_form)
        if aluno_existente:
            return redirect(url_for("cadastro.listar_alunos"))

        novo_aluno = Alunos(
            idAluno=id_aluno_form,
            nome=nome_form,
            data=data_form
        )
        db.session.add(novo_aluno)

        if id_turma_form:
            disciplinas = Disciplinas.listar_disciplinas()

            if disciplinas:
                for disc in disciplinas:
                    relacionamento = RelacionamentoAluno(
                        idAluno=id_aluno_form,
                        idTurma=id_turma_form,
                        idDisciplina=disc.idDisciplina
                    )
                    db.session.add(relacionamento)
            else:
                pass

        db.session.commit()
        
        return redirect(url_for("cadastro.listar_alunos"))
        return redirect(url_for("cadastro.lista"))
        

    alunos = Alunos.listar_alunos()
    turmas = Turmas.listar_turmas()

    stmt = (
        select(Alunos, Turmas.nome.label("nome_turma"))
        .outerjoin(RelacionamentoAluno, Alunos.idAluno == RelacionamentoAluno.idAluno)
        .outerjoin(Turmas, RelacionamentoAluno.idTurma == Turmas.idTurma)
        .distinct()
        .order_by(Alunos.nome)
    )
    
    resultados = db.session.execute(stmt).all()

    alunos = []
    for aluno_obj, nome_turma in resultados:
        aluno_obj.turma_nome = nome_turma if nome_turma else "Sem turma"
        alunos.append(aluno_obj)

    return render_template(
        "cadastro/lista-alunos.html",
        alunos=alunos,
        turmas=turmas,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas
    )

@cadastro_aluno_bp.route("/editar/<int:id_aluno>", methods=["GET", "POST"])
def editar_aluno(id_aluno):
    aluno = Alunos.query.get_or_404(id_aluno)

    if request.method == "POST":
        aluno.nome = request.form.get("nome")
        aluno.data = request.form.get("data_nascimento")

        id_turma_nova = request.form.get("id_turma")

        try:
            RelacionamentoAluno.query.filter_by(idAluno=id_aluno).delete()

            if id_turma_nova:
                disciplinas = Disciplinas.listar_disciplinas() if hasattr(Disciplinas, 'listar_disciplinas') else Disciplinas.query.all()
                if disciplinas:
                    for disc in disciplinas:
                        rel = RelacionamentoAluno(
                            idAluno=id_aluno,
                            idTurma=id_turma_nova,
                            idDisciplina=disc.idDisciplina
                        )
                        db.session.add(rel)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao editar aluno: {e}")

        return redirect(url_for("cadastro.listar_alunos"))

    rel_atual = RelacionamentoAluno.query.filter_by(idAluno=id_aluno).first()
    aluno.id_turma_atual = str(rel_atual.idTurma) if rel_atual else ""

    turmas = Turmas.listar_turmas() if hasattr(Turmas, 'listar_turmas') else Turmas.query.all()
    
    stmt = (
        select(Alunos, Turmas.nome.label("nome_turma"))
        .outerjoin(RelacionamentoAluno, Alunos.idAluno == RelacionamentoAluno.idAluno)
        .outerjoin(Turmas, RelacionamentoAluno.idTurma == Turmas.idTurma)
        .distinct()
        .order_by(Alunos.nome)
    )
    resultados = db.session.execute(stmt).all()
    alunos = []
    for aluno_obj, nome_turma in resultados:
        aluno_obj.turma_nome = nome_turma if nome_turma else "Sem turma"
        alunos.append(aluno_obj)

    return render_template(
        "cadastro/lista-alunos.html",
        alunos=alunos,
        turmas=turmas,
        aluno_edicao=aluno
    )

@cadastro_aluno_bp.route("/deletar/<int:id_aluno>", methods=["POST", "GET"])
def deletar_aluno(id_aluno):
    try:
        relacionamentos = RelacionamentoAluno.query.filter_by(idAluno=id_aluno).all()
        for rel in relacionamentos:
            db.session.delete(rel)

        aluno = Alunos.query.get(id_aluno)
        if aluno:
            db.session.delete(aluno)
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar aluno: {e}")

    return redirect(url_for("cadastro.listar_alunos"))