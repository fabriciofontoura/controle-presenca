// Funções para controle de carga horária
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar barra de progresso dinamicamente
    const atualizarProgresso = function() {
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            const totalHoras = parseFloat(progressBar.getAttribute('aria-valuenow'));
            const maxHoras = parseFloat(progressBar.getAttribute('aria-valuemax'));
            let progresso = (totalHoras / maxHoras) * 100;
            
            // Limitar a 100%
            if (progresso > 100) {
                progresso = 100;
            }
            
            progressBar.style.width = progresso + '%';
            progressBar.textContent = totalHoras.toFixed(1) + '/' + maxHoras + ' horas';
            
            // Mudar cor baseado no progresso
            if (progresso >= 100) {
                progressBar.classList.remove('bg-success', 'bg-warning', 'bg-danger');
                progressBar.classList.add('bg-success');
            } else if (progresso >= 75) {
                progressBar.classList.remove('bg-success', 'bg-warning', 'bg-danger');
                progressBar.classList.add('bg-success');
            } else if (progresso >= 50) {
                progressBar.classList.remove('bg-success', 'bg-warning', 'bg-danger');
                progressBar.classList.add('bg-warning');
            } else {
                progressBar.classList.remove('bg-success', 'bg-warning', 'bg-danger');
                progressBar.classList.add('bg-danger');
            }
            
            // Mostrar alerta se completou as 20 horas
            if (totalHoras >= maxHoras && !document.querySelector('.alerta-conclusao')) {
                const alertaDiv = document.createElement('div');
                alertaDiv.className = 'alert alert-success mt-3 alerta-conclusao';
                alertaDiv.innerHTML = '<strong>Parabéns!</strong> Você completou a carga horária de 20 horas.';
                
                const progressoDiv = document.querySelector('.progress').parentNode;
                progressoDiv.appendChild(alertaDiv);
            }
        }
    };
    
    // Executar ao carregar a página
    atualizarProgresso();
    
    // Adicionar tooltips para mostrar detalhes de horas
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length > 0) {
        tooltips.forEach(function(tooltip) {
            new bootstrap.Tooltip(tooltip);
        });
    }
});
