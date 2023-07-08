# Indicium Challenge for Data Engineer 

<div align="center">
  <img width="700em" src="https://github.com/gabrielcordeiro2/indicium_challenge/assets/100642061/50e0a18e-49ad-4950-9498-303b0a386d42">
</div>

<div align="center">
  <img height='20' src='https://img.shields.io/github/stars/gabrielcordeiro2/indicium_challenge.svg' />
  <img height='20' src='https://img.shields.io/badge/License-MIT-red.svg' />
  <img height='20' src='https://img.shields.io/github/forks/gabrielcordeiro2/indicium_challenge.svg' />

  [<img height='25' src='https://img.shields.io/badge/LinkedIn-000?style=for-the-badge&logo=linkedin&logoColor=blue' alt='linkedin'>](https://www.linkedin.com/in/gabrielcdev/)
</div>

  

# Alguns detalhes sobre o projeto
- Busquei manter o código em POO e totalmente em inglês, mantendo apenas o README em português.
- Cada task foi projetada para ser idempotente, ou seja, pode-se executar o processo completo em "run_process.py" ou separadamente em cada arquivo específico com o mesmo resultado.
- Fiz um diagrama de fluxo do processo, presente em "fluxo_processo.png".
- Todos os processos são monitorados por um sistema de logs centralizado com suas categorias, presente em "process_monitor.log".
- Criei um armazenamento de execução de cada step diário no arquivo "execution_checker.json"
- Nenhuma credencial sensível de banco é mencionada nos scripts python, elas estão mantidas em um arquivo ".env", Em um ambiente real a melhor prática seria armazenar essas variáveis em um cofre de segredos.
- Não utilizei join para o relacionamento de tabelas em "query_orders.sql" para exemplificar uma query mais performática, mas poderia ter sido utilizado normalmente, a query está localizada em "data/query_orders.sql".
- Fiz uma configuração para que, caso a execução de um processo em uma data específica do passo 1 falhe, você só consiga executa-lo novamente 1 dia depois, de acordo com a data referencial.

# Fluxo do processo

||
|:--:|
|![space-1.jpg](https://github.com/gabrielcordeiro2/indicium_challenge/assets/100642061/7d6db294-6b28-44f6-989c-aeae544691ac)|
Eu fiz esse diagrama usando [draw.io](https://www.drawio.com/).


# Como executar

Abaixo estão alguns passos necessários para executar o projeto com sucesso em seu ambiente.

### Requisitos para executar o projeto

- Python 3.10 (Caso não tenha, instale clicando [aqui](https://www.python.org/downloads/release/python-3100/))
- Git (Caso não tenha, instale clicando [aqui](https://git-scm.com/downloads))
- Docker (Caso não tenha, instale clicando [aqui](https://www.docker.com/products/docker-desktop/))


### Importando o projeto localmente

No terminal do seu sistema operacional, execute os seguinte comandos:
- `git clone https://github.com/gabrielcordeiro2/indicium_challenge.git`
- `cd indicium_challenge/`

### Subindo os bancos de dados do projeto

O projeto contém dois bancos de dados Postgres: um chamado 'northwind', sendo esse uma das fontes de dado, e outro chamado 'final_db' que será o banco onde os dados transformados serão enviados.

Para subir ambos os bancos com Docker, execute o comando abaixo:
- `docker compose up -d`

**OBS:** Caso queira posteriormente destruir os bancos com Docker, execute o comando `docker compose down`

### Criando ambiente virtual e instalando os pacotes

Para criar um ambiente virtual onde os pacotes ficarão encapsulado, execute o comando abaixo no terminal:
- `python -m venv venv`
- `source venv/bin/activate` (Esse comando pode variar de acordo com o sistema operacional)

Agora execute o comando abaixo para instalar os pacotes:
- `pip install -r requirements.txt`

### Executando o pipeline

Ainda no terminal, execute o comando abaixo para rodar o pipeline completo:
- `python run_process.py`

**(Opcional):** Caso queira executar os processos separadamente de maneira idempotente, execute o comando abaixo, o processo especifico pode ser encontrado no [Fluxo do processo](https://github.com/gabrielcordeiro2/indicium_challenge/assets/100642061/7d6db294-6b28-44f6-989c-aeae544691ac):
- `python nome-do-arquivo.py`

<br>
<br>

Agradeço a atenção, espero que gostem do projeto :)

<div align="left">
  <img height="300em" src="https://github.com/gabrielcordeiro2/indicium_challenge/assets/100642061/df9ed575-f5c3-44ce-b83d-63e618e1a4ed">
</div>


