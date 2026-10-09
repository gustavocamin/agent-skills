---
name: vault-automation
description: Triagem de 00. Inbox/ + Readwise/, roteamento de Inbox para o PARA, criação de stubs para a camada de conhecimento (Sources/Evergreen/MOC), auditoria semanal, mapa somente-leitura do PARA e preparação de sessão de destilação de uma Source. Use quando o usuário invocar /triage-inbox, /process-inbox, /audit-vault, /map-territory, /next-source, /new-source-note, /new-evergreen-note ou /new-moc.
---

# Vault Automation Skill

Oito automações preparation-only para o PARA e a camada de conhecimento do
vault (ver CLAUDE.md, seção "A camada de conhecimento: princípios
invioláveis"):

1. `/triage-inbox` — triagem conjunta de `00. Inbox/` + `Readwise/`, em buckets retain/seed/ref/discard
2. `/process-inbox` — roteia o que sobra do Inbox entre PARA (Projects/Areas/Resources) e a camada de conhecimento
3. `/audit-vault` — auditoria semanal de saúde de `00. Notes/` + `00. Sources/` + resgate gradual do DMZ
4. `/map-territory` — inventário somente-leitura do PARA, nunca cria/move/edita nada
5. `/next-source` — escolhe UMA Source da fila e prepara a sessão de destilação
6. `/new-source-note` — cria manualmente um stub em `00. Sources/`
7. `/new-evergreen-note` — cria manualmente um rascunho em `00. Notes/`
8. `/new-moc` — cria um MOC, só em squeeze point genuíno

Nenhum comando aqui escreve o conteúdo intelectual de uma nota — só prepara
o material para o usuário fazer o trabalho generativo.

**Subagente de varredura:** para as fases de leitura ampla de
`/audit-vault` e `/map-territory` (contagens, órfãs, links quebrados,
estimativas de bucket, afinidades), delegar ao agente `vault-auditor`
(`.claude/agents/vault-auditor.md`) via Agent tool. Ele só tem ferramentas
de leitura — os princípios invioláveis ficam garantidos por ferramenta, não
só por instrução — e devolve conclusões compactas em vez de despejo de
arquivos. As fases de escrita (relatório, stubs autorizados) continuam na
sessão principal.

**Vault location:** todas as pastas ficam dentro de `second-brain/`
relativo ao diretório de trabalho. Os nomes de pasta usados neste documento
são a forma curta — mapeiam para os nomes reais com prefixo numérico:

| Forma curta       | Caminho real                        |
| ------------------ | ------------------------------------ |
| `Readwise/`         | `second-brain/Readwise/`             |
| `Notes/`            | `second-brain/00. Notes/`            |
| `Sources/`          | `second-brain/00. Sources/`          |
| `Inbox/`            | `second-brain/00. Inbox/`            |
| `Projects/`         | `second-brain/01. Projects/`         |
| `Areas/`            | `second-brain/02. Areas/`            |
| `Areas/Writing/`    | `second-brain/02. Areas/Writing/`    |
| `Areas/Writing/Seeds/` | `second-brain/02. Areas/Writing/Seeds/` |
| `Resources/`        | `second-brain/03. Resources/`        |
| `Archiving/DMZ/`    | `second-brain/04. Archiving/DMZ/`    |
| `Reports/`          | `second-brain/05. Reports/`          |

Frontmatter dos tipos de nota: ver CLAUDE.md, "Convenções → Frontmatter —
camada de conhecimento" (`type: source | evergreen | moc | seed`;
`status` de source: `captured | reading | processing | processed |
archived`; `status` de evergreen: `seedling | developing | evergreen`).

---

## Princípios invioláveis (preparation-only)

Valem para todos os comandos abaixo, sem exceção:

1. **NUNCA escrever o corpo intelectual de uma nota.** O agente cria
   frontmatter, links, stubs e filas — jamais o texto "com minhas
   palavras", jamais resumos que substituam a leitura, jamais respostas a
   perguntas de auto-teste. Todo stub deve conter o campo literal:
   `**Com minhas palavras:** _[escrever aqui]_`
