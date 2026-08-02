document.getElementById('form-login').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const usuario = document.getElementById('usuario').value;
    const senha = document.getElementById('senha').value;
    const mensagemErro = document.getElementById('mensagem-erro');

    // Validação estática inicial (futuramente validada no backend)
    if (usuario === "admin" && senha === "1234") {
        localStorage.setItem("autenticado", "true");
        window.location.href = "/";
    } else {
        mensagemErro.textContent = "Usuário ou senha incorretos!";
    }
});