from database import db
from sqlalchemy import select, and_
from models import Turmas, Alunos, RelacionamentoAluno, RelacionamentoTurma, RelacionamentoProfessor, Disciplinas, Professores, Notas

class DetalheTurma ():
    def __init__(self, idTurma):
        self.idTurma = idTurma
        self.relAlunos = RelacionamentoAluno()
        self.relDisciplinas = RelacionamentoTurma()
        self.relProfessores = RelacionamentoProfessor()


    def getTurma(self):
        return db.get_or_404(Turmas, self.idTurma)

    def getAlunos(self, idDisciplina=None):
        if idDisciplina is None:
            stmt = (
                select(Alunos)
                .join(RelacionamentoAluno, Alunos.idAluno == RelacionamentoAluno.idAluno)
                .where(RelacionamentoAluno.idTurma == self.idTurma)
                .distinct()
                .order_by(Alunos.nome)
            )
            return db.session.scalars(stmt).all()

        stmt = (
            select(Alunos, Notas.nota)
            .join(RelacionamentoAluno, Alunos.idAluno == RelacionamentoAluno.idAluno)
            .outerjoin(
                Notas,
                and_(
                    Notas.idAluno == Alunos.idAluno,
                    Notas.idDisciplina == idDisciplina,
                ),
            )
            .where(RelacionamentoAluno.idTurma == self.idTurma)
            .distinct()
            .order_by(Alunos.nome)
        )

        alunos = []
        for aluno, nota in db.session.execute(stmt).all():
            if nota:
                aluno.nota = nota
            else:
                aluno.none = ''
            alunos.append(aluno)
        return alunos

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

    def getDadosTurma(self, idDisciplina=None):
        alunos = self.getAlunos(idDisciplina)
        disciplinas = self.getDisciplinas()
        return {
            "turma": self.getTurma(),
            "alunos": alunos,
            "quantidadeAlunos": len(alunos),
            "disciplinas": disciplinas,
            "quantidadeDisciplinas": len({d.idDisciplina for d in disciplinas}),
            "quantidadeProfessores": len({d.idProfessor for d in disciplinas})
        }