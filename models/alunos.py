from database import db

class Alunos(db.Model):
    __tablename__ = 'alunos'

    idAluno = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(100), nullable=True)

    @staticmethod
    def listar_alunos():
        return Alunos.query.all()