let tarefas = [];

async function carregarTarefas() {
  try {
    const res = await fetch('/api/tarefas');
    if (!res.ok) throw new Error('Falha ao carregar tarefas');
    tarefas = await res.json();
    renderizarTarefas(menuUrgentes.classList.contains('active'));
    if (viewDashboard && !viewDashboard.classList.contains('hidden')) {
      calcularResumos();
    }
  } catch (e) {
    console.error(e);
  }
}


const menuTodas = document.getElementById('menu-todas');
const menuUrgentes = document.getElementById('menu-urgentes');
const menuAdd = document.getElementById('menu-add');
const menuResumo = document.getElementById('menu-resumo');

const viewForm = document.getElementById('view-form');
const viewList = document.getElementById('view-list');
const viewDashboard = document.getElementById('view-dashboard');

const formTitle = document.getElementById('form-title');
const btnSubmitText = document.getElementById('btn-submit-text');
const taskIdInput = document.getElementById('task-id');
const listTitle = document.getElementById('list-title');
const taskContainer = document.getElementById('task-container');
const todoForm = document.getElementById('todo-form');

function alternarAba(abaAtiva) {
  [menuTodas, menuUrgentes, menuAdd, menuResumo].forEach(aba => aba.classList.remove('active'));
  abaAtiva.classList.add('active');
}

function esconderTodasViews() {
  viewForm.classList.add('hidden');
  viewList.classList.add('hidden');
  viewDashboard.classList.add('hidden');
}

function obterDataSemHora(dataString) {
  if (!dataString) return new Date();
  const partes = dataString.split('-');
  return new Date(partes[0], partes[1] - 1, partes[2]);
}

function renderizarTarefas(filtrarPorUrgente = false) {
  taskContainer.innerHTML = '';
  const tarefasFiltradas = filtrarPorUrgente
    ? tarefas.filter(t => t.prioridade === '1' || t.prioridade === '2')
    : tarefas;

  if (tarefasFiltradas.length === 0) {
    taskContainer.innerHTML = `<li class="empty-state">Nenhuma tarefa encontrada.</li>`;
    return;
  }

  tarefasFiltradas.forEach(tarefa => {
    const li = document.createElement('li');
    li.className = 'task-item';

    let badgeClass = 'badge-normal';
    let badgeText = 'Não Urgente';
    if (tarefa.prioridade === '1') {
      badgeClass = 'badge-muito-urgente';
      badgeText = 'Muito Urgente';
    } else if (tarefa.prioridade === '2') {
      badgeClass = 'badge-urgente';
      badgeText = 'Urgente';
    }

    const dataFormatada = tarefa.data.split('-').reverse().join('/');

    li.innerHTML = `
                <div class="task-info">
                    <h4>${tarefa.nome} <span class="badge ${badgeClass}">${badgeText}</span></h4>
                    <div class="task-meta">
                        <span>📅 ${dataFormatada}</span>
                        ${tarefa.categoria ? `<span>📁 ${tarefa.categoria}</span>` : ''}
                    </div>
                </div>
                <div class="task-actions">
                    <button class="btn-inline btn-edit" onclick="editarTarefa('${tarefa.id}')">Editar</button>
                    <button class="btn-inline btn-delete" onclick="removerTarefa('${tarefa.id}')">Remover</button>
                </div>
            `;
    taskContainer.appendChild(li);
  });
}

function calcularResumos() {
  const total = tarefas.length;

  const hojeData = new Date();
  hojeData.setHours(0, 0, 0, 0);

  let atrasadas = 0;
  let hoje = 0;
  let futuras = 0;
  let urgentes = 0;

  let catEscola = 0, catTrabalho = 0, catPessoal = 0, catOutro = 0;

  tarefas.forEach(t => {
    const tData = obterDataSemHora(t.data);
    tData.setHours(0, 0, 0, 0);

    if (tData.getTime() < hojeData.getTime()) {
      atrasadas++;
    } else if (tData.getTime() === hojeData.getTime()) {
      hoje++;
    } else {
      futuras++;
    }

    if (t.prioridade === '1' || t.prioridade === '2') {
      urgentes++;
    }

    const cat = t.categoria.trim().toLowerCase();
    if (cat === 'escola') catEscola++;
    else if (cat === 'trabalho') catTrabalho++;
    else if (cat === 'pessoal') catPessoal++;
    else catOutro++;
  });

  document.getElementById('count-total').textContent = total;
  document.getElementById('count-atrasadas').textContent = atrasadas;
  document.getElementById('count-hoje').textContent = hoje;
  document.getElementById('count-futuras').textContent = futuras;
  document.getElementById('count-urgentes').textContent = urgentes;

  const taxaAtraso = total > 0 ? Math.round((atrasadas / total) * 100) : 0;
  document.getElementById('delay-bar').style.width = `${taxaAtraso}%`;
  document.getElementById('delay-text').textContent = `${taxaAtraso}%`;

  const maxCat = Math.max(catEscola, catTrabalho, catPessoal, catOutro, 1);

  document.getElementById('bar-escola').style.width = `${(catEscola / maxCat) * 100}%`;
  document.getElementById('bar-trabalho').style.width = `${(catTrabalho / maxCat) * 100}%`;
  document.getElementById('bar-pessoal').style.width = `${(catPessoal / maxCat) * 100}%`;
  document.getElementById('bar-outro').style.width = `${(catOutro / maxCat) * 100}%`;

  document.getElementById('val-escola').textContent = `${catEscola} ${catEscola === 1 ? 'tarefa' : 'tarefas'}`;
  document.getElementById('val-trabalho').textContent = `${catTrabalho} ${catTrabalho === 1 ? 'tarefa' : 'tarefas'}`;
  document.getElementById('val-pessoal').textContent = `${catPessoal} ${catPessoal === 1 ? 'tarefa' : 'tarefas'}`;
  document.getElementById('val-outro').textContent = `${catOutro} ${catOutro === 1 ? 'tarefa' : 'tarefas'}`;
}

