const scenes=[...document.querySelectorAll('.scene')];
const nav=document.getElementById('nav'), catNav=document.getElementById('catnav');
const categories=[
  {id:'kracht',label:'Wat is een kracht?'},
  {id:'traagheid',label:'Traagheid'},
  {id:'fr',label:'Resulterende kracht en beweging'},
  {id:'leven',label:'Dagelijks leven'},
  {id:'oefenen',label:'Oefenen'},
];
let currentIndex=0, activeCat=scenes[0].dataset.cat;
function renderCatNav(){
  catNav.innerHTML='';
  categories.forEach(cat=>{
    const b=document.createElement('button'); b.textContent=cat.label;
    b.classList.toggle('active',cat.id===activeCat);
    b.addEventListener('click',()=>{ const i=scenes.findIndex(s=>s.dataset.cat===cat.id); if(i>=0) activate(i); });
    catNav.appendChild(b);
  });
}
function renderSectionNav(){
  nav.innerHTML='';
  scenes.forEach((sc,i)=>{
    if(sc.dataset.cat!==activeCat) return;
    const b=document.createElement('button');
    b.innerHTML='<span class="nr">'+(i+1)+'</span>'+sc.dataset.title;
    b.classList.toggle('active',i===currentIndex);
    b.addEventListener('click',()=>activate(i));
    nav.appendChild(b);
  });
}
function activate(i){
  currentIndex=i;
  scenes.forEach((sc,j)=>sc.classList.toggle('active',j===i));
  activeCat=scenes[i].dataset.cat;
  renderCatNav(); renderSectionNav();
}
document.querySelectorAll('.scene').forEach((sc,i)=>{ const n=sc.querySelector('.scene-head .num'); if(n) n.textContent=i+1; });
activate(0);
// directe link naar een sectie, bv. krachten-beweging.html#s3
if(location.hash){ const i=scenes.findIndex(sc=>sc.id===location.hash.slice(1)); if(i>=0) activate(i); }
const isActive=id=>document.getElementById(id).classList.contains('active');
