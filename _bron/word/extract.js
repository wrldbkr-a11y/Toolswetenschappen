// Haalt de structuur van een cursuspagina op (leerkrachtweergave) en maakt PNG's van de figuren.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGINAS = process.argv.slice(2);
const UIT = '/home/claude/word/data';
fs.mkdirSync(UIT + '/fig', { recursive: true });

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1200 }, deviceScaleFactor: 2.5 });
  const alles = [];
  for (const naam of PAGINAS) {
    await p.goto('file:///home/claude/toolswetenschappen/' + naam + '.html?leerkracht');
    await p.waitForTimeout(900);
    // figuren: svg zonder rand fotograferen
    const figs = await p.$$('figure.figuur');
    const figInfo = [];
    for (let i = 0; i < figs.length; i++) {
      const el = await figs[i].$('svg');
      await el.evaluate(e => { e.style.border = 'none'; e.style.background = '#fff'; });
      const f = `${UIT}/fig/${naam}_${i}.png`;
      await el.screenshot({ path: f });
      const bb = await el.boundingBox();
      figInfo.push({ f, w: bb.width, h: bb.height });
    }
    // oplossingsfiguren (in redeneringen): los renderen, want ze kunnen verborgen zijn
    const oplHtml = await p.$$eval('figure.oplfig svg', a => a.map(s => s.outerHTML));
    const oplInfo = [];
    if (oplHtml.length) {
      const q = await b.newPage({ deviceScaleFactor: 2.5 });
      for (let i = 0; i < oplHtml.length; i++) {
        await q.setContent('<body style="margin:0;background:#fff">' + oplHtml[i] + '</body>');
        const el = await q.$('svg'); const f = `${UIT}/fig/${naam}_opl${i}.png`;
        await el.screenshot({ path: f }); const bb = await el.boundingBox(); oplInfo.push({ f, w: bb.width, h: bb.height });
      }
      await q.close();
    }
    await p.evaluate(v => { window.MET_EDI = v; }, !!process.env.EDI);
    const data = await p.evaluate(() => {
      let oplNr = 0;
      const oplVan = red => { const n = red.querySelectorAll('figure.oplfig').length; const r = []; for (let k = 0; k < n; k++) r.push(oplNr++); return r; };
      const runsVan = (node, fl = {}) => {
        const out = [];
        node.childNodes.forEach(n => {
          if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' '); if (t) out.push({ t, ...fl }); return; }
          if (n.nodeType !== 1) return;
          const tag = n.tagName;
          if (tag === 'BR') { out.push({ br: true }); return; }
          if (['BUTTON', 'SCRIPT', 'OL', 'UL', 'TABLE', 'FIGURE', 'svg'].includes(tag)) return;
          const f2 = { ...fl };
          if (tag === 'B' || tag === 'STRONG') f2.b = true;
          if (tag === 'I' || tag === 'EM') f2.i = true;
          if (tag === 'SUB') f2.sub = true;
          if (tag === 'SUP') f2.sup = true;
          if (tag === 'A') { f2.link = n.href; }
          out.push(...runsVan(n, f2));
        });
        return out;
      };
      const trim = r => { if (r.length && r[0].t) r[0].t = r[0].t.replace(/^\s+/, ''); const l = r[r.length - 1]; if (l && l.t) l.t = l.t.replace(/\s+$/, ''); return r.filter(x => x.br || x.t); };
      let figNr = 0;
      const items = el => {
        const out = []; let inline = [];
        const flush = () => { const r = trim(inline); if (r.length) out.push({ type: 'p', runs: r }); inline = []; };
        el.childNodes.forEach(n => {
          if (n.nodeType === 3) { if (n.textContent.trim()) inline.push({ t: n.textContent.replace(/\s+/g, ' ') }); return; }
          if (n.nodeType !== 1) return;
          const tag = n.tagName, c = n.classList;
          if (['B', 'I', 'STRONG', 'EM', 'SUB', 'SUP', 'SPAN', 'BR'].includes(tag) && !c.contains('stap')) {
            if (tag === 'BR') inline.push({ br: true }); else inline.push(...runsVan({ childNodes: [n] })); return;
          }
          flush();
          if (n.hidden && !c.contains('redenering')) return;
          if (tag === 'STYLE' || tag === 'SCRIPT') return;
          if (c.contains('edi')) { if (window.MET_EDI) out.push({ type: 'kader', kop: n.querySelector('.kop').textContent, body: items(n) }); return; }
          if (tag === 'P') { if (n.querySelector('button')) return; const r = trim(runsVan(n)); if (r.length) out.push({ type: 'p', runs: r, cls: n.className }); }
          else if (tag === 'H3' || tag === 'H4') out.push({ type: tag.toLowerCase(), t: n.textContent.trim() });
          else if (tag === 'UL' || tag === 'OL') out.push({ type: tag === 'UL' ? 'ul' : 'ol', letters: n.getAttribute('type') === 'a', items: [...n.children].map(li => trim(runsVan(li))) });
          else if (tag === 'TABLE') out.push({ type: 'table', grid: n.classList.contains('grid'), rows: [...n.querySelectorAll('tr')].map(tr => [...tr.children].map(td => trim(runsVan(td)))) });
          else if (tag === 'FIGURE') out.push({ type: 'fig', i: figNr++, liggend: n.classList.contains('liggend'), cap: trim(runsVan(n.querySelector('figcaption'))) });
          else if (tag === 'A' && c.contains('toolknop')) out.push({ type: 'tool', t: n.textContent.replace('▶', '').trim(), href: n.href });
          else if (c.contains('def')) out.push({ type: 'def', wet: c.contains('wet'), kop: n.querySelector('.kop').textContent, body: items(n) });
          else if (c.contains('vgl')) out.push({ type: 'vgl', runs: trim(runsVan(n.querySelector('.f'))), n: (n.querySelector('.n') || {}).textContent || '' });
          else if (c.contains('voorbeeld') || c.contains('kader') || c.contains('verdieping')) out.push({ type: c.contains('voorbeeld') ? 'vb' : c.contains('kader') ? 'kader' : 'verd', kop: n.querySelector('.kop').textContent, body: items(n) });
          else if (c.contains('denk')) {
            const red = n.querySelector('.redenering');
            out.push({ type: 'denk', vraag: trim(runsVan(n.querySelector('.vraag p'))), stappen: [...red.querySelectorAll('li')].map(li => ({ stap: li.querySelector('.stap').textContent, runs: trim(runsVan(li)).filter(r => r.t !== li.querySelector('.stap').textContent) })), besluit: trim(runsVan(red.querySelector('.besluit'))), opl: oplVan(red) });
          }
          else if (c.contains('oef')) {
            const red = n.querySelector('.redenering');
            out.push({ type: 'oef', nr: n.querySelector('.titel .nr').textContent, titel: n.querySelector('.titel').textContent.replace(n.querySelector('.titel .nr').textContent, '').trim(), body: items(n.querySelector('.tekst')),
              stappen: [...red.querySelectorAll('li')].map(li => ({ stap: li.querySelector('.stap').textContent, runs: trim(runsVan(li)).filter(r => r.t !== li.querySelector('.stap').textContent) })), besluit: trim(runsVan(red.querySelector('.besluit'))), opl: oplVan(red) });
          }
          else if (c.contains('kop') || c.contains('onder') || c.contains('stappenplan') || c.contains('slotje') || c.contains('gesloten-deel')) return;
          else out.push(...items(n));
        });
        flush();
        return out;
      };
      const secties = [...document.querySelectorAll('section.blok')].map(s => {
        const h2 = s.querySelector(':scope > h2'), nr = h2.querySelector('.nr');
        const kids = document.createElement('div');
        [...s.children].filter(c => c !== h2).forEach(c => kids.appendChild(c.cloneNode(true)));
        return { id: s.id, nr: nr ? nr.textContent : '', titel: h2.textContent.replace(nr ? nr.textContent : '', '').trim(), body: items(kids) };
      });
      return { titel: document.querySelector('h1').textContent, eyebrow: document.querySelector('.eyebrow').textContent, intro: document.querySelector('.intro').innerText, secties, cornell: CORNELL };
    });
    data.figs = figInfo; data.opl = oplInfo; data.naam = naam;
    alles.push(data);
  }
  fs.writeFileSync(UIT + '/cursus.json', JSON.stringify(alles, null, 1));
  console.log('ok', alles.map(a => a.titel + ':' + a.secties.length + ' secties, ' + a.figs.length + ' fig'));
  await b.close();
})();
