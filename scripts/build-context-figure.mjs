// Anatomy Figure: a document comparison bench. Build-time only; no browser dependency.
// One fixed finding, three dossiers. The reader moves; technical severity does not.
import fs from 'node:fs';
import * as k from './vendor/anatomy/iso-kit.mjs';
import * as A from './vendor/anatomy/audit.mjs';

const P=k.fitProjection(k.boxCorners({x:-154,y:-72,w:308,d:144,r:8},-7,48),620,330,{pad:25,azimuth:52,elevation:35});
const R=A.recorder(P);
const S=k.solidSvg,L=k.lineSvg;
const parts=[];
function slab(name,plan,z,h,{tone='mid',inner='',moving=false,bevel=.4}={}){
  const svg=S(k.slabOf(plan,z,h,P,5,bevel),{tone,inner});
  parts.push({name,plan,z,h,moving});
  R.put({name,piece:moving?'reader':'bench',anchor:[plan.x+plan.w/2,plan.y+plan.d/2,z+h/2],at:[plan.x+plan.w/2,plan.y+plan.d/2,z+h/2],svg,
    shapes:[R.solid(A.slab(plan,z,h,{name},5))]});
}
// Base: 4 pads, 4 feet, deck, inset groove, 4 fasteners and a ruler.
for(const [i,[x,y]] of k.corners({x:-150,y:-68,w:300,d:136,r:9},17).entries()){
 slab('stand.pad.'+i,{x:x-8,y:y-7,w:16,d:14,r:2},-7,2,{tone:'lo'});
 slab('stand.foot.'+i,{x:x-6,y:y-5,w:12,d:10,r:1.4},-5,5,{tone:'lo'});
}
const deck={x:-150,y:-68,w:300,d:136,r:9};
slab('stand.deck',deck,0,8,{tone:'lo',bevel:1.2,inner:L(k.planOutline(k.insetPlan(deck,5),8,P),{tone:'faint'})});
for(const [i,[x,y]] of k.corners(deck,10).entries())slab('stand.fastener.'+i,{x:x-1.2,y:y-1.2,w:2.4,d:2.4,r:.8},8,.5,{tone:'lo'});
const rule={x:-128,y:58,w:256,d:5,r:.7};
const ticks=k.topTicks(-124,124,4,5,58.2,8.7,[1.7,3.5],P);
slab('stand.ruler',rule,8,.7,{tone:'lo',inner:L(ticks.minor,{tone:'lo'})+L(ticks.major,{tone:'mid'})});
// Structure: two rails and four end stops, all mounted to the deck.
for(const [i,y] of [-51,45].entries()){
 slab('stand.rail.'+i,{x:-135,y,w:270,d:6,r:1},8,4,{tone:'mid'});
 for(const [j,x] of [-140,135].entries())slab('stand.stop.'+i+'.'+j,{x,y:y-2,w:5,d:10,r:1},8,7,{tone:'mid'});
}
// Three trays: 3 sheets each, tabs, binder clips and engraved label plates.
for(const [i,x] of [-88,0,88].entries()){
 slab('tray.'+i,{x:x-36,y:-36,w:72,d:72,r:3},8,1.4,{tone:'mid',bevel:.6});
 for(let page=0;page<3;page++){
  const p={x:x-30+page*.5,y:-28+page*.5,w:60,d:57,r:1.3};
  const top=9.4+(page+1)*.6;
  const ink=page===2?[0,1,2,3,4].map(n=>L(k.lineOnTop([p.x+8,p.y+23+n*5],[p.x+48-(n%2)*9,p.y+23+n*5],top,P),{tone:'lo',free:true})).join(''):'';
  slab('paper.'+i+'.'+page,p,9.4+page*.6,.6,{tone:'hi',inner:ink,bevel:.1});
 }
 slab('tab.'+i,{x:x+18,y:-31,w:11,d:7,r:1},11.2,.7,{tone:'mid'});
 slab('clip.'+i,{x:x-20,y:-27,w:20,d:4,r:.8},11.2,1.2,{tone:'lo'});
 slab('label.'+i,{x:x-20,y:-15,w:21,d:7,r:.6},11.2,.3,{tone:'mid'});
}
// Reader: two sliding shoes, two posts, bridge, reader housing and three ridges.
for(const [i,y] of [-51,45].entries()){
 slab('reader.shoe.'+i,{x:-8,y,w:16,d:6,r:1},12,3,{moving:true});
 slab('reader.post.'+i,{x:-4,y,w:8,d:6,r:.8},15,18,{moving:true});
}
slab('reader.bridge',{x:-4,y:-51,w:8,d:102,r:.8},33,4,{moving:true});
slab('reader.housing',{x:-12,y:-9,w:24,d:22,r:2},37,4,{moving:true,tone:'hi',bevel:.8});
for(let i=0;i<3;i++)slab('reader.ridge.'+i,{x:-9,y:-5+i*5,w:18,d:2,r:.4},41,.6,{moving:true,tone:'hi'});

