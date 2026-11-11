'use strict';
const form = document.querySelector('#filters');
const number = new Intl.NumberFormat('es-PA');
const money = new Intl.NumberFormat('es-PA', {style:'currency', currency:'USD'});
const colors = ['#294e37','#88996b','#b5be98','#d2bd94','#a2785b','#78908c'];
const charts = {};
const translation = {Clothing:'Ropa', Accessories:'Accesorios', Footwear:'Calzado', Outerwear:'Abrigos', Spring:'Primavera', Summer:'Verano', Fall:'Otoño', Winter:'Invierno', Male:'Masculino', Female:'Femenino'};
const label = value => translation[value] || value;
let page = 1, generation = 0, controller;

async function api(path, signal) {
  const response = await fetch(path, {signal});
  const body = await response.json();
  if (!response.ok) throw new Error(body.error?.message || 'No fue posible consultar los datos.');
  return body;
}

function renderChart(id, records, field, horizontal=false, doughnut=false) {
  const context = document.querySelector(`#${id}`);
  if (charts[id]) charts[id].destroy();
  charts[id] = new Chart(context, {
    type: doughnut ? 'doughnut' : 'bar',
    data: {labels: records.map(r => label(r.label)), datasets: [{
      label: field === 'records' ? 'Registros' : 'Monto USD',
      data: records.map(r => r[field]), backgroundColor: doughnut ? colors : colors[0],
      borderRadius: doughnut ? 0 : 3, borderWidth: 0, maxBarThickness: 32
    }]},
    options: {responsive:true, maintainAspectRatio:false, indexAxis:horizontal?'y':'x',
      plugins:{legend:{display:doughnut,position:'bottom'},tooltip:{callbacks:{label:ctx => field === 'records' ? `${ctx.dataset.label}: ${number.format(ctx.raw)}` : money.format(ctx.raw)}}},
      ...(doughnut ? {cutout:'65%'} : {scales:{x:{beginAtZero:true,grid:{color:'#edf0e8'}},y:{beginAtZero:true,grid:{display:!horizontal}}}})
    }
  });
  // La tabla ofrece los mismos valores a lectores de pantalla y al revisar cifras.
  const table = document.createElement('table');
  for (const row of records) {
    const tr = table.insertRow();
    tr.insertCell().textContent = label(row.label);
    tr.insertCell().textContent = field === 'records' ? number.format(row[field]) : money.format(row[field]);
  }
  document.querySelector(`#${id}-data`).replaceChildren(table);
}

function renderTable(result) {
  const body = document.querySelector('#rows');
  body.replaceChildren();
  for (const row of result.data) {
    const tr = document.createElement('tr');
    for (const value of [row.customer_id,row.item,label(row.category),label(row.season),row.discounted?'Sí':'No',money.format(row.amount_usd)]) {
      const td = document.createElement('td'); td.textContent = value; tr.append(td);
    }
    tr.lastElementChild.className = 'numeric'; body.append(tr);
  }
  if (!result.data.length) {
    const td = document.createElement('td'); td.colSpan=6; td.textContent='No hay registros para estos filtros.';
    const tr = document.createElement('tr'); tr.append(td); body.append(tr);
  }
  document.querySelector('#table-count').textContent = `${number.format(result.total)} registros`;
  document.querySelector('#page-label').textContent = result.pages ? `Página ${result.page} de ${result.pages}` : 'Sin resultados';
  document.querySelector('#prev').disabled = page <= 1;
  document.querySelector('#next').disabled = page >= result.pages;
}

async function refresh() {
  controller?.abort(); controller = new AbortController();
  const signal = controller.signal, current = ++generation;
  const parameters = new URLSearchParams(new FormData(form));
  const suffix = '?' + parameters.toString();
  const status = document.querySelector('#status');
  status.textContent='Actualizando selección…';
  document.querySelector('main').setAttribute('aria-busy','true');
  document.querySelector('#error').hidden=true; document.querySelector('#retry').hidden=true;
  try {
    const [summary,categories,seasons,items,rows] = await Promise.all([
      api('/api/summary'+suffix,signal),api('/api/groups/category'+suffix,signal),
      api('/api/groups/season'+suffix,signal),api('/api/groups/item'+suffix,signal),
      api(`/api/purchases${suffix}&page=${page}&per_page=10`,signal)
    ]);
    if (current !== generation) return;
    document.querySelector('#records').textContent=number.format(summary.records);
    document.querySelector('#total').textContent=money.format(summary.total_amount_usd);
    document.querySelector('#average').textContent=summary.average_amount_usd===null?'—':money.format(summary.average_amount_usd);
    document.querySelector('#rating').textContent=summary.average_rating===null?'—':`${number.format(summary.average_rating)} / 5`;
    renderChart('categories',categories.data,'amount_usd',true);
    renderChart('seasons',seasons.data,'records',false,true);
    renderChart('items',items.data.slice(0,10),'amount_usd',true);
    renderTable(rows);
    status.textContent=`${number.format(summary.records)} registros en la selección · Datos sintéticos`;
  } catch(error) {
    if (error.name === 'AbortError') return;
    document.querySelector('#error').textContent=error.message;
    document.querySelector('#error').hidden=false; document.querySelector('#retry').hidden=false;
    status.textContent='La selección no pudo actualizarse. Los valores anteriores pueden estar desactualizados.';
  } finally {
    if (current === generation) document.querySelector('main').setAttribute('aria-busy','false');
  }
}

async function initialize() {
  try {
    const filters = await api('/api/filters');
    for (const [key,values] of Object.entries(filters)) {
      for (const value of values) {
        const option = document.createElement('option'); option.value=value; option.textContent=label(value);
        document.getElementById(key).append(option);
      }
    }
    const {latest_run:run} = await api('/api/pipeline');
    document.querySelector('#pipeline').textContent = run ? `${number.format(run.row_count)} filas · ${new Date(run.loaded_at).toLocaleString('es-PA',{timeZone:'America/Panama'})} (Panamá) · SHA-256 ${run.sha256.slice(0,12)}…` : 'Sin cargas registradas';
  } catch(error) { document.querySelector('#pipeline').textContent=error.message; }
  await refresh();
}
form.addEventListener('submit',e => e.preventDefault());
form.addEventListener('change',() => {page=1;refresh();});
form.addEventListener('reset',() => {page=1;setTimeout(refresh,0);});
document.querySelector('#prev').addEventListener('click',() => {page--;refresh();});
document.querySelector('#next').addEventListener('click',() => {page++;refresh();});
document.querySelector('#retry').addEventListener('click',refresh);
initialize();
