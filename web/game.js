/* The route is declarative; observations and XP are decided by the server. */
const $ = (s, root = document) => root.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let game, boot, selected, zone, step = 0, busy = false, connected = false, riskClient = 0, riskStep = 0, riskDraft = {};
let accessMode='novnc';try{accessMode=localStorage.getItem('vulncorp-access-mode')==='ssh'?'ssh':'novnc';}catch(error){}
const stationNames = {analyst:'Puesto de análisis',ops:'Estación de soporte',appdesk:'Estación de aplicaciones'};
const api = async (url, data) => {
  const r = await fetch(url, data === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const value = await r.json(); if (!r.ok || value.error) throw Error(value.error || 'No se pudo completar la solicitud.'); return value;
};
function toast(text) { $('#toast').textContent = text; $('#toast').hidden = false; clearTimeout(toast.timer); toast.timer = setTimeout(() => $('#toast').hidden = true, 6500); }
function challenge() { return game.catalog.challenges.find(c => c.id === selected); }
function runRecords(kind) { return (boot.records[kind] || []).filter(x => x.game_run === game.run.id || (!('game_run' in x) && x.occurred_at >= game.run.started)); }
function primary(text, action, extra = '') { return `<button class="primary" data-action="${action}" ${extra}>${text}</button>`; }
function choose(id) { selected = id; zone = challenge().zone; step = 0; riskStep = 0; riskDraft = {}; render(); }
function render() {
  $('#xp-value').textContent = game.xp; $('#progress-label').textContent = `${game.completed} de ${game.total} objetivos`;
  $('#progress-fill').style.width = `${100 * game.completed / game.total}%`;
  $('#zones').innerHTML = game.catalog.zones.map((z,i) => `<button class="zone-tab ${zone===z.id?'active':''}" data-zone="${z.id}" aria-current="${zone===z.id?'step':'false'}"><span class="zone-number">${String(i+1).padStart(2,'0')}</span>${esc(z.short)}${game.catalog.challenges.filter(c=>c.zone===z.id).every(c=>game.states[c.id]==='locked')?'<span class="zone-lock" aria-label="Bloqueada">○</span>':''}</button>`).join('');
  const levels = game.catalog.challenges.filter(c => c.zone === zone);
  $('#zone-count').textContent = `${levels.filter(c=>game.states[c.id]==='done').length} / ${levels.length}`;
  $('#levels').innerHTML = levels.map((c,i) => `<button class="level ${game.states[c.id]} ${selected===c.id?'selected':''}" data-level="${c.id}" ${selected===c.id?'aria-current="step"':''}><span class="level-marker" aria-hidden="true">${game.states[c.id]==='done'?'✓':String(i+1).padStart(2,'0')}</span><span class="level-title">${esc(c.title)}<span class="level-label">${game.states[c.id]==='done'?'Comprobado':game.states[c.id]==='locked'?'Por desbloquear':`${c.xp} PX · En curso`}</span></span></button>`).join('');
  renderQuest();
}
function stationArt() {
  return `<div class="station-art" aria-hidden="true"><svg viewBox="0 0 250 180"><ellipse cx="132" cy="159" rx="96" ry="12" fill="#d9d5e2"/><path d="M112 111h30v28l24 10v6h-76v-6l22-10z" fill="#b8b1c9" stroke="#9990af"/><path d="M122 113h20v26l24 10h-18l-26-10z" fill="#a79ebc"/><rect x="35" y="18" width="181" height="108" rx="9" fill="#f9f8fc" stroke="#a69cb9" stroke-width="2"/><rect x="44" y="27" width="163" height="89" rx="4" fill="#e6e9f0"/><rect x="56" y="39" width="139" height="65" rx="4" fill="#fff" stroke="#c7cbd6"/><path d="M56 51h139" stroke="#d7dae2"/><circle cx="63" cy="45" r="2" fill="#c2b8d8"/><circle cx="70" cy="45" r="2" fill="#d1cadf"/><path d="m68 65 6 5-6 5m12 0h13" fill="none" stroke="#78629f" stroke-width="2" stroke-linecap="round"/><path d="M69 86h78m-78 6h48" stroke="#c8ced8" stroke-width="3" stroke-linecap="round"/><path d="m67 153 116 0 16 14H51z" fill="#faf9fc" stroke="#b8b1c9"/><path d="M72 158h107m-114 5h121" stroke="#d1ccdd"/><rect x="212" y="137" width="17" height="27" rx="8" fill="#faf9fc" stroke="#b8b1c9"/><path d="M220.5 141v6" stroke="#b8b1c9"/></svg></div>`;
}
function hints(c) { return `<details><summary class="hint-toggle">Necesito una pista</summary><div class="hints">${c.hints.map(h=>`<p>${esc(h)}</p>`).join('')}</div></details>`; }
function checksHTML(c) {
  const award = game.awards.find(a=>a.challenge_id===c.id);
  const feedback = game.feedback?.challenge_id===c.id ? game.feedback : null;
  const checks = award?.checks || feedback?.checks;
  return checks ? checks.map(x=>`<div class="objective ${x.ok?'ok':''}"><span class="objective-dot" aria-hidden="true">${x.ok?'✓':''}</span><span>${esc(x.label)}</span></div>`).join('') : `<div class="objective"><span class="objective-dot" aria-hidden="true"></span><span>La estación y los servicios registrarán tus pruebas al ejecutarlas.</span></div>`;
}
function renderQuest() {
  const c = challenge(), z = game.catalog.zones.find(z=>z.id===c.zone), state = game.states[c.id];
  const index = game.catalog.challenges.filter(x=>x.zone===c.zone).findIndex(x=>x.id===c.id)+1;
  let body;
  if (state === 'locked') body = `<div class="locked-panel"><h2>Primero, la evidencia anterior</h2><p>Este desafío se abre al comprobar «${esc(game.catalog.challenges.find(x=>x.id===c.requires[0])?.title || 'el objetivo anterior')}».</p>${primary('Volver al objetivo activo','current')}</div>`;
  else if (state === 'done') body = `<div class="success-panel"><span class="complete-mark" aria-hidden="true">✓</span><h2>Objetivo comprobado</h2><p>+${c.xp} PX de práctica. Tu evidencia quedó en el cuaderno.</p>${game.current?primary('Continuar el recorrido →','current'):primary('Ver mi expediente','notebook')}</div><div class="objectives">${checksHTML(c)}</div>${!game.current?'<p class="muted">Has cerrado este tramo de Operación continuidad. El caso puede extenderse con nuevas zonas y desafíos.</p>':''}`;
  else body = `${c.steps.length?taskHTML(c):''}<div id="challenge-form">${c.form?formHTML(c):''}</div><div id="quest-checks" class="objectives" aria-live="polite">${checksHTML(c)}</div><div class="task-tools">${hints(c)}<p id="verification-note">La evidencia se comprueba automáticamente.</p></div>`;
  $('#quest').innerHTML = `<div class="quest-frame"><div class="quest-top"><span class="kicker">${esc(z.short.toUpperCase())} / OBJETIVO ${String(index).padStart(2,'0')}</span><span class="reward">✧ ${c.xp} PX</span></div><h1>${esc(c.title)}</h1><p class="quest-brief">${esc(c.brief)}</p>${body}</div>`;
  wireForms(); if (!$('#workspace').hidden) renderGuide();
}
function sshSteps(c) {
  const s=c.steps[step];
  return `<div class="guide-step-counter">PASO ${step+1} DE ${c.steps.length}</div><div class="guide-location">${esc(s.where)}</div><pre>${esc(s.command)}</pre><p class="step-reason">${esc(s.why)}</p><button class="secondary" data-action="copy-step">Copiar comando del paso</button><div class="step-navigation"><button class="quiet-button" data-action="step-back" ${step===0?'disabled':''}>← Anterior</button><button class="quiet-button" data-action="step-next" ${step===c.steps.length-1?'disabled':''}>Siguiente paso →</button></div>`;
}
function taskHTML(c) {
  if(accessMode==='ssh')return `<section class="form-card ssh-task"><span class="station-tag">TU TERMINAL · LA MISMA CAMPAÑA</span><h3>Guía para ${esc(stationNames[c.station].toLowerCase())}</h3><p>Ejecuta cada paso dentro del puesto indicado. La conexión SSH inicial siempre entra a análisis.${c.station!=='analyst'?` Si abriste una sesión nueva, continúa con <code>ssh ${esc(c.station)}</code>; sal primero de otro puesto con <code>exit</code>.`:' Si estás en otro puesto, vuelve con exit.'}</p><div id="ssh-steps">${sshSteps(c)}</div><div class="ssh-task-links"><button class="quiet-button" data-action="ssh-access">Acceso y llaves SSH</button><button class="quiet-button" data-action="desk">Usar escritorio noVNC</button></div></section>`;
  return `<div class="task-scene"><div><span class="station-tag">LINUX REAL · RED DE LA EMPRESA</span><h3>${esc(stationNames[c.station])}</h3><p>Entra al escritorio. La guía te acompaña mientras investigas en la terminal.</p>${primary('Entrar al puesto →','desk')}<button class="quiet-button access-alternative" data-action="ssh-access">Conectar por SSH</button></div>${stationArt()}</div>`;
}
function setAccessMode(mode){accessMode=mode;try{localStorage.setItem('vulncorp-access-mode',mode);}catch(error){}}
function refreshSteps(){if($('#ssh-steps'))$('#ssh-steps').innerHTML=sshSteps(challenge());if(!$('#workspace').hidden)renderGuide();}
function evidenceOptions(predicate = ()=>true) {
  return [...new Map(runRecords('evidence').filter(predicate).map(x=>[x.actor+':'+x.action+':'+x.result.status,x])).values()].map(x=>`<label class="evidence-option"><input type="checkbox" name="evidence" value="${esc(x.id)}">${esc(x.action)} · HTTP ${x.result.status} · ${esc(stationNames[x.actor]||x.actor)}<small>${esc(x.id)}</small></label>`).join('') || '<p class="muted">Aún no hay pruebas de esta campaña. Ejecuta las comprobaciones en la estación y vuelve aquí.</p>';
}
function evidenceFilter(kind) {
  return x => x.actor==='analyst' && (kind==='export' ? x.action==='export'&&x.result.status===200 : ['export','transaction'].includes(x.action) && (kind!=='residual' || x.occurred_at >= (runRecords('station').filter(p=>p.action==='proteger').at(-1)?.occurred_at || Infinity)));
}
function refreshEvidencePicker() {
  const picker=$('[data-evidence-picker]'); if(!picker)return;
  const checked=[...picker.querySelectorAll('input:checked')].map(input=>({id:input.value,label:input.closest('label').outerHTML}));
  const next=document.createElement('div');next.innerHTML=evidenceOptions(evidenceFilter(picker.dataset.evidencePicker));
  for(const item of checked) if(![...next.querySelectorAll('input')].some(x=>x.value===item.id))next.insertAdjacentHTML('beforeend',item.label);
  if([...picker.querySelectorAll('input')].map(x=>x.value).join('|')===[...next.querySelectorAll('input')].map(x=>x.value).join('|'))return;
  picker.replaceChildren(...next.childNodes);
  for(const input of picker.querySelectorAll('input'))input.checked=checked.some(x=>x.id===input.value);
}
const reason = (label='Fundamento y límites de tu conclusión') => `<label>${label}<textarea name="reason" required minlength="40" maxlength="4000" placeholder="Relaciona lo observado con tu conclusión. Explica qué falta por demostrar."></textarea></label>`;
const select = (name,label,options) => `<label>${label}<select name="${name}" required><option value="">Elige una conclusión…</option>${options.map(([v,t])=>`<option value="${v}">${esc(t)}</option>`).join('')}</select></label>`;
function formHTML(c) {
  if(c.form==='advanced')return AdvancedUI.render(c);
  if (c.form==='proveedor') return `<form class="form-card" id="analysis-form"><h3>Contrasta el reporte</h3><p>F-01: records · Django 3.2 · CVE-2021-35042.<br>VENDOR-06: records · Django 3.2 · misma CVE.<br>VENDOR-07: mission · requests 2.31.0.</p>${select('duplicate','¿Qué registro duplica F-01?',[['VENDOR-06','VENDOR-06'],['VENDOR-07','VENDOR-07']])}${select('misattributed','¿Qué registro atribuye el componente al activo equivocado?',[['VENDOR-06','VENDOR-06'],['VENDOR-07','VENDOR-07']])}${reason()}${primary('Guardar mi conclusión','submit','type="submit"')}<p class="form-error" role="alert"></p></form>`;
  if (c.form==='expediente') return `<form class="form-card" id="analysis-form"><h3>Presencia, uso y falla reproducida</h3>${select('component','F-01 · Django en records',[['confirmed','Explotabilidad confirmada por la presencia'],['present_not_reachable','Presente; ruta de uso no demostrada'],['false_positive','El componente no existe']])}${select('local','F-02 · Exportación sin autorización',[['confirmed','Falla de autorización reproducida'],['false_positive','Sin CVE, no hay vulnerabilidad']])}<fieldset><legend>Prueba de exportación desde análisis</legend><div data-evidence-picker="export">${evidenceOptions(evidenceFilter('export'))}</div></fieldset>${reason()}${primary('Conservar el expediente','submit','type="submit"')}<p class="form-error" role="alert"></p></form>`;
  if (['contexto','residual'].includes(c.form)) return riskHTML(c);
  if (c.form==='asistente') {
    const audit = runRecords('ai').filter(x=>x.mode==='live-local').at(-1);
    if (!audit) return '<div class="form-card" id="ai-wait"><h3>Primero, la consulta en el puesto</h3><p>Ejecuta <code>lab ia</code> desde aplicaciones. La respuesta real y sus fuentes aparecerán aquí para que las revises.</p></div>';
    return `<form class="form-card" id="review-form" data-audit="${esc(audit.id)}"><span class="station-tag">MODELO LOCAL · CPU · ${esc(audit.model)}</span><h3>Revisa su razonamiento</h3><p>${esc(audit.output.summary)}</p>${audit.output.facts.map(f=>`<div class="ai-fact">${esc(f.statement)}<small>Fuentes propuestas: ${f.evidence_ids.map(esc).join(', ')}</small></div>`).join('')}${(audit.output.missing_context||[]).length?`<details class="source"><summary>Preguntas, opciones y límites</summary><p>${[...audit.output.missing_context,...audit.output.options,...audit.output.limitations].map(esc).join('<br>')}</p></details>`:''}${audit.sources.map(s=>`<details class="source"><summary>${esc(s.id)} · ${esc(s.title)}</summary><p>${esc(s.text)}</p></details>`).join('')}${audit.validation_errors.length?`<p class="inline-warning">La salida tiene errores: ${audit.validation_errors.map(esc).join(' ')}. Debes corregir o rechazar.</p>`:''}${select('verdict','Tu dictamen',[['accept','Aceptar con fundamento'],['correct','Corregir una afirmación'],['reject','Rechazar la propuesta']])}${reason('Cita una afirmación y contrástala con su fuente')}${primary('Registrar revisión humana','submit','type="submit"')}<p class="form-error" role="alert"></p></form>`;
  }
  if (c.form==='cartera') return `<form class="form-card" id="portfolio-form"><h3>Una cartera que puedas ejecutar</h3><p>Máximo 4 h de ingeniería y 15 min de ventana. Incluye A: será la medida que aplicarás en el siguiente objetivo. Compara qué pospones y por qué.</p><div class="portfolio-choices">${[['A','Restringir exportación','2 h · 0 min'],['B','Rotar llave de copias','2 h · 10 min'],['C','Restringir diagnóstico','1 h · 5 min'],['D','Actualizar legacy','3 h · 30 min']].map(([id,t,cost])=>`<label class="package"><input type="checkbox" name="packages" value="${id}">${id} · ${t}<small>${cost}</small></label>`).join('')}</div><div class="metric-line" id="budget-preview">Selecciona los trabajos que puedes comprometer.</div>${select('scope','¿Qué demuestra restringir /api/export?',[['http_only','Restricción de una ruta HTTP; no segmentación de red'],['network','Segmentación de todas las redes internas']])}${select('mitre','Hipótesis ATT&CK que orienta la investigación',[['T1190','T1190 · aplicación pública'],['T1486','T1486 · cifrado de datos']])}${select('iso','Control que orienta la autorización de la aplicación',[['A.8.26','A.8.26 · requisitos de seguridad de aplicaciones'],['A.8.13','A.8.13 · copias de seguridad'],['A.8.22','A.8.22 · segregación de redes']])}${select('law','Marco del deber de gestión y revisión de la OIV ficticia',[['L21663_8','Ley 21.663 · art. 8'],['L21459','Ley 21.459 · delitos informáticos']])}<details class="source"><summary>Fuentes y límites de la asociación</summary><p>El acceso a una aplicación pública se relaciona con la hipótesis ATT&CK T1190. La autorización de la aplicación se vincula con ISO 27001 A.8.26 y la gestión con A.8.8. En la OIV ficticia, analiza las medidas y revisiones del art. 8 de la Ley 21.663. Esta asociación orienta el análisis; el bloqueo de una ruta no acredita cumplimiento integral.</p></details>${reason('Explica qué proteges, qué pospones y el alcance del control')}${primary('Comprometer esta cartera','submit','type="submit"')}<p class="form-error" role="alert"></p></form>`;
  return '';
}
function riskHTML(c) {
  const residual = c.form==='residual', clientId = residual?'salud':riskClient===0?'salud':'agua';
  const client = boot.clients.find(x=>x.id===clientId), d = riskDraft;
  const titles = ['El dueño','Impacto','Urgencia y razón'];
  const scale = (n,label) => `<label>${label}<select name="${n}" required>${[1,2,3,4,5].map(v=>`<option value="${v}" ${Number(d[n]|| (n==='likelihood'?4:1))===v?'selected':''}>${v}${n==='likelihood'?[' · Remota',' · Poco factible',' · Factible',' · Muy factible',' · Casi cierta'][v-1]:[' · Menor',' · Limitado',' · Relevante',' · Grave',' · Crítico'][v-1]}</option>`).join('')}</select></label>`;
  let content;
  if(riskStep===0) content = `<div class="client-dossier"><b>${esc(client.name)} · ${esc(client.sector)}</b><p>${esc(client.story)}</p>${client.owner_cards.map(x=>`<p><b>${esc(x.title)}</b><br>${esc(x.text)}</p>`).join('')}<b>Tolerancia</b> · RTO ${esc(client.rto)} / RPO ${esc(client.rpo)}<br><b>Dueño:</b> ${esc(client.owner)}</div><p>${residual?'Reevalúa el riesgo después de probar el bloqueo y la transacción. No des por corregida la autorización en records.':`Misma falla F-02. ${riskClient===0?'Primero, salud; después, agua.':'Ahora cambia el contexto: conserva L y reconsidera las consecuencias.'}`}</p>`;
  if(riskStep===1) content = `${scale('likelihood','Factibilidad local · L')}<p>Impactos del 1 al 5. Usa las consecuencias para este dueño.</p><div class="impact-fields">${[['operation','Operación'],['people','Personas'],['data','Datos'],['financial','Finanzas']].map(([n,l])=>scale(n,l)).join('')}</div><div class="metric-line">Índice ordinal <b id="risk-preview">—</b><span>4 × L × impacto máximo<br>No es un porcentaje.</span></div>`;
  if(riskStep===2) content = `<div class="two-fields">${select('exploitation','Explotación · SSVC',[['N','None · sin evidencia ni PoC público'],['P','Public PoC · método conocido'],['A','Active · explotación real documentada']])}${select('exposure','Exposición del sistema',[['S','Small · acceso muy controlado'],['C','Controlled · restricciones efectivas'],['O','Open · acceso ampliamente disponible']])}${select('automatable','¿Automatizable?',[['N','No'],['Y','Sí']])}${select('human_impact','Human Impact · SSVC',[['L','Low'],['M','Medium'],['H','High'],['VH','Very High']])}</div><details class="source"><summary>Definiciones de Human Impact</summary><p>Low: Safety negligible/marginal y misión degraded/MEF support crippled. Medium: Safety negligible/marginal + MEF failure, o Safety critical + misión degraded. High: Safety critical + MEF support crippled/MEF failure. Very High: Safety catastrophic o Mission failure. Usa el árbol Deployer; no traslades automáticamente el máximo de los cuatro impactos.</p></details><fieldset><legend>${residual?'Vincula la denegación 403 y la transacción 200 posteriores':'Evidencia de la falla y su contexto'}</legend><div data-evidence-picker="${residual?'residual':'context'}">${evidenceOptions(evidenceFilter(residual?'residual':'context'))}</div></fieldset>${reason('Explica tu decisión para este dueño y sus supuestos')}<label>Responsable de aceptar o tratar<input name="owner" required minlength="3" maxlength="150" value="${esc(client.owner)}"></label>`;
  return `<form class="form-card" id="risk-form" data-client="${clientId}"><h3>${residual?'Evaluación residual':`${riskClient+1} de 2 · ${esc(client.name)}`}</h3><div class="wizard-tabs">${titles.map((x,i)=>`<span class="${i===riskStep?'selected':''}">${i+1}. ${x}</span>`).join('')}</div>${content}<div class="form-actions">${riskStep?'<button type="button" class="quiet-button" data-action="risk-back">← Anterior</button>':'<span></span>'}${riskStep<2?primary('Siguiente →','risk-next','type="button"'):primary(residual?'Guardar evaluación residual':'Registrar decisión','submit','type="submit"')}</div><p class="form-error" role="alert"></p><p class="check-note">Se comprueban cálculo y referencias. El fundamento se discute con el equipo.</p></form>`;
}
function retainRisk() { const f=$('#risk-form'); if(f) for (const [k,v] of new FormData(f)) if(k!=='evidence') riskDraft[k]=v; }
function refreshForm() { $('#challenge-form').innerHTML=formHTML(challenge()); wireForms(); }
function wireForms() {
  const form=$('#quest form'); if (!form) return;
  if(form.id==='advanced-form'){AdvancedUI.wire(form,challenge());return;}
  if(form.id==='risk-form') {
    for(const [key,value] of Object.entries(riskDraft)) if(form.elements[key]) form.elements[key].value=value;
    const preview=()=>{const data=new FormData(form);if($('#risk-preview'))$('#risk-preview').textContent=4*Number(data.get('likelihood'))*Math.max(...['operation','people','data','financial'].map(k=>Number(data.get(k))));}; form.addEventListener('change',preview);preview();
  }
  if(form.id==='portfolio-form') form.addEventListener('change',()=>{const costs={A:[2,0],B:[2,10],C:[1,5],D:[3,30]}, sums=[...new FormData(form).getAll('packages')].reduce((s,k)=>[s[0]+costs[k][0],s[1]+costs[k][1]],[0,0]);$('#budget-preview').textContent=`${sums[0]} / 4 h de ingeniería · ${sums[1]} / 15 min de ventana`;});
  form.addEventListener('submit',async e=>{
    e.preventDefault(); const button=form.querySelector('[type=submit]');button.disabled=true;$('.form-error',form).textContent=''; const data=Object.fromEntries(new FormData(form)), refs=new FormData(form).getAll('evidence');
    try {
      if(form.id==='analysis-form') await api('/api/game/analysis',{...data,challenge_id:selected,evidence_ids:refs});
      if(form.id==='review-form') await api('/api/ai/review',{...data,audit_id:form.dataset.audit});
      if(form.id==='portfolio-form') {
        const packages=new FormData(form).getAll('packages'); if(!packages.includes('A'))throw Error('Incluye A: es la medida comprometida para el siguiente objetivo.');
        await api('/api/portfolio',{client_id:'salud',packages,reason:data.reason}); await api('/api/game/analysis',{challenge_id:selected,scope:data.scope,mitre:data.mitre,iso:data.iso,law:data.law,reason:data.reason});
      }
      if(form.id==='risk-form') {
        retainRisk(); const d=riskDraft;
        const payload={client_id:form.dataset.client,finding_id:'F-02',state:challenge().form==='residual'?'residual':'inherent',likelihood:Number(d.likelihood),impacts:Object.fromEntries(['operation','people','data','financial'].map(k=>[k,Number(d[k])])),ssvc:Object.fromEntries(['exploitation','exposure','automatable','human_impact'].map(k=>[k,d[k]])),reason:data.reason,owner:data.owner,evidence_ids:refs};
        if(!refs.length)throw Error('Vincula al menos una prueba observada.');
        if(selected==='contexto' && riskClient===1) { const first=runRecords('decision').filter(x=>x.client_id==='salud'&&x.finding_id==='F-02'&&x.state==='inherent').at(-1); if(first && (first.likelihood!==payload.likelihood || JSON.stringify(first.impacts)===JSON.stringify(payload.impacts)))throw Error('Conserva L y revisa al menos una consecuencia distinta para agua.'); }
        const result=await api('/api/decisions',payload); toast(`Decisión conservada · índice ${result.calculation.index} · ${result.calculation.ssvc.outcome}`);
        boot=await api('/api/bootstrap');
        if(selected==='contexto' && riskClient===0) {riskClient=1;riskStep=0;riskDraft={likelihood:d.likelihood};refreshForm();return;}
      }
      await verify(); toast('Registro conservado en tu expediente.');
    } catch(error) {$('.form-error',form).textContent=error.message;} finally {button.disabled=false;}
  });
}
function renderGuide() {
  const c=challenge(), done=game.states[c.id]==='done', s=c.steps[step];
  $('#workspace-guide').innerHTML=`<span class="kicker">OBJETIVO EN CURSO</span><h2>${esc(c.title)}</h2><p class="quest-brief">${esc(c.brief)}</p>${done?`<div class="success-panel"><h3>Comprobado · +${c.xp} PX</h3>${primary('Siguiente objetivo →','current')}</div>`:s?`<div class="guide-step-counter">PASO ${step+1} DE ${c.steps.length}</div><div class="guide-location">${esc(s.where)}</div><div class="command"><pre>${esc(s.command)}</pre><button data-action="type" ${connected?'':'disabled'}>Pegar en el puesto</button></div><p class="step-reason">${esc(s.why)}</p><p class="check-note">Haz clic en la terminal. Pegar escribe; tú pulsas Enter.</p><div class="step-navigation"><button class="quiet-button" data-action="step-back" ${step===0?'disabled':''}>← Anterior</button><button class="quiet-button" data-action="step-next" ${step===c.steps.length-1?'disabled':''}>Siguiente paso →</button></div>`:`<p class="muted">Este objetivo se resuelve en la ruta con la evidencia que ya reuniste.</p>${primary('Ir al objetivo','close-desk')}`}<div class="objectives" id="workspace-checks" aria-live="polite">${checksHTML(c)}</div>${hints(c)}`;
}
function openDesk() {
  if(game.states[selected]==='locked')return toast('Completa primero el objetivo activo.');
  if(accessMode!=='novnc'){setAccessMode('novnc');renderQuest();}
  $('#workspace').hidden=false;$('#desk-button').classList.add('selected');$('#route-button').classList.remove('selected');document.body.style.overflow='hidden';
  if(!$('#desktop-frame').getAttribute('src'))$('#desktop-frame').src='/desktop/desk.html';renderGuide();$('#close-workspace').focus();
}
function closeDesk() {$('#workspace').hidden=true;document.body.style.overflow='';$('#desk-button').classList.remove('selected');$('#route-button').classList.add('selected');$('#desk-button').focus();}
async function verify() {
  if(busy||!game)return;busy=true;
  try {
    const oldXP=game.xp, oldDone=game.completed;game=await api('/api/game/verify',{});boot=await api('/api/bootstrap');
    if(game.completed!==oldDone){render();if(game.xp>oldXP)toast(`Objetivo comprobado · +${game.xp-oldXP} PX`);}
    else {AdvancedUI.refresh();refreshEvidencePicker();if($('#quest-checks'))$('#quest-checks').innerHTML=checksHTML(challenge());if($('#workspace-checks'))$('#workspace-checks').innerHTML=checksHTML(challenge());if($('#ai-wait')&&runRecords('ai').some(x=>x.mode==='live-local'))refreshForm();}
    if($('#verification-note'))$('#verification-note').textContent='Comprobación automática activa · sin marcar tareas a mano.';
  } catch(error) {if($('#verification-note'))$('#verification-note').textContent='Sin conexión con el laboratorio. Reconectando…';}
  finally{busy=false;}
}
async function sshAccess() {
  if($('#help').open)$('#help').close();
  $('#ssh-content').innerHTML='<p class="muted">Consultando el acceso a tu puesto…</p>';
  $('#ssh-access').showModal();
  try {
    const access=await api('/api/access');
    $('#ssh-content').innerHTML=`<p class="muted">Tu terminal y noVNC entran al mismo puesto de análisis. Los comandos cuentan para la misma campaña; las decisiones y el progreso siguen en esta plataforma.</p>
      <dl class="access-facts"><div><dt>Usuario</dt><dd><code>${esc(access.username)}</code></dd></div><div><dt>Destino local</dt><dd><code>${esc(access.host)}:${access.port}</code></dd></div><div><dt>Contraseña SSH</dt><dd>No se usa · acceso por llave</dd></div><div><dt>Frase de paso de la llave</dt><dd>Vacía · no se solicita</dd></div></dl>
      <div class="access-command"><span class="station-tag">DESDE LA CARPETA DEL REPOSITORIO</span><p>macOS / Linux</p><pre>${esc(access.mac_linux_command)}</pre><button class="quiet-button" data-copy-access="${esc(access.mac_linux_command)}">Copiar comando macOS / Linux</button><p>Windows PowerShell</p><pre>${esc(access.powershell_command)}</pre><button class="quiet-button" data-copy-access="${esc(access.powershell_command)}">Copiar comando Windows</button></div>
      <p class="access-note">El lanzador prepara los permisos de la llave y verifica el servidor de tu instalación. Al entrar, ejecuta <code>lab iniciar</code>. Después puedes usar <code>ssh ops</code> o <code>ssh appdesk</code>.</p>
      <details class="source"><summary>Llaves publicadas y conexión manual</summary><p>Este par es público e idéntico para el entrenamiento local. Úsalo solo en este laboratorio.</p><div class="access-downloads"><a class="secondary" href="${esc(access.private_key_url)}" download>Descargar llave privada de práctica</a><a class="secondary" href="${esc(access.public_key_url)}" download>Descargar llave pública</a></div><p>En macOS / Linux, desde la raíz del repositorio:</p><pre>chmod 600 training/ssh/vulncorp_student_ed25519
${esc(access.direct_command)}</pre><p>Si descargaste la llave, reemplaza su ruta por la ubicación del archivo. La primera conexión manual pregunta por la identidad del servidor. Compara esta huella antes de aceptar:</p><p class="host-fingerprint"><b>Servidor:</b> ${esc(access.host_fingerprint||'Aún no disponible. Comprueba el puesto y vuelve a abrir este acceso.')}</p><p class="host-fingerprint"><b>Llave del alumno:</b> ${esc(access.key_fingerprint)}</p><details><summary>Ver llave pública del alumno</summary><pre>${esc(access.public_key)}</pre></details></details>
      <div class="dialog-footer"><button class="primary" data-action="use-ssh">Usar mi terminal y ver los pasos</button></div><p class="access-note">Cada alumno usa su instalación local. Soporte y aplicaciones conservan sus redes internas; entrar por SSH no abre conexiones directas desde tu equipo a esos servicios.</p>`;
  } catch(error) {$('#ssh-content').innerHTML=`<p class="form-error">${esc(error.message)}</p><button class="secondary" data-action="retry-ssh-access">Volver a consultar</button>`;}
}
async function notebook() {
  boot=await api('/api/bootstrap');
  const awards=game.awards.map(x=>`<article class="notebook-item"><span class="station-tag">+${x.xp} PX · COMPROBADO</span><h3>${esc(game.catalog.challenges.find(c=>c.id===x.challenge_id)?.title)}</h3><p>${x.checks.map(c=>esc(c.label)).join('<br>')}</p><small>${esc(x.created_at)}</small></article>`).join('');
  const decisions=runRecords('decision').map(d=>`<article class="notebook-item"><h3>${esc(boot.clients.find(c=>c.id===d.client_id)?.name)} · ${d.state==='residual'?'Residual':'Inherente'}</h3><p>F-02 · índice ${d.calculation.index} · SSVC ${esc(d.calculation.ssvc.outcome)}<br>${esc(d.reason)}</p></article>`).join('');
  $('#notebook-content').innerHTML=`<p class="muted">${game.completed} objetivos · ${game.xp} PX. Son hitos de práctica, sin efecto en la nota.</p>${awards||'<p>Tu primera evidencia aparecerá al completar el primer contacto.</p>'}${decisions}${runRecords('lab_record').map(r=>`<article class="notebook-item"><h3>${esc(game.catalog.challenges.find(c=>c.id===r.challenge_id)?.title)}</h3><p>${esc(r.answers.reason)}</p><details class="source"><summary>Ver análisis y fuentes</summary><pre>${esc(JSON.stringify(r,null,2))}</pre></details></article>`).join('')}<details class="source"><summary>Pruebas y procedencia</summary>${runRecords('station').map(p=>`<p><b>${esc(p.action)}</b> · ${esc(p.station)}<br><small>${esc(p.id)}</small></p>`).join('')}${runRecords('evidence').map(p=>`<p><b>${esc(p.action)} · HTTP ${p.result.status}</b> · ${esc(p.actor)}<br><small>${esc(p.id)}</small></p>`).join('')}</details>`;$('#notebook').showModal();
}
document.addEventListener('click',async e=>{
  const zoneButton=e.target.closest('[data-zone]'),level=e.target.closest('[data-level]'),close=e.target.closest('[data-close]');
  if(zoneButton){zone=zoneButton.dataset.zone;const options=game.catalog.challenges.filter(c=>c.zone===zone);selected=(options.find(c=>game.states[c.id]==='active')||options[0]).id;step=0;render();}
  if(level)choose(level.dataset.level);
  if(close)$('#'+close.dataset.close).close();
  const copy=e.target.closest('[data-copy-access]');if(copy){try{await navigator.clipboard.writeText(copy.dataset.copyAccess);toast('Comando copiado. Ejecútalo en la terminal de tu equipo.');}catch(error){toast('Selecciona el comando del recuadro y cópialo con el teclado.');}}
  const a=e.target.closest('[data-action]');if(!a)return;
  const action=a.dataset.action;
  if(action==='desk')openDesk();
  if(action==='ssh-access')sshAccess();
  if(action==='use-ssh'){setAccessMode('ssh');$('#ssh-access').close();renderQuest();$('#quest').focus();}
  if(action==='copy-step'){try{await navigator.clipboard.writeText(challenge().steps[step].command);toast('Comando copiado. Ejecútalo dentro del puesto indicado.');}catch(error){toast('Selecciona el comando y cópialo con el teclado.');}}
  if(action==='retry-ssh-access'){$('#ssh-access').close();sshAccess();}
  if(action==='close-desk')closeDesk();
  if(action==='current'){choose(game.current||game.catalog.challenges.at(-1).id);if(!$('#workspace').hidden){if(challenge().steps.length)renderGuide();else closeDesk();}$('#quest').focus();}
  if(action==='notebook')notebook();
  if(action==='step-back'){step=Math.max(0,step-1);refreshSteps();}
  if(action==='step-next'){step=Math.min(challenge().steps.length-1,step+1);refreshSteps();}
  if(action==='type'){const text=challenge().steps[step].command;$('#desktop-frame').contentWindow.postMessage({type:'lab:type',text},location.origin);}
  if(action==='risk-next'||action==='risk-back'){retainRisk();riskStep+=action==='risk-next'?1:-1;refreshForm();}
});
$('#desk-button').onclick=openDesk;$('#close-workspace').onclick=closeDesk;
$('#expand-workspace').onclick=()=>{const expanded=$('#workspace').classList.toggle('expanded');$('#expand-workspace').textContent=expanded?'Mostrar guía':'Ampliar escritorio';};
$('#route-button').onclick=()=>{closeDesk();choose(game.current||game.catalog.challenges.at(-1).id);};
$('.logo').onclick=e=>{e.preventDefault();$('#route-button').click();};
$('#notebook-button').onclick=notebook;$('#help-button').onclick=()=>$('#help').showModal();
$('#export-button').onclick=async()=>{const bundle=await api('/api/export'),blob=new Blob([JSON.stringify(bundle,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='vulncorp-expediente.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
window.addEventListener('message',e=>{if(e.origin!==location.origin||e.source!==$('#desktop-frame').contentWindow)return;if(e.data?.type==='lab:typed'){$('#desktop-frame').dataset.lastTyped=e.data.text;window.dispatchEvent(new CustomEvent('lab:typed'));toast('Comando escrito. Compruébalo en la terminal y pulsa Enter.');}if(e.data?.type==='lab:connected'){connected=true;$('#workspace').classList.add('connected');$('#connection-status').textContent='Conectado · Puesto de análisis';renderGuide();}if(e.data?.type==='lab:disconnected'){connected=false;$('#workspace').classList.remove('connected');$('#connection-status').textContent='Escritorio desconectado · vuelve a entrar';$('#desktop-frame').removeAttribute('src');renderGuide();}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('#workspace').hidden)closeDesk();});
(async()=>{try{[game,boot]=await Promise.all([api('/api/game'),api('/api/bootstrap')]);selected=game.current||game.catalog.challenges.at(-1).id;zone=challenge().zone;render();await verify();setInterval(()=>{if(!document.hidden)verify();},6000);}catch(error){$('#quest').innerHTML=`<h1>Conecta el laboratorio</h1><p>${esc(error.message)}</p><p>Revisa que los servicios estén iniciados y recarga esta página.</p>`;}})();
