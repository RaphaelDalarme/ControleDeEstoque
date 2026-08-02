document.addEventListener("DOMContentLoaded", () => {
    carregarProdutos();

    document.getElementById("form-cadastro").addEventListener("submit", cadastrarProduto);
});

let chartEntradasInstance = null;
let chartSaidasInstance = null;

// 2. Buscar dados e desenhar gráficos do Dashboard (CORRIGIDO)
async function carregarDashboard() {
    try {
        const res = await fetch('/api/dashboard');
        const dados = await res.json();

        const ctxEntradas = document.getElementById('graficoEntradas').getContext('2d');
        const ctxSaidas = document.getElementById('graficoSaidas').getContext('2d');

        // Destrói os gráficos antigos para evitar sobreposição ao atualizar
        if (chartEntradas) chartEntradas.destroy();
        if (chartSaidas) chartSaidas.destroy();

        // Gráfico de Entradas
        chartEntradas = new Chart(ctxEntradas, {
            type: 'bar',
            data: {
                labels: dados.entradas.labela || [], // Corrigido para mapear a propriedade do backend
                datasets: [{
                    label: 'Quantidade Entrada',
                    data: dados.entradas.valores || [],
                    backgroundColor: 'rgba(40, 167, 69, 0.7)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });

        // Gráfico de Saídas
        chartSaidas = new Chart(ctxSaidas, {
            type: 'bar',
            data: {
                labels: dados.saidas.labela || [], // Corrigido para mapear a propriedade do backend
                datasets: [{
                    label: 'Quantidade Saída',
                    data: dados.saidas.valores || [],
                    backgroundColor: 'rgba(220, 53, 69, 0.7)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (erro) {
        console.error("Erro ao carregar o dashboard:", erro);
    }
}

async function cadastrarProduto(evento) {
    evento.preventDefault();

    const nome = document.getElementById("cad-nome").value;
    const quantidade = parseInt(document.getElementById("cad-qtd").value);

    const resposta = await fetch("/produtos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, quantidade })
    });

    if (resposta.ok) {
        document.getElementById("cad-nome").value = "";
        document.getElementById("cad-qtd").value = "";
        carregarProdutos(); // Atualiza a tabela imediatamente!
    } else {
        alert("Erro ao cadastrar produto.");
    }
}

async function excluirProduto(id) {
    if (!confirm(`Deseja realmente excluir o produto ID ${id}?`)) return;

    const resposta = await fetch(`/produtos/${id}`, { method: "DELETE" });

    if (resposta.ok) {
        carregarProdutos(); // Atualiza a tabela
    } else {
        alert("Erro ao excluir produto.");
    }
}