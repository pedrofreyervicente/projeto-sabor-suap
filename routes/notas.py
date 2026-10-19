from flask import Blueprint, render_template, request
from models import Disciplinas, Notas

notas_bp = Blueprint("notas", __name__, url_prefix="/notas")

@notas_bp.route("")
def lista():
    disciplinas = Disciplinas.listar_disciplinas()
    return render_template("notas.html", disciplinas=disciplinas)


@notas_bp.route("/salva-nota", methods=["POST"])
def salvarNota():
    dados = request.get_json()

    idProfessor = dados.get("idProfessor")
    idTurma = dados.get("idTurma")
    idDisciplina = dados.get("idDisciplina")

    notas = dados.get("notas", {})

    registros = []

    for idAluno, nota in notas.items():
        if nota is not None and nota != "":
            id_aluno = int(idAluno)
            valor_nota = int(nota)
            registro = Notas.salvaNotas(
                int(idProfessor),
                int(idTurma),
                int(idDisciplina),
                id_aluno,
                valor_nota
            )

            if registro is False:
                return {
                    "status": "erro",
                    "mensagem": f"Não foi possível salvar a nota do aluno {id_aluno}."
                }, 500

            registros.append({
                "idAluno": id_aluno,
                "nota": valor_nota
            })

    return {
        "status": "sucesso",
        "dados": dados,
        "registros": registros
    }