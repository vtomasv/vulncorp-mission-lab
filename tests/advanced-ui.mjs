// Pure rendering contract: malformed model output must remain reviewable/rejectable.
// No browser, network, model inference or learner progress is fabricated here.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const config=JSON.parse(fs.readFileSync('data/advanced.json','utf8'));
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const audit={id:'RENDER-FIXTURE',model:'render-test-only',model_digest:'fixture',purpose:'oiv-dossier',sources:[],validation_errors:['facts debe ser lista'],output:{summary:'<script>untrusted</script>',facts:{unexpected:true},missing_context:null,options:'invalid',limitations:42}};
const context=vm.createContext({game:{run:{id:'UI-RENDER-FIXTURE'}},boot:{advanced:config,records:{lab_event:[]}},runRecords:kind=>kind==='ai'?[audit]:[],esc});
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
