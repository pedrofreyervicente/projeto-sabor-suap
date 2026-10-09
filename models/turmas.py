from database import db

class Turmas(db.Model):
    __tablename__ = 'turmas'

    idTurma = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    ano = db.Column(db.Integer, nullable=True)

    @staticmethod
    def listar_turmas():
        return Turmas.query.all()