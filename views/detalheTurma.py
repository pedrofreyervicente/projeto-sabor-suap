from database import db
from sqlalchemy import select
from models import Turmas, Alunos, RelacionamentoAluno, RelacionamentoTurma, RelacionamentoProfessor, Disciplinas, Professores

class DetalheTurma ():
    def __init__(self, idTurma):
        self.idTurma = idTurma
        self.relAlunos = RelacionamentoAluno()
        self.relDisciplinas = RelacionamentoTurma()
        self.relProfessores = RelacionamentoProfessor()


    def getTurma(self):
        return db.get_or_404(Turmas, self.idTurma)

    def getAlunos(self):
        stmt = (
            select(Alunos)
            .join(RelacionamentoAluno, Alunos.idAluno == RelacionamentoAluno.idAluno)
            .where(RelacionamentoAluno.idTurma == self.idTurma)
            .distinct()
        )
        return db.session.scalars(stmt).all()

    def getDisciplinas(self):
        stmt = (
        select(
            RelacionamentoProfessor.idTurma,
            Disciplinas.idDisciplina,
            Disciplinas.nome.label("disciplina"),
            Professores.idProfessor,
            Professores.nome.label("professor"),
        )
        .select_from(RelacionamentoProfessor)
        .join(Disciplinas, Disciplinas.idDisciplina == RelacionamentoProfessor.idDisciplina)
        .join(Professores, Professores.idProfessor == RelacionamentoProfessor.idProfessor)
        .where(RelacionamentoProfessor.idTurma == self.idTurma)
        .order_by(Disciplinas.nome)
        )
        return db.session.execute(stmt).all()

    def getDadosTurma(self):
        alunos = self.getAlunos()
        return {
            "turma": self.getTurma(),
            "alunos": alunos,
            "quantidadeAlunos": len(alunos),
            "disciplinas": self.getDisciplinas(),
            "quantidadeDisciplinas": len(self.getDisciplinas())
        }