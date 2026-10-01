// Minimal DOM harness: verifies actual handlers, state reset and staged reveal.
// It does not claim graphical browser or classroom projector acceptance.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=fs.readFileSync(path.join(ROOT,'demos/compression-playground.html'),'utf8');
assert(!/https?:\/\//.test(html),'Offline playground has a network dependency');
const elements={};
function element(){return {textContent:'',value:'',style:{},disabled:false,hidden:false,children:[],replaceChildren(...items){this.children=items}};}
const document={getElementById(id){return elements[id]??=element()},createElement(){return element()}};
document.getElementById('pattern').value='runs';document.getElementById('value').value='121';
vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],{document,JSON,Math,Number,Array});
assert.equal(elements['rle-out'].textContent,'');
elements.encode.onclick();assert.match(elements['rle-out'].textContent,/16 B → 6 B/);
for(let i=0;i<3;i++)elements.decode.onclick();assert.equal(elements.restored.children.length,16);assert.match(elements['rle-out'].textContent,/true/);
elements.pattern.value='alternate';elements.pattern.onchange();assert.equal(elements['rle-out'].textContent,'');assert.equal(elements.decode.disabled,true);
elements.encode.onclick();assert.match(elements['rle-out'].textContent,/16 B → 32 B/);
for(let i=0;i<7;i++)elements.next.onclick();assert.match(elements['delta-out'].textContent,/22 bit → 3 B/);
elements['reset-delta'].onclick();assert.equal(elements['delta-out'].textContent,'');
elements.map.onclick();assert.match(elements['quant-out'].textContent,/代表值120/);
elements.value.value='120';elements.value.oninput();assert.equal(elements['quant-out'].textContent,'');elements.map.onclick();assert.match(elements['quant-out'].textContent,/代表值120/);
elements.value.value='256';elements.map.onclick();assert.match(elements['quant-out'].textContent,/输入0–255/);
fs.writeFileSync(path.join(ROOT,'validation/playground-handlers.json'),JSON.stringify({pass:true,checks:['RLE 6B and 32B','exact restoration','input clears stale result','delta seven-step reveal and reset','quantization many-to-one and input bounds','no network dependency'],scope:'Node DOM handler harness; graphical browser not tested'},null,2));
console.log('Playground handler checks passed.');
