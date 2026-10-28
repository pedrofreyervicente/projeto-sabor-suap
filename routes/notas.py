from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request
from models import Disciplinas, Notas

notas_bp = Blueprint("notas", __name__, url_prefix="/notas")


def converter_nota(valor):
    """Converte '7,5' ou '7.5' em Decimal. Retorna None se for inválido."""
    try:
        nota = Decimal(str(valor).strip().replace(",", "."))
    except InvalidOperation:
        return None
    if nota < 0 or nota > 10:
        return None
    return nota.quantize(Decimal("0.01"))


@notas_bp.route("/salva-nota", methods=["POST"])
def salvarNota():
    dados = request.get_json()

    idProfessor = dados.get("idProfessor")
    idTurma = dados.get("idTurma")
    idDisciplina = dados.get("idDisciplina")
    notas = dados.get("notas", {})

    registros = []

    for idAluno, nota in notas.items():
        if nota is None or nota == "":
            continue

        id_aluno = int(idAluno)
        valor_nota = converter_nota(nota)

        if valor_nota is None:
            return {
                "status": "erro",
                "mensagem": f"Nota inválida para o aluno {id_aluno}. Use um valor entre 0 e 10."
            }, 400

        registro = Notas.salvaNotas(
            int(idProfessor), int(idTurma), int(idDisciplina), id_aluno, valor_nota
        )

        if registro is False:
            return {
                "status": "erro",
                "mensagem": f"Não foi possível salvar a nota do aluno {id_aluno}."
            }, 500

        registros.append({"idAluno": id_aluno, "nota": float(valor_nota)})

    return {"status": "sucesso", "registros": registros}