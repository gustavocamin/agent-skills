---
name: mockup-telas
description: Faz o mockup clicável das telas novas antes do código — casos de uso, mapa das telas em Mermaid e um HTML estático por tela e estado (vazio, carregando, erro, sucesso), ligados por links, no celular e no desktop, com o CSS do próprio app quando ele existe — e para no ok do dono. Use quando uma spec prevê tela nova ou um grupo de mockups, quando pedirem mockup, wireframe, protótipo, fluxo de telas, mapa de telas ou jornada do usuário, ou antes de implementar uma tela nova que ainda não tem mockup aprovado.
---

# Mockup de telas

O mockup existe para decidir antes do código o que a tela mostra, em que ordem, o que cada toque faz e como fica cada estado. Ele não é o produto: é barato de mudar e caro de pular.

Num repo spec-first, esta skill é o grupo de mockups da feature: leia o `AGENTS.md` e a spec (`plan.md` e `requirements.md`) antes, e mexa só no `Toca` do grupo.

## Onde fica

- O destino é o que a spec disser. Sem spec, siga a convenção do repo (no app do apê, `docs/<id>/mockups/`) ou use `docs/mockups/<tema>/`.
- A entrada são os requisitos e os aceites da spec. Sem spec, pergunte em uma rodada (3 perguntas, no máximo) quem usa a tela, o que precisa conseguir fazer e o que acontece quando dá errado.

## Passos

1. **Casos de uso.** No `README.md` da pasta, uma lista curta: ID, quem, objetivo, passos principais e caminhos de erro, cada um ligado aos requisitos (R1, R2…). Se eles não vieram de uma spec aprovada, mostre a lista e espere a confirmação antes de desenhar.
2. **Mapa das telas.** No mesmo README, um `flowchart` Mermaid com todas as telas e as setas de navegação; acima de uns 15 nós, divida em subfluxos. Um `stateDiagram-v2` só para a tela com mais de três estados ou transições que não sejam óbvias. Sem diagrama de sequência: o contrato entre cliente e servidor é da spec (Interfaces), não do mockup.
3. **Telas.** Um HTML por tela; um estado é um arquivo próprio ou um bloco marcado na mesma tela.
   - **Cara do app:** se o app já tem folha de estilo e tokens (ex.: `src/styles.css`), ligue o mockup a ela por caminho relativo e ponha só os blocos novos num `mockups.css`, para que o ok valha para o que será construído. Em tela nova de um app sem identidade visual, a direção (paleta, tipo, layout) vem antes da skill `frontend-design`; se o dono só quer decidir estrutura, wireframe neutro em tons de cinza.
   - **Estático e local:** sem rede, sem fonte ou script externo, sem `localStorage` nem cookie, sem dado real. Exemplos sintéticos e plausíveis do domínio, no idioma do app. JavaScript só no índice, se precisar.
   - **Todos os estados:** primeira vez (vazio), carregando, erro de campo, erro do servidor ou sem conexão, sucesso e os que os requisitos pedirem. Faltar um estado é o defeito mais comum.
   - **Clicável:** botão que navega, aba, item de lista, cartão e voltar são `<a href="outra-tela.html">`. Nenhuma tela sem saída, nenhum `href="#"` em algo que leva a outra tela.
   - **Texto final:** rótulos, botões e mensagens já no texto que o código vai usar; o botão diz o que acontece ("Salvar medidas", não "Enviar"), e o mesmo nome segue no fluxo.
   - **Base de acessibilidade:** rótulo em todo campo, foco visível, alvo de toque de pelo menos 44 px, estado dito em texto e não só em cor, contraste AA.
4. **Índice.** `index.html` mostra cada tela na menor largura de celular do projeto (360 px se nada disser) e em 1280 px, lado a lado (iframes). O README traz a tabela: tela, arquivo, estados, requisitos e para onde cada tela leva.
5. **Conferir uma vez.** Rode `python3 <pasta desta skill>/scripts/conferir_mockups.py <pasta dos mockups>` (a pasta é `${CLAUDE_SKILL_DIR}` no Claude Code; no Codex, a deste `SKILL.md`): ele acusa link quebrado, tela sem saída, tela que o índice não alcança e recurso externo. Abra no navegador (Playwright com o Chromium da máquina, se houver) e tire screenshots nas duas larguras: sem rolagem horizontal, nada cortado. Corrija tudo numa rodada e confira de novo uma vez; não fique polindo.
6. **Parar no ok.** Mostre o índice e as screenshots e peça o ok do dono. Mudança pedida é uma nova rodada, com um novo commit e um novo ok. O ok é registrado como relato, com data e o commit dos mockups (num repo spec-first, no `plan.md` e no `validation.md`, por quem integra). Código da tela só depois do ok.

## Depois do ok

- Quem implementa segue o mockup aprovado: texto, ordem e estados. O que mudar na implementação entra no `plan.md` como "Decidido na implementação".
- Ajuste de texto ou layout numa tela que já existe não pede mockup novo, salvo se a constituição do projeto disser outra coisa.
- Figma só se o dono pedir: com o MCP do Figma conectado, leve as telas a partir do HTML, seguindo as skills da própria integração.
