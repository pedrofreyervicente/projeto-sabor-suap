from database import db

class Disciplinas(db.Model):
    __tablename__ = 'disciplinas'

    idDisciplina = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    @staticmethod
    def listar_disciplinas():
        return Disciplinas.query.all()