2. **NUNCA deletar nada.** Itens descartáveis vão para uma lista de
   aprovação; só depois de aprovação explícita do usuário movem-se para
   `Archiving/DMZ/` (nunca `rm`, nunca lixeira do sistema).
3. **Os dois pipelines têm regras opostas.** Retenção (`Sources/` →
   `Notes/`): fricção máxima, reescrita humana. Crônica (`Areas/Writing/Seeds/`,
   seeds): fricção zero, texto bruto integral, nunca resumido ou destilado.
   Nunca cruzar os dois.
4. **NUNCA mover ou editar arquivos em `Projects/`, `Areas/` (exceto
   `Areas/Writing/Seeds/`), `Resources/`, `Notes/` sem instrução explícita.** As
   automações só escrevem em: `Notes/` (só com instrução explícita —
   `/new-evergreen-note`, `--scope`, ou relatórios), `Sources/` (stubs
   novos), `Areas/Writing/Seeds/` (só criação/cópia de seeds), `Archiving/DMZ/`
   (só pós-aprovação) e `Reports/`. `/triage-inbox --scope <pasta>` é a
   exceção desenhada para tocar `Projects/`/`Areas/`/`Resources/`: a flag
   É a instrução explícita, mas mesmo assim só **lê** a pasta — nunca
   move, edita ou marca os arquivos originais nela.
5. **Toda execução gera um relatório em `Reports/`** — não só output no
   terminal — para que o resultado seja acionável dentro do Obsidian.
6. **Filas curtas.** Máximo 10 itens acionáveis por relatório. Melhor 10
   itens bem ranqueados que 200 ignoráveis.
7. **No território PARA, classificar e reportar é o padrão; criar stub
   não é.** Um stub em `Sources/` só nasce de: triagem de `Inbox/`/
   `Readwise/`, demanda explícita via `--scope`, ou resgate da auditoria
   ligado a trabalho ativo. Nunca varredura em massa do PARA por conta
   própria.

---

## `/triage-inbox`

**Objetivo:** processar `Inbox/` e `Readwise/` juntos — numa única
passada, não uma triagem por vez —, classificar cada item e preparar os
artefatos para o usuário executar o trabalho generativo. Aceita
`--scope <pasta>` para rodar em modo de extração sobre uma pasta do PARA
em vez do fluxo padrão — ver "Modo `--scope`" abaixo.

### Comportamento

1. Ler todos os arquivos ainda não triados de `Inbox/` e de `Readwise/`
   (marcar os triados com `triaged: true` no frontmatter para
   idempotência). Ignorar itens já com `triaged: true` e os próprios
   relatórios.
2. Para cada highlight (Readwise) ou nota inteira (Inbox — ver regra
   abaixo), classificar em exatamente um bucket:

| Bucket    | Critério                                                                                                                             | Ação do agente                                                                                                                                    |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `retain`  | Afirmação generalizável, conhecimento técnico/conceitual marcado `#retain` OU com estrutura de claim (causa-efeito, princípio, dado) | Criar/atualizar stub em `Sources/<slug-da-fonte>.md` (`type: source`, `status: captured`); anexar o trecho numa seção `## A processar` com o campo "Com minhas palavras" em branco |
| `seed`    | Concreto, sensorial, observacional, narrativo, ou marcado `#seed` — potencial material de crônica                                     | Criar `Areas/Writing/Seeds/YYYY-MM-DD <primeiras palavras>.md` (`type: seed`) com o texto bruto integral. SEM resumir, SEM editar                       |
| `ref`     | Referência utilitária (sintaxe, config, lista, how-to) ou marcado `#ref` — útil achar depois, inútil memorizar                         | Listar para mover a `Archiving/DMZ/` (buscável via Smart Connections)                                                                              |
| `discard` | Redundante com nota existente, trivial, clickbait, sem claim nem imagem concreta                                                       | Listar para aprovação de arquivamento                                                                                                              |

