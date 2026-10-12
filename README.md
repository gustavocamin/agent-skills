# agent-skills

Skills compartilhadas para Claude Code e Codex. A instalação distribui arquivos; não instala
CLIs, MCPs, credenciais ou serviços e não garante que um runtime carregou uma skill.

## Catálogo e fonte

| Conjunto | Uso |
| --- | --- |
| `skills/` | Skills gerais próprias e de terceiros; instaladas por padrão |
| `projetos/obsidian/skills/` | Workflows de vault, inclusive `study-loop`, `comms-check` e `exec-sim` portáveis |
| `projetos/obsidian/commands/`, `agents/` | Adaptadores e agentes **exclusivos do Claude Code** |
| `projetos/databricks/skills/` | 34 skills oficiais Databricks, opt-in com `--projeto databricks` |
| `projetos/curso-lab-agent/skills/` | Fluxo específico de especificação, implementação e validação do curso-lab |

Novas skills próprias:
- `tutor-databricks`: tentativa do aluno, dica incremental, diagnóstico, nova tentativa e transferência.
- `mapa-projeto-tech-lead`: mapa de um projeto existente em oito dimensões, com evidências e lacunas.
- `revisar-qualidade-dados`: regra de negócio, métrica, limiar, testes, exceções e reprocessamento.
- `diagnosticar-skills`: comparação read-only entre fonte, hashes, baseline e instalação.
- `revisar-decisao-de-compra`: necessidade, custo total, compatibilidade, evidências e alternativas,
  incluindo esperar ou não comprar; pesquisa e decisão, sem checkout automático.

No pacote Obsidian, `exec-sim --conversa` (ensaiar-conversa-dificil) treina conversas com
clientes sobre prazo, escopo e recomendações, com tentativa, feedback e nova tentativa.
O modo usa o fluxo e o relatório existentes; não envia mensagens nem cria compromissos.

O preparo de decisão técnica está integrado ao handoff, implementação e validação existentes:
racional, impacto de negócio, custo, risco, operação, reversibilidade e alternativas rejeitadas.
Não há uma segunda skill de decisão, revisão semanal ou simulação executiva.

O pacote Databricks é opcional (`bash install.sh --projeto databricks --dry-run`) e está
fixado no commit `c1964266c7aa6063d89036691d0594420ffa0129`. Sua licença é restrita a uso
com os serviços Databricks; cada skill mantém LICENSE/NOTICE. Não instalamos ferramentas,
MCPs ou autenticação. Veja [instruções e dependências](projetos/databricks/README.md).

`TERCEIROS.md` identifica origens, versões e licenças. Skills de terceiros não são editadas
localmente. Para o curso-lab, a fonte das cinco skills continua sendo seu próprio repositório;
esta cópia central e qualquer correção pendente de upstream precisam ser reconciliadas antes
de rodar `scripts/sincronizar.sh`, para não perder mudanças.

## Instalar e escolher o agente

Requisitos do instalador: Bash, Python 3.10+ e Git. Execute primeiro o dry-run:

```bash
git clone https://github.com/gustavocamin/agent-skills
cd agent-skills
bash install.sh --dry-run
bash install.sh
```

- Padrão: skills gerais em `~/.claude/skills` e `~/.agents/skills`.
- `--agente claude`, `--agente codex` ou `--agente ambos` (padrão) seleciona o agente.
- `--destino "<pasta de skills>"` usa um destino explícito; pode repetir.
- `--projeto obsidian` ou `--projeto curso-lab-agent` inclui o conjunto escolhido.
- `--projeto obsidian --em "<vault>"` instala skills do projeto em `.claude/skills` e
  `.agents/skills` conforme o agente. Comandos/agentes entram só em `.claude/` quando Claude
  está selecionado. `--em` não significa que o Codex execute comandos ou agentes Claude.
- `--link` aponta diretamente para o clone. Editar um item instalado assim modifica a fonte;
  mantenha o clone no mesmo lugar. Trocar cópia/link exige revisão explícita.
- `--dry-run` descreve o plano sem criar pastas, manifestos, backups ou exclusões Git.

Exemplo apenas Codex, sem adaptadores Claude:

```bash
bash install.sh --agente codex --projeto obsidian --em "<vault>" --dry-run
```

