function switchProducaoTab(t){document.querySelectorAll('.producao-tab-content').forEach(c=>c.style.display='none');const e=document.getElementById(t);if(e)e.style.display='block'}
function abrirModalPallet(){const m=document.getElementById('modalNovoPallet');if(m)m.style.display='flex'}
function loadProducao(){console.log("Carga OK")}
function goTo(p){if(p==='producao')loadProducao()}
type fix.js >> gelocrim_v1.html

