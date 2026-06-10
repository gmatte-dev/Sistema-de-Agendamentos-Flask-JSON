from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  # teu HTML principal



DATA_FILE = os.path.join(os.path.dirname(__file__), 'tarefas.json')


def _carregar_tarefas():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f) or []
    except json.JSONDecodeError:
        return []


def _salvar_tarefas(tarefas):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def _tarefas_por_id(tarefas, task_id):
    for t in tarefas:
        if str(t.get('id')) == str(task_id):
            return t
    return None


@app.get('/api/tarefas')
def api_listar_tarefas():
    return jsonify(_carregar_tarefas())


@app.post('/api/tarefas')
def api_criar_tarefa():
    dados = request.get_json(silent=True) or {}

    nome = dados.get('nome', '').strip()
    data = dados.get('data', '').strip()  # yyyy-mm-dd do input type="date"
    categoria = (dados.get('categoria', '') or 'Outro').strip()
    prioridade = int(dados.get('prioridade', 3))

    if not nome or not data:
        return jsonify({'error': 'nome e data são obrigatórios'}), 400

    # valida formato yyyy-mm-dd
    try:
        datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'data inválida'}), 400

    tarefas = _carregar_tarefas()
    nova = {
        'id': str(dados.get('id') or int(datetime.utcnow().timestamp() * 1000)),
        'nome': nome,
        'data': data,
        'categoria': categoria,
        'prioridade': prioridade
    }

    tarefas.append(nova)
    _salvar_tarefas(tarefas)

    return jsonify(nova), 201


@app.put('/api/tarefas/<task_id>')
def api_atualizar_tarefa(task_id):
    dados = request.get_json(silent=True) or {}

    nome = dados.get('nome', '').strip()
    data = dados.get('data', '').strip()
    categoria = (dados.get('categoria', '') or 'Outro').strip()
    prioridade = int(dados.get('prioridade', 3))

    if not nome or not data:
        return jsonify({'error': 'nome e data são obrigatórios'}), 400

    try:
        datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'data inválida'}), 400

    tarefas = _carregar_tarefas()
    tarefa = _tarefas_por_id(tarefas, task_id)
    if not tarefa:
        return jsonify({'error': 'tarefa não encontrada'}), 404

    tarefa.update({
        'nome': nome,
        'data': data,
        'categoria': categoria,
        'prioridade': prioridade
    })

    _salvar_tarefas(tarefas)
    return jsonify(tarefa)


@app.delete('/api/tarefas/<task_id>')
def api_remover_tarefa(task_id):
    tarefas = _carregar_tarefas()
    nova_lista = [t for t in tarefas if str(t.get('id')) != str(task_id)]

    if len(nova_lista) == len(tarefas):
        return jsonify({'error': 'tarefa não encontrada'}), 404

    _salvar_tarefas(nova_lista)
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(debug=True, port=5050)


