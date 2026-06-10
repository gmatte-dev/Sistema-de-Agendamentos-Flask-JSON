# Sistema de Agendamentos (Flask + JSON)

Projeto web para organizar tarefas com CRUD via API e persistência em `tarefas.json`.

## Como rodar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Inicie o servidor:
```bash
python app.py
```

3. Acesse no navegador:
- `http://localhost:5050/`

## Rotas da API

- `GET /api/tarefas` → lista todas as tarefas
- `POST /api/tarefas` → cria tarefa
- `PUT /api/tarefas/<id>` → atualiza tarefa
- `DELETE /api/tarefas/<id>` → remove tarefa

## Dados (persistência)

- As tarefas ficam em `tarefas.json` na raiz do projeto.
- O backend cria o arquivo automaticamente se ele não existir.

## Observação sobre o arquivo `SistemaDeAgendamentos.py`

Esse arquivo contém uma versão em console do sistema. Ele não é usado pela aplicação Flask.