// The reader travels above the documents; only its shoes meet the continuous rails.
// Solve painter order and audit each station and the intermediate positions.
let markup='';
for(const x of [-88,-44,0,44,88]){
 const posed=A.recorder(P);
 for(const it of R.items){
  const d=it.piece==='reader'?[x,0,0]:[0,0,0];
  const shapes=it.shapes.map(shape=>posed.solid(A.moved(shape,d)));
  posed.put({...it,key:undefined,at:it.anchor.map((n,i)=>n+d[i]),shapes,svg:it.piece==='reader'?`<g transform="${k.translateAlong(P,d)}">${it.svg}</g>`:it.svg});
 }
 A.settle(posed,P);
 A.auditOrExit(posed,P);
 if(x===0){
  posed.items.sort((a,b)=>a.key-b.key);
  markup=posed.items.map(it=>`<g data-solid="${it.name}"${it.piece==='reader'?' data-reader-part':''}>${it.svg}</g>`).join('');
 }
}
// One set of painter keys must remain valid over the reader's complete travel.
const moving=A.recorder(P);
for(const it of R.items){
 const shift=it.piece==='reader'?[-88,0,0]:[0,0,0];
 const shapes=it.shapes.map(shape=>moving.solid(A.moved(shape,shift)));
 moving.put({...it,key:undefined,at:it.anchor.map((n,i)=>n+shift[i]),move:it.piece==='reader'?[176,0,0]:[0,0,0],shapes,
   svg:it.piece==='reader'?`<g transform="${k.translateAlong(P,shift)}">${it.svg}</g>`:it.svg});
}
A.settle(moving,P,{states:A.uniformStates(16)});
A.auditOrExit(moving,P);
const lift=k.depthOf([176,0,0],P);
markup=moving.items.map(it=>`<g data-solid="${it.name}" data-depth="${it.key.toFixed(6)}" data-lift="${it.piece==='reader'?lift.toFixed(6):0}"${it.piece==='reader'?' data-reader-part':''}>${it.svg}</g>`).join('');
const svg=k.figureSvg({width:620,height:330,label:'Mesa de comparación con tres expedientes y un lector móvil. Representa un mismo hallazgo leído en tres contextos de negocio; es una maqueta conceptual, no un escáner.',body:markup});
const vector=k.axisVector(P,[1,0,0]).map(n=>Number(n.toFixed(6)));
fs.writeFileSync('web/context-figure.js',`// Generated by scripts/build-context-figure.mjs. Anatomy, MIT; see scripts/vendor/anatomy/LICENSE.\nwindow.ContextFigure={svg:${JSON.stringify(svg)},axis:${JSON.stringify(vector)},stops:[-88,0,88],parts:${parts.length}};\n`);
fs.writeFileSync('artifacts/figure-parts.json',JSON.stringify(parts,null,2));
console.log(`Context figure: ${parts.length} real solids; five reader positions checked, 17 depth poses solved.`);
