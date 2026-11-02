function hiDPI(canvas){
  const dpr=window.devicePixelRatio||1, w=canvas.width, h=canvas.height;
  canvas.width=w*dpr; canvas.height=h*dpr;
  const ctx=canvas.getContext('2d'); ctx.scale(dpr,dpr);
  canvas._w=w; canvas._h=h; return ctx;
}
function arrow(ctx,x1,y1,x2,y2,color,width=4,label='',lx=0,ly=-12){
  const len=Math.hypot(x2-x1,y2-y1); if(len<2) return;
  const a=Math.atan2(y2-y1,x2-x1), hs=Math.min(14,4+width*2.2);
  ctx.save(); ctx.strokeStyle=color; ctx.fillStyle=color; ctx.lineWidth=width; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-Math.cos(a)*hs*0.8,y2-Math.sin(a)*hs*0.8); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x2,y2);
  ctx.lineTo(x2-hs*Math.cos(a-0.42),y2-hs*Math.sin(a-0.42));
  ctx.lineTo(x2-hs*Math.cos(a+0.42),y2-hs*Math.sin(a+0.42)); ctx.closePath(); ctx.fill();
  if(label){ ctx.font='700 15px Inter, sans-serif'; ctx.textAlign='center'; ctx.fillText(label,(x1+x2)/2+lx,(y1+y2)/2+ly); }
  ctx.restore();
}
function text(ctx,t,x,y,{size=14,weight=500,color='#1D2A36',align='left'}={}){
  ctx.save(); ctx.font=`${weight} ${size}px Inter, sans-serif`; ctx.fillStyle=color; ctx.textAlign=align; ctx.fillText(t,x,y); ctx.restore();
}
function roundRect(ctx,x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
const fmt=(v,d=1)=>v.toFixed(d).replace('.',',').replace('-0,0','0,0');