function editarTarefa(id) {
  const tarefa = tarefas.find(t => t.id === id);
  if (!tarefa) return;

  formTitle.textContent = "Editar tarefa";
  btnSubmitText.innerHTML = "<span>✓</span> Salvar Alterações";

  taskIdInput.value = tarefa.id;
  document.getElementById('nome').value = tarefa.nome;
  document.getElementById('data').value = tarefa.data;
  document.getElementById('categoria').value = tarefa.categoria;
  document.getElementById('prioridade').value = tarefa.prioridade;

  alternarAba(menuAdd);
  esconderTodasViews();
  viewForm.classList.remove('hidden');
}

async function removerTarefa(id) {
  try {
    const res = await fetch(`/api/tarefas/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Falha ao remover tarefa');
    await carregarTarefas();
    renderizarTarefas(menuUrgentes.classList.contains('active'));
  } catch (err) {
    alert(err.message || 'Erro ao remover');
    console.error(err);
  }
}


menuAdd.addEventListener('click', () => {
  alternarAba(menuAdd);
  esconderTodasViews();
  formTitle.textContent = "Adicionar tarefa";
  btnSubmitText.innerHTML = "<span>✓</span> Adicionar";
  taskIdInput.value = "";
  todoForm.reset();
  viewForm.classList.remove('hidden');
});

menuTodas.addEventListener('click', () => {
  alternarAba(menuTodas);
  listTitle.textContent = 'Todas Tarefas';
  esconderTodasViews();
  viewList.classList.remove('hidden');
  renderizarTarefas(false);
});

menuUrgentes.addEventListener('click', () => {
  alternarAba(menuUrgentes);
  listTitle.textContent = 'Tarefas Urgentes';
  esconderTodasViews();
  viewList.classList.remove('hidden');
  renderizarTarefas(true);
});

menuResumo.addEventListener('click', async () => {
  alternarAba(menuResumo);
  esconderTodasViews();
  viewDashboard.classList.remove('hidden');
  calcularResumos();
});


document.getElementById('btn-reset-act').addEventListener('click', () => {
  formTitle.textContent = "Adicionar tarefa";
  btnSubmitText.innerHTML = "<span>✓</span> Adicionar";
  taskIdInput.value = "";
});

todoForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const idAtual = taskIdInput.value;
  const dadosTarefa = {
    nome: document.getElementById('nome').value,
    data: document.getElementById('data').value,
    categoria: document.getElementById('categoria').value || 'Outro',
    prioridade: document.getElementById('prioridade').value
  };

  try {
    if (idAtual) {
      const res = await fetch(`/api/tarefas/${idAtual}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dadosTarefa)
      });
      if (!res.ok) throw new Error('Falha ao editar tarefa');
    } else {
      const res = await fetch('/api/tarefas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dadosTarefa)
      });
      if (!res.ok) throw new Error('Falha ao adicionar tarefa');
    }

    todoForm.reset();
    taskIdInput.value = "";
    await carregarTarefas();
    menuTodas.click();
  } catch (err) {
    alert(err.message || 'Erro ao salvar tarefa');
    console.error(err);
  }
});


// Carrega as tarefas do servidor quando a página abrir
carregarTarefas();

// Exportação CSV
document.getElementById('btn-export-csv').addEventListener('click', () => {

  if (tarefas.length === 0) {
    alert('Não há tarefas cadastradas para exportar.');
    return;
  }

  const cabecalhos = ['Nome da Tarefa', 'Data', 'Categoria', 'Prioridade'];

  const linhas = tarefas.map(t => {
    let prioridadeTexto = 'Não Urgente';
    if (t.prioridade === '1') prioridadeTexto = 'Muito Urgente';
    else if (t.prioridade === '2') prioridadeTexto = 'Urgente';

    const dataFormatada = t.data.split('-').reverse().join('/');
    const nomeEscapado = t.nome.replace(/"/g, '""');
    const categoriaEscapada = t.categoria.replace(/"/g, '""');

    return `"${nomeEscapado}";"${dataFormatada}";"${categoriaEscapada}";"${prioridadeTexto}"`;
  });

  const conteudoCsv = [cabecalhos.join(';'), ...linhas].join('\n');
  const blob = new Blob(['\uFEFF' + conteudoCsv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const linkProvisorio = document.createElement('a');

  linkProvisorio.setAttribute('href', url);
  linkProvisorio.setAttribute('download', `organizador_tarefas_${Date.now()}.csv`);
  linkProvisorio.style.visibility = 'hidden';

  document.body.appendChild(linkProvisorio);
  linkProvisorio.click();
  document.body.removeChild(linkProvisorio);
});