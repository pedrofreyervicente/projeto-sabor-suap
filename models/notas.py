from database import db
from sqlalchemy import func

class Notas(db.Model):
    __tablename__ = 'notas'

    idNotas = db.Column(db.Integer, primary_key=True)
    idProfessor = db.Column(db.Integer, nullable=False)
    idDisciplina = db.Column(db.Integer, nullable=True)
    idTurma = db.Column(db.Integer, nullable=True)
    idAluno = db.Column(db.Integer, nullable=True)
    nota = db.Column(db.Numeric (4, 2), nullable=False)

    
    @staticmethod
    def salvaNotas( idProfessor, idTurma, idDisciplina, idAluno, nota):
        try:
            registro = Notas.query.filter_by(
                idTurma=idTurma,
                idDisciplina=idDisciplina,
                idAluno=idAluno
            ).first()

            if registro:
                registro.nota = nota
                registro.idProfessor = idProfessor

            else:
                novo_registro = Notas(
                    idProfessor=idProfessor,
                    idTurma=idTurma,
                    idDisciplina=idDisciplina,
                    idAluno=idAluno,
                    nota=nota
                )
                db.session.add(novo_registro)

            db.session.commit()
            return registro
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar nota: {e}")
            return False

    @staticmethod
    def mediasPorTurma(idTurma):
        linhas = (
        db.session.query(Notas.idAluno, func.avg(Notas.nota))
        .filter(Notas.idTurma == idTurma, Notas.nota.isnot(None))
        .group_by(Notas.idAluno)
        .all()
    )
        return {idAluno: round(float(media), 1) for idAluno, media in linhas}

def calcularConceito(nota):
    if nota is None:
        return ''
    
    if nota >= 9:
        return 'A'

    elif nota >= 8 and nota < 9:
        return 'B'

    elif nota >= 6 and nota < 8:
        return 'C'

    else:
        return 'D'

def calcularSituacao(nota):
    if nota is None:
        return ''
    return 'Aprovado' if nota >= 6 else 'Reprovado'

def corConceito(conceito):
    return {
        'A': 'bg-green-600',
        'B': 'bg-blue-600',
        'C': 'bg-yellow-500',
        'D': 'bg-red-600',
    }.get(conceito, 'bg-gray-400')