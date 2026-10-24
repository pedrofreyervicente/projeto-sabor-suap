def editar_registro(lista_turmas, lista_disciplinas, lista_alunos, lista_professores):
    if not lista_turmas:
        print("\nNenhum registro cadastrado.")
        return

    print("\n=== REGISTROS DISPONÍVEIS ===")
    for i in range(len(lista_turmas)):
        print(f"\n[{i + 1}]")
        print(lista_turmas[i])
        print(lista_disciplinas[i])
        print(lista_alunos[i])
        print(lista_professores[i])

    indice = int(input("\nDigite o número do registro que deseja editar: ")) - 1

    if 0 <= indice < len(lista_turmas):
        print(f"\n--- Editando Registro {indice + 1} ---")
        t = Turma(
            input("Digite o NOVO ID da turma:\n"),
            input("Digite o NOVO curso da turma:\n"),
            input("Digite o NOVO ano atual:\n")
        )
        d = Disciplina(
            indice + 1,
            input("Digite a NOVA matéria do professor:\n"),
            turma=t
        )
        a = Aluno(
            input("Digite o NOVO ID do aluno:\n"),
            input("Digite o NOVO nome do aluno:\n"),
            input("Digite a NOVA data de nascimento do aluno:\n"),
            turma=t
        )
        p = Professor(
            id_professor=input("Digite o NOVO ID do professor:\n"),
            nome=input("Digite o NOVO nome do professor:\n"),
            disciplina=d
        )

        lista_turmas[indice] = t
        lista_disciplinas[indice] = d
        lista_alunos[indice] = a
        lista_professores[indice] = p
        print("\nRegistro editado com sucesso!")
    else:
        print("\nOpção inválida.")