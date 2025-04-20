// Funções para o dashboard do responsável
document.addEventListener('DOMContentLoaded', function() {
    // Filtrar agendamentos por status
    const filtroStatus = document.getElementById('filtroStatus');
    if (filtroStatus) {
        filtroStatus.addEventListener('change', function() {
            const status = this.value;
            const linhasAgendamento = document.querySelectorAll('.agendamento-row');
            
            linhasAgendamento.forEach(function(linha) {
                if (status === 'todos' || linha.dataset.status === status) {
                    linha.style.display = '';
                } else {
                    linha.style.display = 'none';
                }
            });
        });
    }
    
    // Filtrar agendamentos por aluno
    const filtroAluno = document.getElementById('filtroAluno');
    if (filtroAluno) {
        filtroAluno.addEventListener('change', function() {
            const alunoId = this.value;
            const linhasAgendamento = document.querySelectorAll('.agendamento-row');
            
            linhasAgendamento.forEach(function(linha) {
                if (alunoId === 'todos' || linha.dataset.alunoId === alunoId) {
                    linha.style.display = '';
                } else {
                    linha.style.display = 'none';
                }
            });
        });
    }
    
    // Filtrar agendamentos por data
    const filtroData = document.getElementById('filtroData');
    if (filtroData) {
        filtroData.addEventListener('change', function() {
            const data = this.value;
            const linhasAgendamento = document.querySelectorAll('.agendamento-row');
            
            if (data === '') {
                linhasAgendamento.forEach(function(linha) {
                    linha.style.display = '';
                });
                return;
            }
            
            linhasAgendamento.forEach(function(linha) {
                if (linha.dataset.data === data) {
                    linha.style.display = '';
                } else {
                    linha.style.display = 'none';
                }
            });
        });
    }
    
    // Confirmar ações de aprovação/rejeição/conclusão
    const botoesAprovar = document.querySelectorAll('.btn-aprovar');
    const botoesRejeitar = document.querySelectorAll('.btn-rejeitar');
    const botoesConcluir = document.querySelectorAll('.btn-concluir');
    
    botoesAprovar.forEach(function(botao) {
        botao.addEventListener('click', function(event) {
            if (!confirm('Confirmar aprovação deste agendamento?')) {
                event.preventDefault();
            }
        });
    });
    
    botoesRejeitar.forEach(function(botao) {
        botao.addEventListener('click', function(event) {
            if (!confirm('Confirmar rejeição deste agendamento?')) {
                event.preventDefault();
            }
        });
    });
    
    botoesConcluir.forEach(function(botao) {
        botao.addEventListener('click', function(event) {
            if (!confirm('Confirmar conclusão deste agendamento? Isso adicionará as horas ao total do aluno.')) {
                event.preventDefault();
            }
        });
    });
});
