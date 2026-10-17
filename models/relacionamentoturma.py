from database import db

class RelacionamentoTurma(db.Model):
    __tablename__ = 'relacionamentoturma'
    
    id = db.Column(db.Integer, primary_key=True)
    idTurma = db.Column(db.Integer, nullable=True)
    idDisciplina = db.Column(db.Integer, nullable=True)
    

