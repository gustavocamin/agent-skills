// Sonda de iOS para o playwright-cli: playwright-cli run-code --filename=<este arquivo>
// Roda na página aberta e devolve, em JSON, o que costuma quebrar no Safari do iPhone.
// Níveis: "erro" quebra o uso no iPhone; "aviso" costuma quebrar; "info" é para conferir à mão.
async page => page.evaluate(() => {
  const problemas = [];
  // No celular, innerWidth cresce com o conteúdo que vaza; a largura da tela é o clientWidth.
  const W = document.documentElement.clientWidth;
  const add = (nivel, regra, detalhe, alvo) => problemas.push({ nivel, regra, detalhe, ...(alvo ? { alvo } : {}) });
  const nomear = el => {
    const id = el.id ? `#${el.id}` : '';
    const texto = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('name') || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return `${el.tagName.toLowerCase()}${id}${texto ? ` "${texto}"` : ''}`;
  };
  const visivel = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  };

  // CSS das folhas do mesmo domínio (as de outro domínio não deixam ler as regras).
  const regras = [];
  const juntar = lista => {
    for (const r of lista) {
      regras.push(r.cssText);
      if (r.cssRules) juntar(r.cssRules);
    }
  };
  let folhasIlegiveis = 0;
  for (const folha of document.styleSheets) {
    try { juntar(folha.cssRules); } catch { folhasIlegiveis++; }
  }
  const css = regras.join('\n');
  if (folhasIlegiveis) add('info', 'css-ilegivel', `${folhasIlegiveis} folha(s) de outro domínio não foram lidas`);

  // Viewport.
  const meta = document.querySelector('meta[name="viewport"]');
  const conteudo = (meta?.content || '').replace(/\s/g, '').toLowerCase();
  if (!meta) add('erro', 'viewport', 'sem <meta name="viewport">: o Safari renderiza a 980 px e encolhe');
  else {
    if (!conteudo.includes('width=device-width')) add('erro', 'viewport', `sem width=device-width (${meta.content})`);
    if (/user-scalable=(no|0)|maximum-scale=1(\.0)?(,|$)/.test(conteudo)) add('aviso', 'viewport-zoom', `bloqueia o zoom (${meta.content}); o iOS ignora em parte, e quem precisa de zoom perde`);
  }
  const usaSafeArea = /env\(\s*safe-area-inset/.test(css);
  if (usaSafeArea && !conteudo.includes('viewport-fit=cover')) add('aviso', 'safe-area', 'usa env(safe-area-inset-*) sem viewport-fit=cover: os valores ficam 0');

  // Elementos fixos colados na borda: no iPhone ficam sob o notch, a ilha ou a barra de gestos.
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el);
    if ((s.position === 'fixed' || s.position === 'sticky') && visivel(el)) {
      const r = el.getBoundingClientRect();
      const noTopo = r.top <= 0 && s.position === 'fixed';
      const noPe = r.bottom >= innerHeight - 1;
      if ((noTopo || noPe) && !usaSafeArea) add('aviso', 'safe-area', `${s.position} na borda ${noTopo ? 'de cima' : 'de baixo'} sem env(safe-area-inset-*) no CSS`, nomear(el));
    }
  }

  // Campos com fonte menor que 16 px: o Safari dá zoom ao focar.
  for (const el of document.querySelectorAll('input, select, textarea')) {
    if (!visivel(el) || ['checkbox', 'radio', 'range', 'color', 'hidden', 'submit', 'button', 'reset', 'image', 'file'].includes(el.type)) continue;
    const px = parseFloat(getComputedStyle(el).fontSize);
    if (px < 16) add('erro', 'zoom-no-foco', `fonte de ${px}px num campo (mínimo 16px, ou o Safari dá zoom ao focar)`, nomear(el));
    if (el.type === 'number') add('info', 'teclado', 'type=number: em pt-BR prefira type=text com inputmode="decimal" (vírgula) ou "numeric"', nomear(el));
  }

  // Alvos de toque menores que 44 x 44 pt (links dentro de texto corrido ficam de fora).
  const alvos = 'a[href], button, select, summary, [role="button"], [role="tab"], [role="link"], input[type="checkbox"], input[type="radio"], input[type="submit"], input[type="button"]';
  for (const el of document.querySelectorAll(alvos)) {
    if (!visivel(el)) continue;
    const s = getComputedStyle(el);
    if (el.tagName === 'A' && s.display === 'inline' && el.closest('p, li, td, label')) continue;
    let r = el.getBoundingClientRect();
    if (['checkbox', 'radio'].includes(el.type) && el.closest('label')) r = el.closest('label').getBoundingClientRect();
    if (r.width < 44 || r.height < 44) add('aviso', 'alvo-de-toque', `${Math.round(r.width)}x${Math.round(r.height)} px (mínimo 44x44)`, nomear(el));
  }

  // Rolagem horizontal.
  const largura = document.documentElement.scrollWidth;
  if (largura > W + 1) {
    add('erro', 'rolagem-horizontal', `a página tem ${largura}px numa tela de ${W}px`);
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      // Só o primeiro da cadeia que passa da borda: o pai ainda cabe.
      if (r.right > W + 1 && visivel(el) && el.parentElement.getBoundingClientRect().right <= W + 1) {
        add('erro', 'rolagem-horizontal', `passa da borda em ${Math.round(r.right - W)}px`, nomear(el));
      }
    }
  }

  // Altura de tela: 100vh no iOS inclui a área atrás das barras do Safari.
  if (/(^|[^\w-])100vh/.test(css) && !/\d(dvh|svh)/.test(css)) add('aviso', '100vh', '100vh no CSS: no Safari corta o fim da tela; use 100dvh (ou 100svh) com 100vh antes como reserva');

  // Movimento sem alternativa reduzida.
  if (/(animation|transition)\s*:/.test(css) && !/prefers-reduced-motion/.test(css)) add('aviso', 'movimento', 'há animation/transition e nenhuma regra @media (prefers-reduced-motion)');

  // Interação só por hover: no toque, o hover gruda ou não existe.
  if (/:hover/.test(css) && !/hover:\s*hover/.test(css)) add('info', 'hover', 'há :hover sem @media (hover: hover): confira que nada só aparece no hover');

  // Tela de Início e tema.
  if (!document.querySelector('link[rel="apple-touch-icon"]')) add('info', 'tela-de-inicio', 'sem <link rel="apple-touch-icon">: o atalho na Tela de Início vira uma miniatura da página');
  if (!document.querySelector('meta[name="theme-color"]') && !/prefers-color-scheme/.test(css)) add('info', 'tema', 'sem theme-color e sem @media (prefers-color-scheme): confira o modo escuro do iPhone');

  const ordem = { erro: 0, aviso: 1, info: 2 };
  problemas.sort((a, b) => ordem[a.nivel] - ordem[b.nivel]);
  return {
    url: location.href,
    tela: { largura: W, altura: innerHeight, dpr: devicePixelRatio, toque: navigator.maxTouchPoints > 0 },
    total: { erro: problemas.filter(p => p.nivel === 'erro').length, aviso: problemas.filter(p => p.nivel === 'aviso').length, info: problemas.filter(p => p.nivel === 'info').length },
    problemas,
  };
})