## Atualização segura

```bash
git pull --ff-only
git log -5 --oneline
bash install.sh --dry-run
# Revise o diff da fonte e os itens propostos antes de aplicar:
bash install.sh
```

O instalador mantém proveniência e hash da última cópia instalada num manifesto irmão do
destino. Se a instalação segue igual à baseline, a nova fonte pode atualizar automaticamente.
Se há edição local, origem diferente ou item divergente sem proveniência, ele preserva e
informa o conflito. Cópias antigas iguais à fonte podem ser adotadas sem reescrever conteúdo.

`--forcar` permite substituir itens conflitantes com backup, exceto proteções de arquivos
versionados e caminhos inseguros. Revise o caminho do backup informado antes de qualquer
limpeza; ele não é removido automaticamente. Não use `--forcar` no setup automático para
“resolver” conflitos. Itens removidos da fonte não são apagados automaticamente da instalação.

Manifestos/backups ficam ao lado da pasta de destino em `.agent-skills-<nome-do-destino>/`.
Não edite a baseline para ocultar diferenças. Ela registra estado local, não é assinatura
criptográfica de confiança no upstream.

Para diagnóstico sem alteração:

```bash
python3 skills/diagnosticar-skills/scripts/diagnosticar.py \
  --repo . --agente codex --destino "<pasta>/.agents/skills" --json
```

## Ambiente cloud e limites

No setup, clone ou atualize a fonte e rode o instalador com o agente correto. Fixe um commit
revisado para reprodutibilidade. A rede precisa permitir GitHub; não embuta tokens no script.
Com HOME sem escrita, o instalador pode usar o repositório de tarefa encontrado no diretório
atual ou o único repositório elegível no workspace. Instala ali sem sobrescrever skills
versionadas e adiciona apenas itens novos a `.git/info/exclude`. Em ambiente ambíguo, use
`--destino` explicitamente. A seleção de escopo e precedência depende do runtime; valide em
uma sessão nova, não confunda sucesso da cópia com carregamento confirmado.

Compatibilidade observável:
- Claude Code usa `.claude/skills` e seus adaptadores `commands/agents`.
- Codex usa `.agents/skills`; invoque `study-loop`, `comms-check` e `exec-sim` como skills.
  Os demais wrappers Claude não são comandos Codex; suas skills canônicas continuam disponíveis.
- `obsidian-cli` requer o aplicativo desktop aberto. Não funciona num container só por haver
  uma cópia da skill. Workflows por arquivos precisam de um vault acessível e autorizado.
- `liberar-disco` é específico do Mac e recusa Linux; o disco do cloud não é o do usuário.
- Skills MLflow exigem suas ferramentas e acesso ao serviço, não provisionados aqui.
- Duas pastas MLflow preservam nomes diferentes no frontmatter upstream:
  `analyze-mlflow-chat-session` → `analyzing-mlflow-session` e
  `analyze-mlflow-trace` → `analyzing-mlflow-trace`. O checker avisa; carregamento nos
  runtimes não foi validado. As novas skills seguem nome igual à pasta.
- Nenhuma verificação local deste repo prova suporte completo de Claude/Codex/Obsidian ao vivo.

Caminhos oficiais: [Claude Code](https://code.claude.com/docs/en/skills),
[Codex](https://developers.openai.com/codex/skills/) e
[formato Agent Skills](https://agentskills.io/specification).

## Manter e testar

```bash
python3 scripts/conferir.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 skills/iniciar-projeto/scripts/autoteste.py
```

Os testes usam HOME e projetos temporários: instalação nova, idempotência, atualização gerenciada,
preservação local, backups, dry-run, links, caminhos com espaços, seleção de agente e diagnóstico
read-only. Testes estruturais verificam frontmatter e referências; exemplos de acionamento
positivo/negativo estão nas referências das novas skills. Avaliação do comportamento do modelo
continua necessária; esses testes não simulam um runtime completo.

`bash scripts/sincronizar.sh` importa cópias locais; revise seu diff antes de publicar. Com
`--link`, edições já alteram o clone. Não rode instalação real, push, PR ou merge sem a
autorização correspondente. Este repositório é público: exemplos devem ser genéricos, sem
planos privados, pessoas, contas, clientes, segredos ou prazos pessoais.
