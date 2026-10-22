// Pure rendering contract: malformed model output must remain reviewable/rejectable.
// No browser, network, model inference or learner progress is fabricated here.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const config=JSON.parse(fs.readFileSync('data/advanced.json','utf8'));
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const audit={id:'RENDER-FIXTURE',model:'render-test-only',model_digest:'fixture',purpose:'oiv-dossier',sources:[],validation_errors:['facts debe ser lista'],output:{summary:'<script>untrusted</script>',facts:{unexpected:true},missing_context:null,options:'invalid',limitations:42}};
let current={id:'auditoria'};
const context=vm.createContext({challenge:()=>current,game:{run:{id:'UI-RENDER-FIXTURE'}},boot:{advanced:config,records:{lab_event:[]}},runRecords:kind=>kind==='ai'?[audit]:[],esc});
vm.runInContext(fs.readFileSync('web/advanced.js','utf8'),context);
const render=vm.runInContext('AdvancedUI.render',context);
let html=render({id:'auditoria'});
assert.ok(html.includes('Salida completa del modelo'));
assert.ok(html.includes('facts debe ser lista'));
assert.ok(html.includes('&lt;script&gt;untrusted&lt;/script&gt;'));
assert.ok(!html.includes('<script>untrusted</script>'));
assert.ok(html.includes('name="verdict"'));
audit.output={summary:'Una salida válida',facts:[null,{statement:'<b>dato no confiable</b>',evidence_ids:'invalid'}],missing_context:[],options:[],limitations:[]};
html=render({id:'auditoria'});
assert.ok(html.includes('&lt;b&gt;dato no confiable&lt;/b&gt;'));
assert.ok(html.includes('Conservar análisis'));
console.log('PASS: malformed/untrusted model content stays visible, escaped and reviewable.');

const final=JSON.parse(fs.readFileSync('data/continuation.json','utf8'));
context.boot.advanced={...config,exercises:{...config.exercises,...final.exercises}};
context.boot.continuation={...final,episode:'render-only',images:{consulted_at:'2026-10-21'}};
context.boot.records.lab_event=[{id:'render-event',campaign:'UI-RENDER-FIXTURE',episode:'render-only',kind:'php-document',sequence:1}];
for(const [id,spec] of Object.entries(final.exercises)) {
  current={id,zone:id.startsWith('cierre-')?'defensa':id.startsWith('ops-')?'operacion':'asistente'};
  html=render(current);
  assert.ok(html.includes('Conservar análisis')||html.includes('Siguiente →'),id);
  assert.ok(html.includes('Consultar el encargo'),id);
  assert.ok(!html.includes('<script>untrusted</script>'),id);
}
audit.purpose='php-ai-clean';audit.episode='render-only';
current={id:'ia-base',zone:'asistente'};
html=render(current);assert.ok(html.includes('Una salida válida'));
assert.ok(html.includes('php-document'));
console.log('PASS: all 24 final forms render; current episode and actual-purpose inference remain selectable.');
