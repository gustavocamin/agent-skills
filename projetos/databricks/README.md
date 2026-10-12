# Databricks AI Tools

Conjunto opcional das 34 skills estáveis oficiais de
[databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills/tree/c1964266c7aa6063d89036691d0594420ffa0129/skills),
fixado no commit `c1964266c7aa6063d89036691d0594420ffa0129`.

São instruções e materiais de referência para trabalhar com os serviços Databricks.
O instalador deste repositório distribui os arquivos; não instala CLI, SDK, MCP,
dependências Python/Node, hooks, plugins, credenciais ou serviços. Não executa os
scripts distribuídos pelas skills nem autentica uma conta.

## Instalação opcional

Execute a partir da raiz deste repositório e revise primeiro o dry-run:

```bash
# Skills gerais + conjunto Databricks, nos dois agentes
bash install.sh --projeto databricks --dry-run
bash install.sh --projeto databricks

# Somente Codex
bash install.sh --agente codex --projeto databricks --dry-run
bash install.sh --agente codex --projeto databricks

# Skills Databricks limitadas a um projeto local, somente Claude Code
bash install.sh --agente claude --projeto databricks --em "<projeto>" --dry-run
bash install.sh --agente claude --projeto databricks --em "<projeto>"
```

Sem `--projeto databricks`, este conjunto não é instalado. O catálogo completo
está em [TERCEIROS.md](../../TERCEIROS.md#databricks-ai-tools). Consulte o
[README principal](../../README.md) para destinos, cópia/link, atualização e
preservação de edições locais.

## Pré-requisitos e dependências

- Um workspace Databricks acessível, permissões para a tarefa e autenticação
  autorizada separadamente. Não salve tokens ou detalhes da conta neste repo.
- CLI Databricks e versão compatível com a skill escolhida. Neste pin,
  `databricks-core` exige CLI 1.0.0+, `databricks-data-discovery` indica 1.9.0+
  para `genie ask`, `databricks-unity-gateway` exige 1.11.0+ e
  `databricks-setup-local` exige 1.16.0+ e `uv`. O formato simplificado de
  `code_source` em `databricks-ai-runtime` exige 1.20.0+. Confira o frontmatter
  e as referências da skill antes de usar; esses números descrevem o pin,
  não uma garantia sobre versões futuras.
- A maioria das skills declara `parent: databricks-core`; leia-a para CLI,
  autenticação e escolha de perfil. `databricks-app-design` declara
  `parent: databricks-apps`, que depende de `databricks-core`. O conjunto é
  instalado inteiro para preservar essas dependências e referências cruzadas.
  A descoberta de `parent` depende do agente; se ele não carregar a dependência
  automaticamente, carregue a skill base explicitamente.
- Cada tarefa pode exigir recursos ou ferramentas adicionais, como SQL
  warehouse, compute, Unity Catalog, SDK Python, Node/AppKit ou serviços MCP.
  Eles não são provisionados por esta cópia. Confirme escopo, custo e permissão
  antes de criar recursos, publicar apps, enviar dados ou instalar ferramentas.
- `databricks-mlflow-evaluation` complementa as skills genéricas de MLflow já
  presentes em `skills/`, com padrões específicos de Databricks/Unity Catalog.
  `agent-evaluation` continua sendo a referência genérica; ela não foi duplicada.
- A skill própria `tutor-databricks` continua voltada ao processo de aprendizagem;
  o conjunto oficial fornece os workflows e as referências de produto.

A presença dos arquivos não comprova que Claude Code ou Codex os carregaram,
nem que a CLI ou o workspace estejam prontos. Valide a descoberta em uma nova
sessão e siga a [documentação oficial](https://docs.databricks.com/aws/en/agent-skills/)
para requisitos atuais. Instruções das skills não substituem as aprovações de
instalação, autenticação, compartilhamento ou alteração de recursos.

## Escopo, licença e integridade

Foram preservados, byte a byte, os 353 arquivos do diretório `skills/` do
upstream, incluindo scripts, assets e referências. Não foram importados os
diretórios `experimental/`, `commands/`, `hooks/`, bundles de plugins ou
instaladores do repositório upstream. Referências a comandos, hooks ou MCPs
podem aparecer no texto original; eles não são ativados por esta instalação.

Este material está sob a **Databricks License**, com uso, cópia, modificação e
redistribuição restritos ao uso dentro dos serviços Databricks ou à conexão com
eles, conforme os termos integrais. Não é distribuído aqui sob MIT ou Apache-2.0.
Leia [LICENSE](../../licencas/databricks-agent-skills-LICENSE) e
[NOTICE](../../licencas/databricks-agent-skills-NOTICE).

Como adaptação de empacotamento, cada uma das 34 pastas contém uma cópia integral
do `LICENSE` e do `NOTICE` da raiz upstream: 68 arquivos adicionais, sem alterar
nenhum arquivo original. Assim, os avisos acompanham tanto as cópias instaladas
quanto os links. Ao redistribuir uma skill separadamente, mantenha esses avisos.

O [manifesto SHA-256](../../licencas/databricks-agent-skills-SHA256SUMS) separa os
353 originais, os 68 avisos adicionais e as duas cópias centrais. Para conferir
os hashes, execute na raiz deste repositório:

```bash
sha256sum -c licencas/databricks-agent-skills-SHA256SUMS
```

No macOS, pode usar `shasum -a 256 -c` com o mesmo arquivo. O manifesto detecta
divergências locais; não é assinatura do publicador. Para atualizar, revise um
novo commit oficial, sua licença e seus avisos; copie novamente a árvore estável,
replique os avisos, compare os bytes com a origem e regenere o manifesto. Atualize
o pin, o catálogo e as contagens deste README e de `TERCEIROS.md`. Não edite as
skills de terceiros localmente para corrigir conteúdo ou diferenças de metadata.
