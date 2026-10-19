from flask import Blueprint, render_template
from database import db
from models import Turmas, Notas
from models.notas import calcularConceito, calcularSituacao, corConceito
from views import ViewTurmas, DetalheTurma

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")

@turmas_bp.route("")
def lista(): 
    turmas = ViewTurmas().getTurmas()
    totalTurmas = ViewTurmas().getTotalTurmas()
    totalAlunos = ViewTurmas().getTotalAlunos()
    totalProfessores = ViewTurmas().getTotalProfessores()
    totalDisciplinas = ViewTurmas().getTotalDisciplinas()

    detalhes = {}
    for turma in turmas:
        detalhes[turma.idTurma] = DetalheTurma(turma.idTurma).getDadosTurma()

    return render_template(
        "turmas/lista.html",
        turmas=turmas,
        totalTurmas=totalTurmas,
        totalAlunos=totalAlunos,
        totalProfessores=totalProfessores,
        totalDisciplinas=totalDisciplinas,
        detalhes=detalhes
    )

@turmas_bp.route("/<int:id>")
def detalhe(id):
    detalhe = DetalheTurma(id)
    dados_turma = detalhe.getDadosTurma()

    medias = Notas.mediasPorTurma(id)

    alunos_com_conceito = []
    for aluno in dados_turma["alunos"]:
        id_aluno = aluno["idAluno"] if isinstance(aluno, dict) else aluno.idAluno
        media = medias.get(id_aluno)
        conceito = calcularConceito(media)

        item = dict(aluno) if isinstance(aluno, dict) else {
            "idAluno": aluno.idAluno,
            "nome": aluno.nome,
            "data": aluno.data,
        }
        item["media"] = media if media is not None else "-"
        item["conceito"] = conceito
        item["corConceito"] = corConceito(conceito)
        item["situacao"] = calcularSituacao(media)
        alunos_com_conceito.append(item)

        dados_turma["alunos"] = alunos_com_conceito

    return render_template(
        "turmas/detalhe.html",
        dados=dados_turma
    )

@turmas_bp.route("/<int:idTurma>/<int:idDisciplina>")
def detalheDisciplina(idTurma, idDisciplina):
    detalhe = DetalheTurma(idTurma)
    dados_turma = detalhe.getDadosTurma(idDisciplina)
    turma = dados_turma["turma"]
    alunos = dados_turma["alunos"]

    disciplina = next(
        (d for d in detalhe.getDisciplinas() if d.idDisciplina == idDisciplina),
        None
    )

    registros = Notas.query.filter_by(
        idTurma=idTurma,
        idDisciplina=idDisciplina
    ).all()
    notas_por_aluno = {r.idAluno: r.nota for r in registros}

    alunos_com_conceito = []
    notas_lancadas = []

    for aluno in alunos:
        id_aluno = aluno["idAluno"] if isinstance(aluno, dict) else aluno.idAluno
        nota = notas_por_aluno.get(id_aluno)
        conceito = calcularConceito(nota)

        item = dict(aluno) if isinstance(aluno, dict) else {
            "idAluno": aluno.idAluno,
            "nome": aluno.nome,
            "data": aluno.data,
        }
        item["nota"] = nota
        item["conceito"] = conceito
        item["corConceito"] = corConceito(conceito)
        item["situacao"] = calcularSituacao(nota)
        alunos_com_conceito.append(item)

        if nota is not None:
            notas_lancadas.append(nota)

    media = round(sum(notas_lancadas) / len(notas_lancadas), 1) if notas_lancadas else None


    return render_template(
        "turmas/detalhe-disciplinas.html",
        turma=turma,
        alunos=alunos_com_conceito,
        disciplina=disciplina,
        totalAlunos=dados_turma["quantidadeAlunos"],
        media=media,
        conceitoMedia=calcularConceito(media)
    )