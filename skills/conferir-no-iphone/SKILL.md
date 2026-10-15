---
name: conferir-no-iphone
description: Confere uma tela web como no iPhone antes do aceite físico — abre como iPhone pelo playwright-cli (WebKit na máquina, Chromium com perfil de iPhone na cloud), roda a sonda de iOS (zoom em campo com fonte menor que 16 px, safe area, 100vh, alvos de toque, rolagem horizontal, teclado), tira screenshots de cada estado com o commit e monta a lista do aceite físico. Use quando uma tela nova ou alterada vai para o aceite no iPhone, ao validar uma feature com tela, ao conferir mockups de um app usado no celular, quando pedirem para testar no iPhone, no celular ou no Safari, ou quando algo quebra só no iPhone.
---

# Conferir no iPhone

A emulação acha o que é de layout e de CSS: largura, safe area, fonte dos campos, alvos de toque, estados. Ela não prova o Safari real (teclado virtual, gestos, Tela de Início, desempenho). O aceite físico continua, e esta skill chega a ele com os defeitos de CSS já resolvidos e a lista do que só o aparelho mostra.

Só servidor local e dados sintéticos: nunca o Site publicado nem outro ambiente real. Tela que exige o login do dono fica para o aceite físico.

## Passos

1. **Ferramenta.** `playwright-cli --version`. Sem ela: num projeto com Playwright, `npx --no-install playwright cli`; senão, peça o ok para `npm install -g @playwright/cli@latest` (skill `playwright-cli`).
2. **Servir.** O navegador recusa `file://`. Mockups: `python3 -m http.server 8765 --bind 127.0.0.1` na raiz do repo, para que o caminho relativo do CSS do app funcione. App: o comando local do projeto (`AGENTS.md`, "Comandos"), com dados sintéticos.
3. **Abrir como iPhone.**
   - Na máquina, com o motor do Safari: `playwright-cli install-browser webkit` uma vez (pede ok) e `playwright-cli open --browser=webkit --device="iPhone 15" <url>`.
   - Na cloud, o WebKit não baixa (Claude Code na web, conferido em 15/10/2026). Use o Chromium da imagem com o perfil do iPhone (393 x 659, tela 3x, toque, user agent do iPhone): grave `{"browser": {"browserName": "chromium", "launchOptions": {"executablePath": "/opt/pw-browsers/chromium"}}}` num arquivo do scratchpad e rode `playwright-cli open --config=<arquivo> --device="iPhone 15" <url>`.
   - Diga no registro qual motor foi usado. Se o projeto fixa uma largura menor (360 px), repita com `playwright-cli resize 360 740`.
4. **Cada tela e estado.** A lista vem do índice dos mockups ou dos requisitos de tela da spec. Para cada um: `playwright-cli goto <url>`; o estado que depende de ação (erro de campo, resultado) se monta com `snapshot`, `fill` e `click`; depois `playwright-cli --raw run-code --filename=<pasta desta skill>/scripts/sonda_ios.js` (a pasta é `${CLAUDE_SKILL_DIR}` no Claude Code; no Codex, a deste `SKILL.md`) e `playwright-cli screenshot --filename=<destino>/<tela>-<estado>.png`.
5. **Ler a sonda.** Ela devolve JSON com `erro`, `aviso` e `info`:
   - `erro` quebra o uso no iPhone (sem viewport, campo com fonte menor que 16 px, rolagem horizontal): é gap, corrigido antes do aceite;
   - `aviso` costuma quebrar (safe area, 100vh sem dvh, alvo de toque menor que 44 x 44, movimento sem `prefers-reduced-motion`, zoom bloqueado): corrija ou justifique no registro;
   - `info` vira item da lista do aceite físico (Tela de Início, modo escuro, hover, teclado).
6. **Registrar.** Screenshots e o JSON da sonda ficam no repo, na pasta que a spec disser (num repo spec-first, perto do `validation.md` da feature, por exemplo `specs/features/<ID>/evidencias/iphone/`), com o commit conferido no README da pasta ou no `validation.md`. Prova só numa pasta temporária não vale.
7. **Lista do aceite físico.** Monte a tabela para o dono marcar no aparelho, com o caso concreto de cada item, o modelo do iPhone, a versão do iOS e o commit. Inclua o que a emulação não mostra:
   - abrir pelo Safari e, se o projeto usa, pela Tela de Início (ícone, barra de status);
   - focar cada campo: sem zoom, o teclado certo (decimal com vírgula, numérico, email), o campo e o botão principal visíveis acima do teclado;
   - rolar até o fim de cada tela: nada preso atrás da barra do Safari ou da barra de gestos;
   - voltar com o gesto da borda: o estado fica ou se perde como a spec diz;
   - modo escuro, texto maior (Ajustes > Acessibilidade) e Reduzir Movimento ligados;
   - sem rede (modo avião): a mensagem de erro do requisito;
   - com login, a sessão depois de fechar e abrir o Safari.
8. **Fechar.** `playwright-cli close` e pare o servidor local.

O aceite marcado pelo dono vale só para o commit conferido: mudou a tela, o item reabre.
