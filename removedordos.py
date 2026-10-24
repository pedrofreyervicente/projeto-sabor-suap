def remover_registro(lista_turmas, lista_disciplinas, lista_alunos, lista_professores):
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

    indice = int(input("\nDigite o número do registro que deseja remover: ")) - 1

    if 0 <= indice < len(lista_turmas):
        lista_turmas.pop(indice)
        lista_disciplinas.pop(indice)
        lista_alunos.pop(indice)
        lista_professores.pop(indice)
        print("\nRegistro removido com sucesso!")
    else:
        print("\nOpção inválida.")