$(document).ready(function () {
    $('#form-notas').on('submit', function (e) {
        e.preventDefault();

        const idTurma = $('input[name="idTurma"]').val();
        const idDisciplina = $('input[name="idDisciplina"]').val();
        const idProfessor = $('input[name="idProfessor"]').val();

        const notas = {};
        $('.input-nota').each(function () {
            const alunoId = $(this).data('aluno-id');
            const valorNota = $(this).val();
            
            if (valorNota !== '') {
                notas[alunoId] = valorNota;
            }
        });

        const dados = {
            idTurma: idTurma,
            idDisciplina: idDisciplina,
            idProfessor: idProfessor,
            notas: notas,
        };

        $.ajax({
            url: '/notas/salva-nota',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dados),
            success: function (response) {
                console.log('Resposta do servidor:', response);
            },
            error: function (xhr, status, error) {
                alert('Erro ao salvar as notas.');
                console.error(error);
            }
        });
    });
});