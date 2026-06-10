# Persistência JSON (tarefas.json)

Este projeto usa um arquivo `tarefas.json` como “banco de dados” simples.

- `GET /api/tarefas` retorna todas as tarefas.
- `POST /api/tarefas` cria uma tarefa.
- `PUT /api/tarefas/<id>` atualiza uma tarefa.
- `DELETE /api/tarefas/<id>` remove uma tarefa.

O front-end (`static/js/script.js`) chama essas rotas.

