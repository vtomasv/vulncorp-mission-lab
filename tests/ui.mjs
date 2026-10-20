// Developer check. Creates a new campaign; runs real commands through noVNC, not a DOM terminal mock.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const {chromium}=await import(process.env.PLAYWRIGHT_PATH||'playwright');
const full=process.env.LAB_UI_FULL==='1';
execFileSync('docker',['compose','exec','-T','mission','python','-c',"import time;from app.server import save,dispatch;save('game_campaign',{'started':time.time(),'catalog_version':'2.0','purpose':'Validación de navegador'});dispatch('/api/control',{'action':'reset','reason':'Preparar validación real de interfaz conservando todo el historial.'})"]);
const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHANNEL?{channel:process.env.PLAYWRIGHT_CHANNEL}:{})});
const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const getGame=()=>page.evaluate(async()=>fetch('/api/game').then(r=>r.json()));
async function command(text){await page.evaluate(text=>new Promise(resolve=>{window.addEventListener('lab:typed',()=>resolve(),{once:true});document.querySelector('#desktop-frame').contentWindow.postMessage({type:'lab:type',text},location.origin);}),text);await page.frameLocator('#desktop-frame').locator('canvas').focus();await page.keyboard.press('Enter');}
async function completed(id){await page.waitForFunction(async id=>(await fetch('/api/game').then(r=>r.json())).states[id]==='done',id,{timeout:280000});await page.waitForFunction(()=>document.querySelector('.success-panel')!==null);console.log('PASS browser',id);}
async function next(){const scope=await page.locator('#workspace').isVisible()?'#workspace':'#quest';await page.locator(scope+' [data-action=current]').first().click();}
async function desk(){if(!await page.locator('#workspace').isVisible())await page.getByRole('button',{name:'Entrar al puesto →',exact:true}).click();await page.locator('#workspace.connected').waitFor({timeout:30000});}
async function route(){if(await page.locator('#workspace').isVisible())await page.getByRole('button',{name:'← Volver a la ruta',exact:true}).click();}
async function fillReason(text='La evidencia observada delimita el alcance de esta conclusión. Debo contrastar las consecuencias y la aceptación con el dueño.'){await page.locator('#quest [name=reason]').fill(text);}
try {
await fs.mkdir('docs/assets',{recursive:true});await page.goto('http://127.0.0.1:8095');await page.getByRole('heading',{name:'Primer contacto',exact:true}).waitFor();
assert.equal(await page.locator('body').innerText().then(t=>/clase\s*\d|calificaci[oó]n/i.test(t)),false);
await page.screenshot({path:'docs/assets/mission-control.png',fullPage:false});
// Locked previews explain a prerequisite and cannot open a workstation for that goal.
await page.locator('[data-zone=senales]').click();assert.equal(await page.locator('.locked-panel').isVisible(),true);await page.locator('[data-action=current]').click();
await desk();await page.frameLocator('#desktop-frame').locator('canvas').focus();await page.keyboard.press('Control+u');await page.keyboard.press('Control+l');await page.getByRole('button',{name:'Pegar en el puesto',exact:true}).click();await page.waitForFunction(()=>document.querySelector('#desktop-frame').dataset.lastTyped==='lab iniciar');await page.frameLocator('#desktop-frame').locator('canvas').focus();await page.keyboard.press('Enter');await completed('contacto');await page.waitForTimeout(500);await page.screenshot({path:'docs/assets/workstation-proof.png'});
await next();await command('curl -s http://gateway:8080/api/transaction | jq');await completed('funcion');
await next();await command('lab red');await completed('segmento');
await next();await command('curl -s http://gateway:8080/api/export | jq');await page.waitForTimeout(650);await command('curl -s http://gateway:8080/api/diagnostics | jq');await completed('exposicion');
await next();await command('ssh ops');await page.waitForTimeout(1000);await command('lab red');await page.waitForTimeout(700);await command("curl -s -H 'X-Training-Key: training-backup-key' http://backup:8082/catalog | jq");await completed('soporte');
if(full){
 await next();await command('exit');await page.waitForTimeout(500);await command('ssh appdesk');await page.waitForTimeout(900);await command('lab inventario');await completed('inventario');
 await next();await command('lab escanear');await completed('alertas');await next();await command('lab revisar');await completed('aplicabilidad');
 await next();await command('lab contrastar');await page.waitForFunction(async()=>{const r=await fetch('/api/bootstrap').then(r=>r.json());const run=(await fetch('/api/game').then(r=>r.json())).run;return r.records.station.some(x=>x.action==='contrastar'&&x.occurred_at>=run.started);},null,{timeout:120000});await route();
 await page.selectOption('[name=duplicate]','VENDOR-06');await page.selectOption('[name=misattributed]','VENDOR-07');await fillReason();await page.locator('#analysis-form [type=submit]').click();await completed('proveedor');await next();
 await page.selectOption('[name=component]','present_not_reachable');await page.selectOption('[name=local]','confirmed');await page.locator('[name=evidence]').first().check();await fillReason();await page.locator('#analysis-form [type=submit]').click();await completed('expediente');await next();
 for(const [client,impacts] of [['salud',{operation:4,people:3,data:4,financial:3}],['agua',{operation:2,people:1,data:2,financial:2}]]){
  await page.getByRole('button',{name:'Siguiente →',exact:true}).click();await page.selectOption('[name=likelihood]','4');for(const [k,v]of Object.entries(impacts))await page.selectOption(`[name=${k}]`,String(v));assert.equal(await page.locator('#risk-preview').textContent(),client==='salud'?'64':'32');await page.getByRole('button',{name:'Siguiente →',exact:true}).click();
  for(const[k,v]of Object.entries({exploitation:'P',exposure:'O',automatable:'Y',human_impact:client==='salud'?'H':'L'}))await page.selectOption(`[name=${k}]`,v);
  await page.locator('[name=evidence]').filter({visible:true}).first().check(); // observed transaction or export; add export explicitly below
  await page.locator('.evidence-option').filter({hasText:'export · HTTP 200'}).locator('input').check();await fillReason();await page.locator('#risk-form [type=submit]').click();if(client==='salud')await page.getByRole('heading',{name:'2 de 2 · Aguas del Valle Sur'}).waitFor();
 }
 await completed('contexto');await next();await desk();await command('lab ia');await page.waitForFunction(async()=>{const r=await fetch('/api/bootstrap').then(r=>r.json());const g=await fetch('/api/game').then(r=>r.json());return r.records.ai.some(a=>a.game_run===g.run.id);},null,{timeout:280000});await route();await page.locator('#review-form').waitFor();await page.selectOption('[name=verdict]','correct');await fillReason('La fuente describe una hipótesis del caso. No sustenta afirmar observación real sin el registro de la exportación; corrijo esa inferencia y consulto el impacto al dueño.');await page.locator('#review-form [type=submit]').click();await completed('asistente');await next();
 await page.locator('[name=packages][value=A]').check();await page.locator('[name=packages][value=B]').check();for(const[k,v]of Object.entries({scope:'http_only',mitre:'T1190',iso:'A.8.26',law:'L21663_8'}))await page.selectOption(`[name=${k}]`,v);await fillReason();await page.locator('#portfolio-form [type=submit]').click();await completed('cartera');await next();
 await desk();await command('lab proteger');await page.waitForTimeout(1000);await command('Restringir exportación temporalmente y comprobar después denegación y función de negocio.');await completed('medida');await next();await command('exit');await page.waitForTimeout(500);await command('curl -s http://gateway:8080/api/export | jq');await page.waitForTimeout(700);await command('curl -s http://gateway:8080/api/transaction | jq');
 await page.waitForFunction(async()=>{const r=await fetch('/api/bootstrap').then(r=>r.json());const g=await fetch('/api/game').then(r=>r.json());return r.records.evidence.some(x=>x.actor==='analyst'&&x.occurred_at>=g.run.started&&x.action==='export'&&x.result.status===403);});await route();
 // Re-open the goal so the evidence chooser includes the newly collected post-change proofs.
 await page.locator('[data-level=continuidad]').click();await page.getByRole('button',{name:'Siguiente →',exact:true}).click();await page.selectOption('[name=likelihood]','2');for(const[k,v]of Object.entries({operation:'4',people:'3',data:'4',financial:'3'}))await page.selectOption(`[name=${k}]`,v);await page.getByRole('button',{name:'Siguiente →',exact:true}).click();
 for(const[k,v]of Object.entries({exploitation:'P',exposure:'C',automatable:'Y',human_impact:'H'}))await page.selectOption(`[name=${k}]`,v);await page.waitForFunction(()=>document.querySelectorAll('[data-evidence-picker=residual] input').length>=2);for(const checkbox of await page.locator('[name=evidence]').all())await checkbox.check();await fillReason();await page.locator('#risk-form [type=submit]').click();await completed('continuidad');const final=await getGame();assert.equal(final.xp,1370);assert.equal(final.completed,15);await page.screenshot({path:'artifacts/game-complete.png'});
}
await route();await page.getByRole('button',{name:'Cuaderno',exact:true}).click();await page.getByRole('dialog',{name:'Lo que ya puedes demostrar'}).waitFor();await page.getByRole('button',{name:'Cerrar cuaderno',exact:true}).click();
await page.setViewportSize({width:390,height:844});await page.locator('#route-button').click();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:'docs/assets/game-mobile.png',fullPage:true});
await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.evaluate(()=>getComputedStyle(document.body).colorScheme),'light');assert.deepEqual(errors,[]);
} catch(error) {await page.screenshot({path:'artifacts/game-ui-failure.png',fullPage:true});console.error('Visible errors:',await page.locator('.form-error').allTextContents());await browser.close();throw error;}
await browser.close();console.log(`PASS: noVNC real, ${full?'15':'5'} objetivos, rutas y ${full?'formularios, IA y residual, ':''}escritorio/móvil sin desborde ni errores de consola.`);
