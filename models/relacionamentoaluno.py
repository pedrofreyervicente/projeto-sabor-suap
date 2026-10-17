from database import db

class RelacionamentoAluno(db.Model):
    __tablename__ = 'relacionamentoaluno'

    idAluno = db.Column(db.Integer, db.ForeignKey('alunos.idAluno'), primary_key=True)
    idTurma = db.Column(db.Integer, db.ForeignKey('turmas.idTurma'), primary_key=True)
    idDisciplina = db.Column(db.Integer, db.ForeignKey('disciplinas.idDisciplina'), primary_key=True)