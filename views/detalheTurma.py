from database import db
from sqlalchemy import select, and_, func
from models import Turmas, Alunos, RelacionamentoAluno, RelacionamentoTurma, RelacionamentoProfessor, Disciplinas, Professores, Notas

class DetalheTurma():
    def __init__(self, idTurma):
        self.idTurma = idTurma

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
            aluno.nota = nota if nota is not None else ''
            alunos.append(aluno)
        return alunos

    def getDisciplinas(self):
        stmt = (
            select(
                RelacionamentoTurma.idTurma,
                Disciplinas.idDisciplina,
                Disciplinas.nome.label("disciplina"),
                Professores.idProfessor,
                func.coalesce(Professores.nome, "Sem professor").label("professor")
            )
            .select_from(RelacionamentoTurma)
            .join(Disciplinas, Disciplinas.idDisciplina == RelacionamentoTurma.idDisciplina)
            .outerjoin(
                RelacionamentoProfessor,
                and_(
                    RelacionamentoProfessor.idTurma == self.idTurma,
                    RelacionamentoProfessor.idDisciplina == Disciplinas.idDisciplina
                )
            )
            .outerjoin(Professores, Professores.idProfessor == RelacionamentoProfessor.idProfessor)
            .where(RelacionamentoTurma.idTurma == self.idTurma)
            .distinct()
            .order_by(Disciplinas.nome)
        )
        return db.session.execute(stmt).all()

    def getDadosTurma(self, idDisciplina=None):
        alunos = self.getAlunos(idDisciplina)
        disciplinas = self.getDisciplinas()
        
        professores_ids = {d.idProfessor for d in disciplinas if d.idProfessor is not None}
        
        return {
            "turma": self.getTurma(),
            "alunos": alunos,
            "quantidadeAlunos": len(alunos),
            "disciplinas": disciplinas,
            "quantidadeDisciplinas": len({d.idDisciplina for d in disciplinas}),
            "quantidadeProfessores": len(professores_ids)
        }