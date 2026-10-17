from database import db

class RelacionamentoProfessor(db.Model):
    __tablename__ = 'relacionamentoprofessor'

    id = db.Column(db.Integer, primary_key=True)
    idProfessor = db.Column(db.Integer, nullable=True)
    idTurma = db.Column(db.Integer, nullable=True)
    idDisciplina = db.Column(db.Integer, nullable=True)