3. Em caso de dúvida entre buckets, preferir `ref` (custo de erro menor:
   continua buscável). Nunca classificar como `discard` em caso de dúvida.
4. **`retain` vai sempre para `Sources/`**, mesmo quando o conteúdo é
   reflexão própria da pessoa, sem fonte externa citada — trate a própria
   nota/conversa como a "fonte" (`author:` pode nomear a origem, ex. "nota
   pessoal", "conversa com X"). Promover a Evergreen é decisão humana
   posterior, durante o processamento da Source Note — nunca uma
   bifurcação automática do agente no momento da triagem.
5. Ao criar stub em `Sources/`: verificar se a fonte já existe (match por
   título/autor); se sim, anexar à existente em vez de duplicar.
   Preencher frontmatter completo.
6. Consultar Smart Connections (ou similaridade por conteúdo) para sugerir
   em cada stub até 3 links `[[Notes/...]]` existentes relacionados — como
   sugestão comentada, não como link definitivo.

### Tratamento de `Inbox/` nesta rodada

Notas do Inbox são captura livre — não vêm pré-fatiadas em highlights.
Classifique a nota **inteira** como um item só:

- `retain`: mesmo fluxo da tabela acima — stub/anexo em `Sources/`. Mover
  a nota original do Inbox para dentro do stub (não deixar cópia solta no
  Inbox depois de incorporada).
- `seed`: mover a nota inteira para `Areas/Writing/Seeds/YYYY-MM-DD <primeiras
  palavras>.md`.
- `ref` / `discard`: não mover nada agora, só listar no relatório para
  aprovação; a nota fica em `Inbox/` até o `--approve`.
- **Tarefa/ação** (não é conhecimento, é algo a fazer): não classificar
  em bucket nenhum — listar em seção própria do relatório ("Ações
  identificadas"). Não mover, não criar stub.
- **Material de projeto/área existente** (a nota claramente pertence a um
  projeto ou área já mapeados): não mover sozinho — propor o destino no
  relatório ("Propostas de destino PARA"); a execução da mudança é do
  `/process-inbox` ou de aprovação manual.

### Modo `--scope <pasta>` (extração, não triagem)

`/triage-inbox --scope "02. Areas/Business"` (ou qualquer pasta do PARA)
roda um modo **diferente e mais restrito**: extração de conhecimento de
notas já organizadas, não triagem de captura solta. Existe porque
`Areas/`, `Projects/` e `Resources/` são protegidas pelo princípio
inviolável #4 — este modo é a única forma explícita e segura de tirar
valor delas sem violar essa regra. Diferenças em relação ao modo padrão:

1. **Nunca marca nada no original, nunca move o arquivo de origem.** PARA
   não é Inbox — a nota continua exatamente onde está. Idempotência aqui
   vem de checar por conteúdo: antes de anexar um trecho extraído a um
   stub, procurar se aquele texto (ou um trecho muito próximo) já foi
   extraído numa rodada anterior; se sim, pular — nunca duplicar.
2. **Só o bucket `retain` (para `Sources/`) e `seed` (cópia para
   `Areas/Writing/Seeds/`) existem neste modo.** Não há `ref` nem `discard` —
   o usuário pediu extração, não arquivamento nem limpeza. `--approve`
   não se aplica ao modo `--scope`.
3. **Relatório com nome da pasta**, separado: `Reports/Triagem-scope
   YYYY-MM-DD <pasta>.md`.
4. **Recusar** se a pasta apontada estiver fora do PARA (`Readwise/`,
   `Notes/`, `Sources/` já têm fluxo próprio) — explicar por quê, não
   executar.

**Unidade de extração:** notas de área/projeto/recurso não vêm
pré-fatiadas em highlights — leia cada nota da pasta (recursivo, exceto
`_resources/`) e identifique **trechos** (frases ou parágrafos) `retain`
ou `seed` pelos mesmos critérios da tabela acima. `retain` sempre vira
stub/anexo em `Sources/` (mesma regra do parágrafo 4 acima: fonte externa
citada ou não, tanto faz — a Source Note é sempre o destino). `seed` é
**copiado** (nunca movido) para `Areas/Writing/Seeds/`, verbatim — o original na
pasta de origem permanece intacto.

### Output: `Reports/Triagem YYYY-MM-DD.md`

```markdown
# Triagem — YYYY-MM-DD
Escopo: Inbox/ (N notas) + Readwise/ (N fontes)
Processados: N itens | retain: N | seed: N | ref: N | discard: N

## 🎯 Fila de processamento (máx. 10, ranqueada)
- [ ] [[Sources/<fonte>]] — <por que vale processar em 1 linha> (prioridade: alta)
...

## 📋 Ações identificadas (Inbox)
- <nota> — <ação sugerida em 1 linha>

## 🗂️ Propostas de destino PARA (Inbox)
- <nota> → [[Projects/<projeto>]] ou [[Areas/<área>]] — <motivo em 1 linha>

## 🌱 Seeds criadas em Areas/Writing/Seeds
- [[Areas/Writing/Seeds/...]]

## 📦 Aguardando aprovação → Archiving/DMZ
### ref
- <arquivo> — <motivo em 1 linha>
### discard
- <arquivo> — <motivo em 1 linha>

> Para aprovar: `/triage-inbox --approve` (move tudo listado acima para DMZ)
```

**Ranqueamento da fila:** (1º) itens que conectam com notas existentes em
`Notes/` (valor de rede), (2º) itens de fontes que o usuário mais processou
historicamente (sinal de interesse real), (3º) recência.

---

## `/process-inbox`

**Objetivo:** ser a porta de execução de `00. Inbox/` para o PARA —
complementa o `/triage-inbox`, que só *propõe* destino PARA no relatório
sem mover. Use quando quiser que essas propostas (ou notas ainda não
triadas) sejam de fato movidas para `Projects/`/`Areas/`/`Resources/`.

**Fronteira com `/triage-inbox`:** `/process-inbox` só move para
`Projects/`, `Areas/` ou `Resources/`. Para qualquer nota que não bata
claramente com um desses três, `/process-inbox` NÃO decide o bucket de
conhecimento sozinho — deixa a nota no Inbox e a lista no relatório como
"→ candidata de conhecimento, ver `/triage-inbox`". Quem classifica
retain/seed/ref/discard é sempre o `/triage-inbox`, para não haver duas
fontes de verdade sobre o mesmo item.

### Comportamento

1. Ler todas as notas de `Inbox/` sem `layer` definido no frontmatter (ou
   sem frontmatter — captura rápida legítima não tem estrutura).
2. Para cada nota, decidir em exatamente uma categoria:

| Categoria  | Critério                                                                                   | Ação do agente                                                                                                    |
| ---------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `projeto`  | Menciona ou está claramente ligada a um projeto ativo já existente em `Projects/`             | Mover para dentro da pasta daquele projeto, mantendo o nome; preencher frontmatter padrão (`layer: project`)     |
| `área`     | É sobre uma responsabilidade contínua já mapeada em `Areas/`                                  | Mover para a subpasta de área correspondente; frontmatter padrão (`layer: area`)                                 |
| `recurso`  | Referência/conhecimento acumulado, sem prazo, sem projeto/área específica                     | Mover para `Resources/` (subpasta temática se houver uma óbvia); frontmatter padrão (`layer: resource`)          |
| `conhecimento`| Não bate com nenhuma das três acima — é ideia solta, comentário sobre fonte externa, ou vago  | NÃO mover. Listar no relatório como candidata para o `/triage-inbox` processar                                |
| `ambígua`  | Poderia ser mais de uma categoria PARA, ou o projeto/área referido não existe de fato          | NÃO mover. Listar para decisão do usuário — mover errado é pior que não mover                                    |

3. Ao mover para `projeto`/`área`/`recurso`: adicionar frontmatter completo
   (ver Convenções do CLAUDE.md), criar backlinks para a área/projeto
   correspondente.
4. Nunca mover diretamente para `Archiving/` — isso violaria a regra
   "não criar notas em Archiving/ sem ser arquivando uma nota já
   existente".
5. Nunca criar um projeto, área ou pasta nova para acomodar a nota — só
   usar o que já existe.

### Output: `Reports/Processamento-Inbox YYYY-MM-DD.md`

```markdown
# Processamento de Inbox — YYYY-MM-DD
Notas processadas: N | projeto: N | área: N | recurso: N | conhecimento: N | ambígua: N

## ✅ Movidas
- [[Projects/<projeto>/<nota>]] — <motivo em 1 linha>
- [[Areas/<área>/<nota>]] — <motivo em 1 linha>
- [[Resources/<nota>]] — <motivo em 1 linha>

## 🌱 Candidatas de conhecimento (ficaram no Inbox)
- <nota> — <por que não é PARA, em 1 linha> → rodar /triage-inbox

## ❓ Ambíguas (ficaram no Inbox, decisão do usuário)
- <nota> — <categorias possíveis e por que não deu pra decidir sozinho>
```

---

## `/audit-vault`

**Objetivo:** auditoria semanal de saúde da camada de conhecimento +
resgate gradual do DMZ.

### Verificações

1. **Órfãs:** notas em `Notes/` sem nenhum link de entrada nem saída
   (excluindo MOCs).
2. **Evergreens estagnadas:** `status: seedling` ou `status: developing`
   sem `updated` há mais de 30 dias.
3. **Sources abandonadas:** `status: processing` há mais de 60 dias, OU
   `status: captured` há mais de 90 dias.
4. **Squeeze points:** tags/temas com 10+ notas em `Notes/` sem MOC
   correspondente → sugerir criação de MOC (sugerir título e listar as
   notas que ele agruparia; NÃO criar o arquivo).
5. **Links quebrados** em `Notes/` e `Sources/`.
6. **Resgate gradual (pull, don't push):** amostrar até 20 itens de
   `Resources/` e `Archiving/DMZ/`; verificar afinidade com as notas
   criadas nos últimos 30 dias em `Notes/` e com Projects ativos. Alta
   afinidade → candidato a resgate na fila, com bucket sugerido. Item
   referenciado por um Project ativo nunca vai para DMZ — no máximo
   promover direto a `retain`.
7. **Seeds:** contar quantas seeds novas surgiram na semana (métrica de
   saúde do pipeline de crônica). Se algum seed existente foi editado de
   forma a resumir/destilar o texto bruto (viola o princípio #3), reportar
   no relatório — nunca reverter sozinho, só sinalizar.

### Output: `Reports/Auditoria YYYY-MM-DD.md`

```markdown
# Auditoria — YYYY-MM-DD
Notes: N (seedling: N | developing: N | evergreen: N) | Sources: N | DMZ: N

## 🎯 Fila da semana (máx. 10, ranqueada)
- [ ] <ação em 1 linha> — <nota> (tipo: órfã | estagnada | source | resgate-DMZ)

## 🗺️ MOCs sugeridos
- "MOC - <tema>" agruparia: [[nota1]], [[nota2]], ... (N notas)

## ⚠️ Manutenção
- Links quebrados: ...
- Seeds possivelmente editados/resumidos: ...

## 🌱 Seeds da semana
- N seeds novas

## 📈 Desde a última auditoria
- Notas novas: N | Promovidas a evergreen: N | Fila anterior concluída: N/10
```

**Ranqueamento:** resgates-DMZ relacionados a trabalho ativo primeiro
(maior valor marginal), depois sources abandonadas de fontes com stub já
iniciado, depois órfãs, depois estagnadas.

A seção "Desde a última auditoria" lê o relatório anterior — é a métrica de
regime permanente (meta: 3–5 evergreen notes/semana; fila anterior com
conclusão < 30% por 2 semanas seguidas → reportar e sugerir reduzir fila
para 5).

---

## `/map-territory`

**Objetivo:** inventário somente-leitura de `Projects/`, `Areas/` e
`Resources/` (excluindo `_resources/` e seeds) — nunca cria, move ou edita
nada. Serve para orientar onde apontar um `--scope` e alimentar o
ranqueamento do resgate da auditoria.

### Comportamento

1. Varrer `Projects/`, `Areas/` e `Resources/` recursivamente, excluindo
   `_resources/` e `Areas/Writing/Seeds/` (seeds).
2. Contar itens por pasta e subpasta.
3. Para cada nota, estimar o bucket provável (`retain`/`seed`/`ref`/
   `discard`) por leitura rápida — sem processar de verdade, é estimativa
   agregada. Listar item a item só para o top 20.
4. Rankear o top 20 candidatos de maior potencial por: afinidade com
   `Notes/` existentes e Projects ativos > densidade de claims >
   recência. Para cada um, incluir o comando `--scope` pronto para copiar.
5. Identificar bolsões de provável descarte (pastas com alta concentração
   de `discard`/`ref`) como candidatos a bulk-archive futuro — sem agir.

### Output: `Reports/Territorio YYYY-MM-DD.md`

```markdown
# Território — YYYY-MM-DD
Projects: N itens | Areas: N itens | Resources: N itens

## 📊 Contagem por pasta
- <pasta> — N itens (estimativa: N retain, N seed, N ref, N discard)

## 🎯 Top 20 candidatos de maior potencial
1. [[<nota>]] (<pasta>) — <por que, em 1 linha> → `/triage-inbox --scope "<pasta>"`
...

## 🗄️ Bolsões de provável descarte
- <pasta> — <motivo em 1 linha, ex. "alta concentração de referência utilitária desatualizada">
```

Nenhum item vira obrigação por aparecer no relatório — é mapa, não fila.

---

## `/next-source` [fonte opcional]

**Objetivo:** eliminar a fricção de *começar* uma sessão de processamento.
O gargalo do vault não é captura — é destilação (Sources acumulam muito
mais rápido do que viram Evergreens). Este comando escolhe **exatamente
uma** Source e prepara todo o contexto para o usuário sentar e reescrever;
o trabalho generativo continua 100% humano.

### Comportamento

1. **Argumento opcional:** `/next-source "Social Chemistry"` prepara a
   sessão para essa Source específica (match por parte do título ou
   autor). Se o argumento não bater com nenhuma Source, listar os matches
   mais próximos no terminal e não criar nada. Sem argumento → seleção
   automática.
2. **Seleção automática — exatamente 1 Source**, nesta ordem de
   prioridade:
   1. Item não concluído da fila de processamento do relatório de
      `Triagem` mais recente em `Reports/` (a fila já foi ranqueada —
      respeitá-la)
   2. Source com `status: processing` (trabalho iniciado — terminar antes
      de abrir frente nova)
   3. Source com `status: reading`
   4. Source com `status: captured` e trechos pendentes, ranqueada por:
      afinidade com notas existentes em `Notes/` > afinidade com Projects
      ativos > recência de `updated`/`created`
3. **Preparação no stub escolhido** (única escrita fora de `Reports/`):
   - Se o stub ainda não tem sugestões de links, sugerir até 3 notas de
     `Notes/` relacionadas como comentário `<!-- -->`, cada uma com a
     natureza da relação (apoia/contradiz/explica/exemplo/limitação).
     Checar por conteúdo antes de adicionar — nunca duplicar sugestões de
     rodada anterior.
   - **NUNCA** preencher "Com minhas palavras", nunca resumir trechos,
     nunca reordenar ou editar o que já está no stub.
   - **NUNCA alterar `status`** — a progressão `captured → reading →
     processing → processed` é o registro do trabalho humano, não do
     agente. O relatório lembra o usuário de atualizá-lo.
4. Selecionar também **2 suplentes** (próximos da fila) — só listados no
   relatório, sem tocar nos arquivos deles.

### Output: `Reports/Sessao-Source YYYY-MM-DD.md`

```markdown
# Sessão de destilação — YYYY-MM-DD

## 🎯 Source da sessão
[[Sources/<fonte>]] — <por que ela, em 1 linha>
Status atual: <status> | Trechos pendentes: N | Criada: YYYY-MM-DD

## 📋 Trechos aguardando "Com minhas palavras"
1. "<primeiras palavras do trecho...>" 
...

## 🔗 Conexões sugeridas (verificar ao reescrever)
- [[Notes/<nota>]] — <natureza da relação>

## ▶️ Como conduzir a sessão
1. Abrir a nota e reescrever cada trecho no campo "Com minhas palavras"
2. Ao terminar (ou parar), atualizar `status` e `updated` no frontmatter
3. Trecho que virou ideia autônoma → candidato a /new-evergreen-note

## ⏭️ Suplentes (se a source da vez não estiver fluindo)
- [[Sources/<fonte-2>]] — <motivo em 1 linha>
- [[Sources/<fonte-3>]] — <motivo em 1 linha>
```

Idempotência: rodar duas vezes no mesmo dia escolhe a mesma Source e
sobrescreve o relatório do dia — a escolha só muda quando o estado do
vault muda (source processada, fila nova).

---

## `/new-source-note` [fonte]

**Objetivo:** criar manualmente um stub em `Sources/` fora do fluxo de
triagem — para quando o usuário quer começar uma Source Note na hora (leu
um livro físico, quer registrar uma fonte agora).

### Comportamento

1. Reunir (perguntar se não vier no comando): título da fonte, autor,
   medium (`livro | artigo | video | podcast`). Se o usuário já colou um
   trecho junto com o pedido, esse trecho vira o primeiro item de
   `## A processar`.
2. Checar duplicata em `Sources/` por título/autor. Se já existir, não
   criar de novo — avisar e perguntar se é para anexar à existente.
3. Criar o arquivo com o schema de source (ver CLAUDE.md): `type: source`,
   `created`, `author`, `medium`, `status: captured`, `tags: []`.
4. Corpo: H1 com o título; seção `## A processar` com o(s) trecho(s)
   fornecidos como blockquote, cada um seguido de
   `**Com minhas palavras:** _[escrever aqui]_`. Se nenhum trecho foi
   fornecido, deixar a seção com `<!-- adicionar trechos aqui -->`.
5. Nunca preencher "Com minhas palavras", nunca resumir o trecho.

## `/new-evergreen-note` [ideia]

**Objetivo:** criar manualmente o rascunho de uma Evergreen Note em
`Notes/` — sempre stub, nunca o corpo.

### Comportamento

1. A ideia central em uma frase afirmativa vira o título/nome do arquivo
   (ver CLAUDE.md, "teste do título": "A confiança permite que problemas
   apareçam mais cedo" ✅, "Confiança" ❌).
2. Perguntar (não inventar) se há `source` (Source Note de origem) e
   `mocs` (MOC relacionado já existente) — deixar vazio se não houver.
3. Checar duplicata por título em `Notes/`; se existir, avisar em vez de
   sobrescrever.
4. Criar com o schema de evergreen: `type: evergreen`, `created`,
   `source`, `mocs`, `status: seedling`, `updated`, `tags: []`.
5. Corpo: H1 com o título, e só o campo
   `**Com minhas palavras:** _[escrever aqui]_` logo abaixo — nada de
   esboço, nada de "a nota deveria falar sobre X". O agente não escreve
   nem uma frase do conteúdo.
6. Sugerir (como comentário `<!-- -->`, não como wikilink) até 3 notas
   relacionadas já existentes em `Notes/`, com a natureza da relação
   (apoia/contradiz/explica/exemplo/limitação). Não inventar se não
   houver nenhuma candidata real.

## `/new-moc` [tema]

**Objetivo:** criar um MOC — só quando for um squeeze point genuíno (10+
notas permanentes sobre o tema). Este comando existe principalmente para
**recusar** a maior parte das vezes que for chamado.

### Comportamento

1. Receber o tema/tag.
2. Contar quantas notas `type: evergreen` em `Notes/` compartilham essa
   tag (frontmatter `tags:`) ou o tema no título/corpo.
3. **Se < 10 notas:** recusar. Explicar a regra do squeeze point, informar
   quantas notas existem hoje sobre o tema e quantas faltam, e não criar
   nenhum arquivo.
4. **Se ≥ 10 notas:** criar o MOC (`type: moc`, `created`,
   `status: active`) com H1 "MOC - <tema>" e uma lista `[[nota]]` de
   todas as notas encontradas — aqui os links são definitivos (é
   literalmente o papel do MOC), mas só de notas que já existem.

---

## Edge cases

- Highlight sem fonte identificável → bucket `ref`, nunca inventar
  metadados de fonte.
- Arquivo malformado/sem frontmatter no inbox → listar em seção "⚠️ Não
  processados" com o motivo; não travar a execução.
- Colisão de nome ao mover/criar seed → sufixar `-2`, `-3`.
- Execução repetida no mesmo dia → sobrescrever o relatório do dia
  (idempotente), nunca duplicar stubs.
- `Inbox/` e/ou `Readwise/` vazios → gerar relatório mínimo confirmando,
  não é erro (processar o que existir do outro normalmente).
- `--scope <pasta>` apontando para fora do PARA (ex.: `Readwise/`,
  `Notes/`, `Sources/`) → recusar, explicar que `--scope` é só para
  `Projects/`/`Areas/`/`Resources/`.
- `--scope` executado duas vezes na mesma pasta → segunda rodada não
  duplica trechos já extraídos (checagem por conteúdo, não por marcador).
- `/process-inbox` numa nota sem projeto/área/recurso óbvio → categoria
  `conhecimento` ou `ambígua`, nunca forçar um destino PARA por falta de
  opção melhor.
- `/new-moc` chamado para um tema com poucas notas → recusar é o
  comportamento correto, não uma falha.
- `/map-territory` nunca escreve fora de `Reports/` — se parecer útil
  criar um stub durante a varredura, resistir: isso é trabalho do
  `--scope`, não do mapa.
- `/next-source` sem nenhuma Source pendente (todas `processed`/
  `archived`, sem trechos em aberto) → relatório mínimo confirmando fila
  vazia e sugerindo rodar `/triage-inbox`; não é erro.
- `/next-source "<fonte>"` sem match → listar os títulos mais próximos e
  não criar relatório nem tocar em nenhum arquivo.
- `/next-source` com relatório de Triagem antigo cuja fila já foi toda
  processada → ignorar a fila e cair no ranqueamento próprio (passos
  2.2–2.4).

## Critérios de aceitação

1. Rodar `/triage-inbox`, `/process-inbox` ou `/map-territory` duas vezes
   seguidas produz o mesmo estado (idempotência).
2. Nenhuma execução jamais cria texto no campo "Com minhas palavras",
   jamais deleta arquivo, jamais toca em `Projects/` sem instrução
   explícita.
3. Seeds chegam a `Areas/Writing/Seeds/` byte a byte idênticas ao texto original.
4. Todo item movido para DMZ é rastreável: o relatório registra origem →
   destino.
5. As filas nunca excedem 10 itens.
6. `--approve` só move o que está listado no último relatório, nada além.
7. `/new-moc` nunca cria arquivo para um tema com menos de 10 notas evergreen.
8. `/new-source-note` e `/new-evergreen-note` nunca criam duplicata
   silenciosa — sempre checam por título/autor antes.
9. `--scope <pasta>` nunca move, edita ou marca frontmatter nos arquivos
   originais da pasta escopada — só lê e extrai.
10. `--scope <pasta>` nunca gera bucket `ref` ou `discard`, nunca propõe
    nada para `Archiving/DMZ/`.
11. `/map-territory` termina sem ter criado, movido ou editado nenhum
    arquivo fora de `Reports/`.
12. `/next-source` escolhe exatamente 1 Source, nunca altera `status` nem
    o conteúdo existente do stub (só adiciona sugestões de links como
    comentário, sem duplicar), e rodá-lo duas vezes no mesmo dia produz o
    mesmo resultado.
