<div align="center">
  <h1>Sistema de Controle de Estoque e Dashboard</h1>
  <p>Aplicação web para gerenciamento de estoque, histórico de movimentações, autenticação de usuários e visualização de dados em tempo real.</p>
</div>

<hr>

<h2>Sobre o Projeto</h2>
<p>
  Este projeto é uma aplicação web Full Stack desenvolvida para automatizar e simplificar o controle de inventário. 
  A plataforma conta com sistema de autenticação segura, operações completas de CRUD de produtos, atualizações no histórico de movimentações e um dashboard dinâmico alimentado por análise de dados em tempo real.
</p>

<hr>

<h2>Funcionalidades Principais</h2>
<ul>
  <li><b>Autenticação e Segurança:</b> Sistema de login e sessão de usuário com senhas criptografadas (hashing).</li>
  <li><b>Gerenciamento de Produtos:</b> Cadastro, listagem e remoção de produtos do estoque.</li>
  <li><b>Controle de Movimentação:</b> Adição e baixa de estoque com registro automático de data, hora e tipo de transação.</li>
  <li><b>Dashboard Interativo:</b> Gráficos de barras em tempo real exibindo o total de entradas e saídas por produto.</li>
  <li><b>Alertas Visuais:</b> Identificação automática de produtos com estoque crítico (igual ou inferior a 5 unidades).</li>
  <li><b>Pesquisa em Tempo Real:</b> Filtro dinâmico na tabela de produtos no frontend sem necessidade de recarregar a página.</li>
</ul>

<hr>

<h2>Tecnologias Utilizadas</h2>

<h3>Backend</h3>
<ul>
  <li><b>Python 3:</b> Linguagem principal do projeto.</li>
  <li><b>Flask:</b> Microframework para criação da API RESTful e rotas web.</li>
  <li><b>Flask-Login:</b> Gerenciamento de sessões e autenticação de usuários.</li>
  <li><b>Werkzeug:</b> Criptografia de senhas (generate_password_hash / check_password_hash).</li>
  <li><b>Pandas:</b> Processamento, agrupamento e manipulação dos dados de histórico.</li>
  <li><b>SQLite:</b> Banco de dados relacional para persistência de dados.</li>
</ul>

<h3>Frontend</h3>
<ul>
  <li><b>HTML5 & CSS3:</b> Estruturação e estilização da interface.</li>
  <li><b>Bootstrap 5:</b> Framework CSS para design responsivo e componentes visuais.</li>
  <li><b>JavaScript (ES6+):</b> Consumo das APIs internas (fetch) e manipulação do DOM.</li>
  <li><b>Chart.js:</b> Biblioteca JavaScript para renderização dos gráficos dinâmicos.</li>
</ul>

<hr>

<h2>Estrutura do Banco de Dados</h2>
<p>O banco de dados SQLite (<code>estoque.db</code>) é inicializado automaticamente com a seguinte estrutura:</p>
<ul>
  <li><b>usuarios:</b> Armazena o ID, nome de usuário e a senha criptografada.</li>
  <li><b>produtos:</b> Armazena o ID, nome do produto e a quantidade atual em estoque.</li>
  <li><b>historico:</b> Armazena o registro de cada movimentação (ID, produto_id, tipo, quantidade, data_hora).</li>
</ul>

<hr>

<h2>Como Executar o Projeto</h2>

<h3>Pré-requisitos</h3>
<p>Certifique-se de ter o Python 3.8 ou superior instalado em sua máquina.</p>

<h3>Passo a Passo</h3>
<ol>
  <li>
    <p>Clone o repositório:</p>
    <pre><code>git clone https://github.com/seu-usuario/seu-repositorio.git</code></pre>
  </li>
  <li>
    <p>Acesse a pasta do projeto:</p>
    <pre><code>cd seu-repositorio</code></pre>
  </li>
  <li>
    <p>Instale as dependências necessárias:</p>
    <pre><code>pip install flask flask-login pandas werkzeug</code></pre>
  </li>
  <li>
    <p>Execute a aplicação:</p>
    <pre><code>python app.py</code></pre>
  </li>
  <li>
    <p>Acesse a aplicação no navegador através do endereço:</p>
    <pre><code>http://127.0.0.1:5000/</code></pre>
  </li>
</ol>

<hr>

<h2>Acesso Padrão do Sistema</h2>
<p>Ao executar a aplicação pela primeira vez, o banco de dados criará automaticamente a seguinte conta de administrador:</p>
<ul>
  <li><b>Usuário:</b> <code>admin</code></li>
  <li><b>Senha:</b> <code>123</code></li>
</ul>

<hr>
