from database import db

class Professores(db.Model):
    __tablename__ = 'professores'

    idProfessor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    @staticmethod
    def listar_professores():
        return Professores.query.all()