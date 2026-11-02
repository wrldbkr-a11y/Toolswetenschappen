//////////////////// BLAD IN 3D ////////////////////
(function(){
  const cv=$('blad3d'), ctl=$('ctl-blad3d');
  let renderer=null, scene, camera, pivot, klaar=false;
  $('blad-2d').onclick=()=>{ $('blad-2d').classList.add('on'); $('blad-3d').classList.remove('on'); $('fig-blad').style.display=''; $('ctl-blad').style.display=''; $('blad3d-wrap').style.display='none'; ctl.style.display='none'; };
  $('blad-3d').onclick=()=>{ $('blad-3d').classList.add('on'); $('blad-2d').classList.remove('on'); $('fig-blad').style.display='none'; $('ctl-blad').style.display='none'; $('blad3d-wrap').style.display=''; ctl.style.display=''; if(!klaar) bouw(); render(); };
  const LAGEN=[
    {id:'was', naam:'waslaagje', kleur:'#bae6fd', info:'Een dun, doorzichtig <b>waslaagje</b> op het dekweefsel. Het laat geen water door en <b>beperkt de verdamping</b>.'},
    {id:'dek', naam:'dekweefsel', kleur:'#d9f99d', info:'Eén laag platte, doorzichtige cellen aan de boven- en onderkant, zonder bladgroenkorrels. Het <b>dekweefsel</b> beschermt het blad en laat het licht door.'},
    {id:'pal', naam:'vulweefsel (dicht)', kleur:'#22c55e', info:'Bovenaan: lange cellen <b>dicht tegen elkaar</b>, vol bladgroenkorrels. Hier gebeurt de meeste <b>fotosynthese</b>.'},
    {id:'spo', naam:'vulweefsel (los)', kleur:'#86efac', info:'Onderaan: losse, onregelmatige cellen. De ruimte tussen de cellen heet de <b>intercellulaire ruimte</b>. Daarin verspreiden CO₂, O₂ en waterdamp zich.'},
    {id:'nerf', naam:'vaatbundel (nerf)', kleur:'#fde68a', info:'Een <b>nerf</b> is een vaatbundel in het blad, omringd door een laag cellen. Bovenaan liggen de houtvaten, onderaan de zeefvaten.'},
    {id:'hout', naam:'houtvaten', kleur:'#3b82f6', info:'<b>Houtvaten</b> zijn lange, holle buizen met verstevigde ringen. Ze brengen water en mineralen aan (bovenaan in de nerf).'},
    {id:'zeef', naam:'zeefvaten', kleur:'#f59e0b', info:'<b>Zeefvaten</b> zijn rijen cellen met zeefplaten ertussen. Ze voeren de assimilaten (suikers) af (onderaan in de nerf).'},
    {id:'sluit', naam:'sluitcellen en huidmondjes', kleur:'#15803d', info:'Onderaan in het dekweefsel: twee boonvormige <b>sluitcellen</b> rond een opening, het <b>huidmondje</b>. Langs hier komt CO₂ binnen en gaan O₂ en waterdamp naar buiten.'},
  ];
  const UITY={was:1.8,dek:1.1,pal:0.55,spo:0,nerf:0,hout:0,zeef:0,sluit:1.1};
  let sel=null, uit=0, doelUit=0, yaw=-0.7, pitch=0.45, afstand=17, auto=true, drag=null;
  const groepen={}; const mats=[];   // mats: {mat, laag, kleur}
  const rnd=(n)=>{ const v=Math.sin(n*12.9898+78.233)*43758.5453; return v-Math.floor(v); };

  // afgeronde balk: box met veel onderverdelingen, hoeken naar een bol geduwd
  function rondeBalk(w,h,d,r){
    const g=new THREE.BoxGeometry(w,h,d,6,6,6), p=g.attributes.position, v=new THREE.Vector3(), c=new THREE.Vector3();
    const hw=w/2-r, hh=h/2-r, hd=d/2-r;
    for(let i=0;i<p.count;i++){ v.fromBufferAttribute(p,i);
      c.set(Math.max(-hw,Math.min(hw,v.x)),Math.max(-hh,Math.min(hh,v.y)),Math.max(-hd,Math.min(hd,v.z)));
      v.sub(c).normalize().multiplyScalar(r).add(c); p.setXYZ(i,v.x,v.y,v.z); }
    g.computeVertexNormals(); return g;
  }
  // onregelmatige bol (cel van het los vulweefsel)
  function klont(r,zaad){
    const g=new THREE.SphereGeometry(r,20,14), p=g.attributes.position, v=new THREE.Vector3();
    for(let i=0;i<p.count;i++){ v.fromBufferAttribute(p,i); const n=v.clone().normalize();
      const f=1+0.16*Math.sin(n.x*3+zaad)*Math.cos(n.y*2.5+zaad*1.7)+0.1*Math.sin(n.z*4+zaad*2.3); v.copy(n.multiplyScalar(r*f)); p.setXYZ(i,v.x,v.y,v.z); }
    g.computeVertexNormals(); return g;
  }
  function mat(laag,kleur,o={}){
    const m=new THREE.MeshStandardMaterial(Object.assign({color:kleur,roughness:0.55,metalness:0},o));
    mats.push({m,laag,kleur:new THREE.Color(kleur),op:m.opacity,tr:m.transparent}); return m;
  }
  function groep(laag){ if(!groepen[laag]){ groepen[laag]=new THREE.Group(); groepen[laag].userData.laag=laag; pivot.add(groepen[laag]); } return groepen[laag]; }
  function zet(laag,geo,m,x,y,z,rot){ const me=new THREE.Mesh(geo,m); me.position.set(x-5,y-3,z-3); if(rot) me.rotation.set(...rot); me.userData.laag=laag; groep(laag).add(me); return me; }
  // bladgroenkorrels als één InstancedMesh per laag
  function korrels(laag,lijst){
    const geo=new THREE.SphereGeometry(0.075,10,8), m=mat(laag,'#15803d',{roughness:0.4});
    const im=new THREE.InstancedMesh(geo,m,lijst.length), d=new THREE.Object3D();
    lijst.forEach((q,i)=>{ d.position.set(q[0]-5,q[1]-3,q[2]-3); d.scale.set(1.5,0.8,1); d.rotation.set(q[3]||0,q[4]||0,0); d.updateMatrix(); im.setMatrixAt(i,d.matrix); });
    im.userData.laag=laag; im.userData.dir=Math.sign(lijst.reduce((a,q)=>a+q[1],0)/lijst.length-3)||1; groep(laag).add(im);
  }

  function bouw(){
    klaar=true;
    renderer=new THREE.WebGLRenderer({canvas:cv,antialias:true});
    renderer.setPixelRatio(Math.min(2,window.devicePixelRatio||1)); renderer.setSize(900,640,false);
    renderer.setClearColor(0xf8fafc);
    scene=new THREE.Scene();
    camera=new THREE.PerspectiveCamera(35,900/640,0.1,100);
    scene.add(new THREE.HemisphereLight(0xffffff,0xc7d2c0,0.75));
    const zon=new THREE.DirectionalLight(0xffffff,0.75); zon.position.set(4,10,6); scene.add(zon);
    const terug=new THREE.DirectionalLight(0xffffff,0.25); terug.position.set(-6,-4,-5); scene.add(terug);
    pivot=new THREE.Group(); scene.add(pivot);

    // --- waslaagje: dunne, glanzende, doorzichtige laag boven en onder
    const wm=mat('was','#bae6fd',{transparent:true,opacity:0.45,roughness:0.15});
    zet('was',new THREE.BoxGeometry(10,0.1,6),wm,5,6.08,3); zet('was',new THREE.BoxGeometry(10,0.1,6),wm,5,-0.08,3);
    // --- dekweefsel: platte, afgeronde cellen (boven en onder), zonder bladgroen
    const dm=mat('dek','#e7f5c8',{transparent:true,opacity:0.92,roughness:0.35});
    const gaten=[[2.5,2.5],[2.5,4.5],[7.5,1.5],[7.5,4.5]];
    for(let i=0;i<10;i++) for(let k=0;k<6;k++){
      const w=0.96, x=i+0.5, z=k+0.5;
      zet('dek',rondeBalk(w,0.5,0.94,0.14),dm,x,5.73,z);
      if(gaten.some(([gx,gz])=>Math.abs(gx-x)<0.6&&Math.abs(gz-z)<0.6)) continue;
      zet('dek',rondeBalk(w,0.45,0.94,0.14),dm,x,0.25,z);
    }
    // --- vulweefsel (dicht): lange, afgeronde cellen dicht tegen elkaar, met veel bladgroenkorrels langs de wand
    const pm=mat('pal','#86efac',{transparent:true,opacity:0.8,roughness:0.5});
    const pk=[];
    for(let i=0;i<14;i++) for(let k=0;k<8;k++){
      const x=0.38+i*0.7+(rnd(i*13+k)-0.5)*0.05, z=0.38+k*0.75, h=2.0+rnd(i+k*7)*0.15;
      zet('pal',rondeBalk(0.6,h,0.66,0.26),pm,x,3.35+h/2,z);
      for(let n=0;n<16;n++){ const a=rnd(i*31+k*17+n)*Math.PI*2, yy=3.5+rnd(n*5+i+k*3+n*n)*(h-0.3);
        pk.push([x+Math.cos(a)*0.25,yy,z+Math.sin(a)*0.28,0,a]); }
    }
    korrels('pal',pk);
    // --- vulweefsel (los): onregelmatige cellen met luchtholtes, weinig bladgroen
    const sm=mat('spo','#bbf7d0',{transparent:true,opacity:0.85,roughness:0.6});
    const sk=[];
    for(let i=0;i<10;i++) for(let k=0;k<6;k++) for(let l=0;l<2;l++){
      const x=0.55+i*0.98+(rnd(i*7+k+l)-0.5)*0.3, z=0.5+k*1.0+(rnd(k*3+i+l)-0.5)*0.3, y=1.1+l*1.45+(rnd(i+k*11+l)-0.5)*0.25;
      if(Math.abs(x-6.5)<1.35 && y<3.2) continue;                 // plaats voor de nerf
      if(gaten.some(([gx,gz])=>Math.hypot(gx-x,gz-z)<0.7) && l===0) continue;  // intercellulaire ruimte boven het huidmondje
      const r=0.38+rnd(i*5+k+l*3)*0.08;
      zet('spo',klont(r,i*3+k+l),sm,x,y,z);
      for(let n=0;n<6;n++){ const a=rnd(i*19+k*7+n+l)*Math.PI*2, b=(rnd(n+i+k+l)-0.5)*1.6; sk.push([x+Math.cos(a)*Math.cos(b)*r*0.85,y+Math.sin(b)*r*0.85,z+Math.sin(a)*Math.cos(b)*r*0.85,0,a]); }
    }
    korrels('spo',sk);
    // --- nerf: schede van cellen rond de vaatbundel (loopt in de lengte, langs z)
    const nm=mat('nerf','#fef3c7',{transparent:true,opacity:0.8,roughness:0.6});
    for(let a=0;a<14;a++){ const t=a/14*Math.PI*2; const c=new THREE.CylinderGeometry(0.2,0.2,6,14);
      const me=zet('nerf',c,nm,6.5+Math.cos(t)*1.12,1.95+Math.sin(t)*1.0,3,[Math.PI/2,0,0]); }
    // --- houtvaten: holle buizen met ringen
    const hm=mat('hout','#93c5fd',{transparent:true,opacity:0.75,roughness:0.3,side:THREE.DoubleSide});
    const hr=mat('hout','#1d4ed8',{roughness:0.45});
    [[6.1,2.45,0.27],[6.62,2.6,0.3],[7.05,2.35,0.24]].forEach(([x,y,r])=>{
      zet('hout',new THREE.CylinderGeometry(r,r,6,24,1,true),hm,x,y,3,[Math.PI/2,0,0]);
      for(let z=0.2;z<6;z+=0.3) zet('hout',new THREE.TorusGeometry(r,0.035,8,24),hr,x,y,z);
    });
    // --- zeefvaten: rijen cellen met zeefplaten
    const zm=mat('zeef','#fcd34d',{transparent:true,opacity:0.8,roughness:0.45});
    const zp=mat('zeef','#b45309',{roughness:0.5});
    [[6.2,1.35,0.2],[6.7,1.3,0.18],[7.05,1.55,0.15]].forEach(([x,y,r])=>{
      zet('zeef',new THREE.CylinderGeometry(r,r,6,20),zm,x,y,3,[Math.PI/2,0,0]);
      for(let z=0.5;z<6;z+=1.0) zet('zeef',new THREE.CylinderGeometry(r*1.02,r*1.02,0.05,20),zp,x,y,z,[Math.PI/2,0,0]);
    });
    // --- sluitcellen: twee boonvormen rond het huidmondje, met bladgroenkorrels
    const gm=mat('sluit','#4ade80',{roughness:0.45});
    const gk=[];
    gaten.forEach(([x,z])=>{
      for(const s of [-1,1]){
        const t=new THREE.TorusGeometry(0.3,0.15,14,28,Math.PI);
        t.rotateZ(s>0?-Math.PI/2:Math.PI/2); t.scale(1,1.55,1); t.rotateX(-Math.PI/2);
        zet('sluit',t,gm,x,0.25,z);
        for(let n=0;n<4;n++){ const a=(n+0.5)/4*Math.PI-Math.PI/2; gk.push([x+s*0.3*Math.cos(a),0.25,z+0.46*Math.sin(a)]); }
      }
    });
    korrels('sluit',gk);
    // --- klikken op een structuur
    const ray=new THREE.Raycaster(), muis=new THREE.Vector2();
    cv.addEventListener('click',e=>{ if(versleept) return;
      const r=cv.getBoundingClientRect(); muis.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);
      ray.setFromCamera(muis,camera); const hit=ray.intersectObjects(pivot.children,true).find(h=>!sel||h.object.userData.laag===sel||true);
      kies(hit?hit.object.userData.laag:null); });
  }

  function kleuren(){
    const grijs=new THREE.Color('#d5dbe1');
    mats.forEach(o=>{
      const actief = !sel || o.laag===sel || (sel==='nerf' && (o.laag==='hout'||o.laag==='zeef'));
      o.m.opacity=o.op; o.m.transparent=o.tr;
      if(!sel){ o.m.color.copy(o.kleur); o.m.emissive.set(0x000000); }
      else if(actief){ o.m.color.copy(o.kleur); o.m.emissive.copy(o.kleur); o.m.emissiveIntensity=0.35; if(o.tr) o.m.opacity=Math.max(o.op,0.95); }
      else { o.m.color.copy(o.kleur).lerp(grijs,0.85); o.m.emissive.set(0x000000); }
      o.m.needsUpdate=true;
    });
  }
  // zet de camera zo dat het gekozen weefsel goed zichtbaar is
  const ZICHT={sluit:[-0.7,-0.75],spo:[-0.7,-0.25],nerf:[0.25,0.15],hout:[0.25,0.15],zeef:[0.25,0.15]};
  function render(){
    if(!renderer) return;
    Object.values(groepen).forEach(g=>{ const l=g.userData.laag, s=(l==='was'||l==='dek'||l==='sluit')?1:1;
      // boven en onder uit elkaar: alles boven de helft omhoog, eronder omlaag
      g.children.forEach(c=>{ if(c.userData.y0===undefined) c.userData.y0=c.position.y; c.position.y=c.userData.y0+uit*(UITY[l]||0)*(c.userData.dir||(c.userData.y0>0?1:-1)); });
    });
    camera.position.set(Math.sin(yaw)*Math.cos(pitch)*afstand, Math.sin(pitch)*afstand, Math.cos(yaw)*Math.cos(pitch)*afstand);
    camera.lookAt(0,0,0);
    renderer.render(scene,camera);
  }
  function kies(l){
    sel = sel===l ? null : l;
    ctl.querySelectorAll('[data-l]').forEach(x=>x.classList.toggle('on',x.dataset.l===sel));
    const L=LAGEN.find(x=>x.id===sel); $('b3-read').innerHTML=L?`<b>${L.naam}</b><br>${L.info}`:'Klik op een weefsel, in de lijst of in de tekening.';
    if(sel && ZICHT[sel]){ auto=false; $('b3-auto').textContent='⟳ Automatisch draaien'; [yaw,pitch]=ZICHT[sel]; }
    kleuren(); render();
  }
  // ----- besturing
  ctl.innerHTML=`<div class="ctrl-row"><button class="btn" id="b3-auto">⏸ Stop met draaien</button><button class="btn" id="b3-uit">Lagen uit elkaar</button></div>
    <div class="chips" id="b3-chips">${LAGEN.map(l=>`<button class="chip" data-l="${l.id}" style="border-left:10px solid ${l.kleur}">${l.naam}</button>`).join('')}</div>
    <div class="readout" id="b3-read">Klik op een weefsel, in de lijst of in de tekening.</div>
    <div class="note">Sleep om te draaien, scroll om te zoomen. Een gekozen weefsel licht op in zijn eigen kleur; de rest wordt grijs. Bij sommige weefsels draait het blad zodat je ze goed ziet.</div>`;
  ctl.querySelectorAll('[data-l]').forEach(b=>b.onclick=()=>kies(b.dataset.l));
  $('b3-uit').onclick=()=>{ doelUit=doelUit?0:1; $('b3-uit').textContent=doelUit?'Lagen samen':'Lagen uit elkaar'; };
  $('b3-auto').onclick=()=>{ auto=!auto; $('b3-auto').textContent=auto?'⏸ Stop met draaien':'⟳ Automatisch draaien'; };
  let versleept=false;
  cv.addEventListener('pointerdown',e=>{ drag={x:e.clientX,y:e.clientY}; versleept=false; cv.setPointerCapture(e.pointerId); cv.style.cursor='grabbing'; });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const dx=e.clientX-drag.x, dy=e.clientY-drag.y; if(Math.abs(dx)+Math.abs(dy)>3){ versleept=true; auto=false; $('b3-auto').textContent='⟳ Automatisch draaien'; }
    yaw-=dx*0.01; pitch=Math.max(-1.3,Math.min(1.3,pitch+dy*0.01)); drag={x:e.clientX,y:e.clientY}; render(); });
  cv.addEventListener('pointerup',()=>{ drag=null; cv.style.cursor='grab'; });
  cv.addEventListener('wheel',e=>{ e.preventDefault(); afstand=Math.max(9,Math.min(30,afstand*(e.deltaY<0?0.9:1.1))); render(); },{passive:false});
  let last=performance.now();
  (function lus(now){ const dt=Math.min(0.05,(now-last)/1000); last=now;
    if(renderer && $('blad3d-wrap').style.display!=='none' && $('p2').classList.contains('active')){ let ver=false; if(auto){ yaw+=dt*0.3; ver=true; } if(Math.abs(uit-doelUit)>0.001){ uit+=(doelUit-uit)*Math.min(1,dt*5); ver=true; } if(ver) render(); }
    requestAnimationFrame(lus); })(last);
})();

