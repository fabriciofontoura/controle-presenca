// Validação de formulário de agendamento
document.addEventListener('DOMContentLoaded', function() {
    const agendarForm = document.getElementById('agendarForm');
    
    if (agendarForm) {
        agendarForm.addEventListener('submit', function(event) {
            const dataInput = document.getElementById('data');
            const horaInicioInput = document.getElementById('hora_inicio');
            const horaFimInput = document.getElementById('hora_fim');
            
            const data = new Date(dataInput.value);
            const diaSemana = data.getDay();
            
            // Verificar se é dia útil (0=domingo, 6=sábado)
            if (diaSemana === 0 || diaSemana === 6) {
                event.preventDefault();
                alert('Por favor, selecione apenas dias úteis (segunda a sexta-feira).');
                return;
            }
            
            // Verificar se a hora de início é anterior à hora de fim
            if (horaInicioInput.value >= horaFimInput.value) {
                event.preventDefault();
                alert('A hora de início deve ser anterior à hora de fim.');
                return;
            }
            
            // Verificar se o horário está dentro do permitido (7h às 19h)
            const horaInicio = horaInicioInput.value.split(':')[0];
            const horaFim = horaFimInput.value.split(':')[0];
            
            if (horaInicio < 7 || horaFim > 19) {
                event.preventDefault();
                alert('O horário deve estar entre 7h e 19h.');
                return;
            }
        });
    }
    
    // Definir data mínima e máxima para o campo de data
    const dataInput = document.getElementById('data');
    if (dataInput) {
        const hoje = new Date();
        const dataMinima = new Date(2025, 3, 15); // 15 de abril de 2025 (mês é 0-indexed)
        const dataMaxima = new Date(2025, 5, 30); // 30 de junho de 2025
        
        // Usar a data mínima ou a data atual, o que for maior
        const dataInicialEfetiva = hoje > dataMinima ? hoje : dataMinima;
        
        dataInput.min = dataInicialEfetiva.toISOString().split('T')[0];
        dataInput.max = dataMaxima.toISOString().split('T')[0];
        
        // Pré-selecionar a próxima data útil
        let proximaDataUtil = new Date(dataInicialEfetiva);
        const diaSemana = proximaDataUtil.getDay();
        
        // Se for sábado ou domingo, ajustar para a próxima segunda-feira
        if (diaSemana === 0) { // Domingo
            proximaDataUtil.setDate(proximaDataUtil.getDate() + 1);
        } else if (diaSemana === 6) { // Sábado
            proximaDataUtil.setDate(proximaDataUtil.getDate() + 2);
        }
        
        dataInput.value = proximaDataUtil.toISOString().split('T')[0];
    }
});
