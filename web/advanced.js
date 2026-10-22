/* One decision at a time. Drafts survive polling and route changes in this tab. */
const AdvancedUI = (() => {
  const drafts = new Map();
  function state(c) {
    const key = game.run.id + ':' + c.id;
    if (!drafts.has(key)) drafts.set(key, {page: 0, answers: {}, refs: []});
    return drafts.get(key);
  }
  function events() { const final=!!boot.continuation && !!boot.advanced.exercises[challenge().id]?.final_mission; return (boot.records.lab_event || []).filter(r => r.campaign === game.run.id && (!final || r.episode===boot.continuation.episode)); }
  function audit(purpose) { const spec=boot.advanced.exercises[challenge().id]; return runRecords('ai').filter(a => a.purpose === (purpose||spec?.ai_purpose||'oiv-dossier') && (!spec?.final_mission || a.episode===boot.continuation.episode)).at(-1); }
  function field(f, draft) {
    const value = draft.answers[f.key] || '';
    return `<label>${esc(f.label)}${f.options ? `<select name="${esc(f.key)}" required><option value="">Selecciona según tu evidencia</option>${f.options.map(([v,l])=>`<option value="${esc(v)}" ${v===value?'selected':''}>${esc(l)}</option>`).join('')}</select>` : `<textarea name="${esc(f.key)}" required minlength="${f.min||1}" maxlength="${f.max||1800}" rows="3">${esc(value)}</textarea>`}</label>`;
  }
  function sourcePanel() {
    const rows = events();
    return `<details class="source advanced-sources" data-version="${esc(rows.length+':'+(rows.at(-1)?.id||''))}"><summary>Consultar evidencia del rango · ${rows.length} eventos</summary><p class="muted">IDs y secuencias del servidor. Elige las fuentes que sostienen tu conclusión. Los eventos de control no acreditan por sí solos el resultado.</p><div class="event-list">${rows.slice().reverse().map(r=>`<article><b>${esc(r.kind)} ${r.status!==undefined?'· HTTP '+esc(r.status):''}</b><p><code>${esc(r.id)}</code><br>Secuencia ${esc(r.sequence)} · ${esc(r.provenance)}<br>${esc(r.identity||'')} ${esc(r.route||'')}<br>Correlación: ${esc(r.correlation||'—')}</p><details><summary>Ver registro completo</summary><pre>${esc(JSON.stringify(r,null,2))}</pre></details></article>`).join('')||'<p>Ejecuta primero la prueba indicada en aplicaciones.</p>'}</div></details>`;
  }
  function aiPanel(purpose) {
    const a = audit(purpose);
    if (!a) { const c=challenge(),command=c.id==='auditoria'?'ia-expediente':c.id; return `<div id="advanced-ai-wait" class="client-dossier"><p>Ejecuta <code>lab ${esc(command)}</code>. La propuesta aparecerá al terminar la inferencia local. Conserva el formulario mientras esperas.</p></div>`; }
    const out=a.output&&typeof a.output==='object'?a.output:{}, list=v=>Array.isArray(v)?v:[];
    return `<div class="client-dossier"><span class="station-tag">${esc(a.model)} · CPU · INFERENCIA REAL</span><h3>Propuesta que debes revisar</h3><p>${esc(out.summary)}</p>${list(out.facts).filter(f=>f&&typeof f==='object').map(f=>`<p>${esc(f.statement)}<br><small>Fuentes propuestas: ${list(f.evidence_ids).map(esc).join(', ')}</small></p>`).join('')}${(a.sources||[]).map(s=>`<details class="source"><summary>${esc(s.id)} · ${esc(s.title)}</summary><p>${esc(s.text)}</p></details>`).join('')}<details class="source"><summary>Incertidumbres y validación</summary><p>${[...list(out.missing_context),...list(out.options),...list(out.limitations),...a.validation_errors].map(esc).join('<br>')}</p><p>Digest del modelo: ${esc(a.model_digest)}</p></details><details class="source"><summary>Salida completa del modelo</summary><pre>${esc(JSON.stringify(a.output,null,2))}</pre></details></div>`;
  }
  function finalContext(c,spec) {
    if (!spec.final_mission) return '';
    const x=boot.continuation, item=c.zone==='defensa'?x.closure_case:c.zone==='operacion'?x.drift:x.contract;
    const labels={client:'Cliente',function:'Función',owner:'Dueño',scope:'Alcance',stop:'Condición de detención',policy:'Criterio docente',event:'Cambio observado',owner_update:'Nuevo contexto del dueño',likelihood:'Verosimilitud del escenario',impacts:'Impactos',index:'Índice ordinal',rule:'Regla',alternative:'Alternativa',oiv:'Supuesto OIV',facts:'Hechos y límites',evaluation:'Evaluación',operation:'Operación',people:'Personas',data:'Datos',finance:'Finanzas'};
    const value=v=>typeof v==='object'?Object.entries(v).map(([k,n])=>`${esc(labels[k]||k)}: ${esc(n)}`).join(' · '):esc(v);
    const details=Object.entries(item).map(([k,v])=>`<p><b>${esc(labels[k]||k)}</b>: ${value(v)}</p>`).join('');
    return `<details class="source"><summary>Consultar el encargo y sus límites</summary>${details}</details><details class="source"><summary>Avisos PHP y método de comprobación</summary>${x.documents.map(d=>`<article><h3>${esc(d.id)} · ${esc(d.title)}</h3><p>${esc(d.text)}</p>${d.url?`<a href="${esc(d.url)}" target="_blank" rel="noopener noreferrer">Consultar fuente primaria</a>`:''}</article>`).join('')}<p>Fuentes consultadas ${esc(x.images.verified_at||'2026-10-21')}. La prueba multipart es funcional; no reproduce RCE.</p></details>${['ia-hostil','revision-ia'].includes(c.id)?`<details class="source"><summary>Documento del proveedor del escenario</summary><p>${esc(x.supplier_note.text)}</p></details>`:''}`;
  }
  function render(c) {
    const spec = boot.advanced.exercises[c.id], d = state(c), page = spec.pages[d.page], last = d.page === spec.pages.length-1;
    const saved = runRecords('lab_record').filter(r=>r.challenge_id===c.id).at(-1);
    const dossier = ['incidente','reportes','excepcion'].includes(c.id) ? `<details class="source"><summary>Consultar dossier de negocio y reglas del reporte</summary><pre>${esc(JSON.stringify(boot.advanced.incident,null,2))}</pre><p>${esc(boot.advanced.legal_summary)}</p></details>` : '';
    const prior = c.id==='matriz'?`<details class="source"><summary>Consultar hallazgos y fuentes del expediente original</summary><p>F-02 corresponde a /api/export y su mitigación anterior. R-01 y R-02 pertenecen al nuevo rango; corregir /range/live no corrige /api/export.</p>${boot.findings.filter(f=>f.id.startsWith('F-')).map(f=>`<p><b>${esc(f.id)} · ${esc(f.title)}</b><br>${esc(f.description)}<br>Fragmentos: ${f.evidence.map(esc).join(', ')}</p>`).join('')}${boot.corpus.map(s=>`<details><summary>${esc(s.id)} · ${esc(s.title)}</summary><p>${esc(s.text)}</p></details>`).join('')}</details>`:'';
    return `${c.id==='auditoria'||spec.ai_purpose?aiPanel():''}${c.id==='revision-ia'?`<details class="source"><summary>Comparar las dos inferencias conservadas</summary><h3>Consulta inicial</h3>${aiPanel('php-ai-clean')}<h3>Documento con instrucciones</h3>${aiPanel('php-ai-hostile')}</details>`:''}${dossier}${prior}${finalContext(c,spec)}<form class="form-card" id="advanced-form"><span class="station-tag">${esc(spec.title)}</span>${spec.pages.length>1?`<p class="muted">Decisión ${d.page+1} de ${spec.pages.length}</p>`:''}<h3>${esc(page.title)}</h3>${page.fields.map(f=>field(f,d)).join('')}${last?`<details class="source"><summary>Vincular fuentes del rango · <span id="advanced-ref-count">${d.refs.length}</span> elegidas</summary><div id="advanced-ref-picker">${refOptions(d)}</div></details><p class="check-note">Se comprueban pruebas, relaciones y estructura. El fundamento requiere discusión profesional; estos PX no tienen nota.</p>`:''}<div class="form-actions">${d.page?'<button class="quiet-button" type="button" data-advanced-back>← Anterior</button>':'<span></span>'}<button class="primary" type="submit">${last?'Conservar análisis':'Siguiente →'}</button></div><p class="form-error" role="alert"></p>${saved?'<p class="muted">Ya hay un análisis conservado. Puedes revisarlo en el expediente y corregirlo mientras este objetivo siga activo.</p>':''}</form>${c.id==='capa'?'<p><a class="secondary" href="/api/advanced/layer" download="attack-layer.json">Descargar capa Navigator</a></p>':''}${sourcePanel()}<details class="source"><summary>Fuentes del método y del marco chileno</summary>${boot.advanced.sources.map(s=>`<p><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a></p>`).join('')}<p>Consultadas ${esc(boot.advanced.consulted_at)}. Asociaciones docentes; no acreditan cumplimiento.</p></details>`;
  }
  function refOptions(d) {
    return events().slice().reverse().map(r=>`<label class="evidence-option"><input type="checkbox" name="advanced-evidence" value="${esc(r.id)}" ${d.refs.includes(r.id)?'checked':''}><span>${esc(r.kind)} ${r.status!==undefined?'· '+esc(r.status):''} ${esc(r.identity||'')}<small>${esc(r.id)}</small></span></label>`).join('') || '<p class="muted">Aún no hay eventos. Ejecuta el comando en la estación indicada.</p>';
  }
  function retain(form,c) {
    const d=state(c);
    for(const [k,v] of new FormData(form)) if(k!=='advanced-evidence')d.answers[k]=v;
    if(form.querySelector('#advanced-ref-picker'))d.refs=new FormData(form).getAll('advanced-evidence');
    return d;
  }
  function wire(form,c) {
    form.querySelector('[data-advanced-back]')?.addEventListener('click',()=>{const d=retain(form,c);d.page--;refreshForm();});
    form.addEventListener('change',()=>{const d=retain(form,c);if($('#advanced-ref-count'))$('#advanced-ref-count').textContent=d.refs.length;});
    form.addEventListener('submit',async e=>{
      e.preventDefault(); const d=retain(form,c), spec=boot.advanced.exercises[c.id];
      if(d.page<spec.pages.length-1){d.page++;refreshForm();$('#advanced-form h3')?.scrollIntoView({block:'nearest'});return;}
      const button=form.querySelector('[type=submit]');button.disabled=true;$('.form-error',form).textContent='';
      try{await api('/api/advanced/record',{challenge_id:c.id,answers:d.answers,evidence_ids:d.refs});await verify();toast('Análisis conservado. Las pruebas técnicas se comprueban por separado.');}
      catch(error){$('.form-error',form).textContent=error.message;}
      finally{button.disabled=false;}
    });
  }
  function refresh() {
    const c=challenge();if(c.form!=='advanced')return;
    const form=$('#advanced-form'), picker=$('#advanced-ref-picker');
    if(form&&picker){const d=retain(form,c),version=events().map(r=>r.id).join(',');if(picker.dataset.version!==version){picker.innerHTML=refOptions(d);picker.dataset.version=version;}}
    if($('#advanced-ai-wait')&&audit())refreshForm();
    const old=$('.advanced-sources');const rows=events(),version=rows.length+':'+(rows.at(-1)?.id||'');if(old&&old.dataset.version!==version){const open=old.open;const wrapper=document.createElement('div');wrapper.innerHTML=sourcePanel();wrapper.firstElementChild.open=open;old.replaceWith(wrapper.firstElementChild);}
  }
  return {render,wire,refresh};
})();
