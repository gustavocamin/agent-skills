# Skills de terceiros

## MLflow

Copiadas sem alteração do [mlflow/skills](https://github.com/mlflow/skills), commit
`51a42ea2b07fadb45fb34c7cecf0c87edbe05686` (copiado em 09/10/2026), sob a licença Apache-2.0
([licencas/mlflow-skills-LICENSE](licencas/mlflow-skills-LICENSE)). Para atualizar, copie de novo
do repo de origem num commit novo e troque o hash acima; o `scripts/sincronizar.sh` não mexe nelas.

| Skill | Pasta de origem |
| --- | --- |
| `agent-evaluation` | `agent-evaluation/` |
| `analyze-mlflow-chat-session` | `analyze-mlflow-chat-session/` (name: `analyzing-mlflow-session`) |
| `analyze-mlflow-trace` | `analyze-mlflow-trace/` (name: `analyzing-mlflow-trace`) |
| `instrumenting-with-mlflow-tracing` | `instrumenting-with-mlflow-tracing/` |
| `mlflow-onboarding` | `mlflow-onboarding/` |
| `querying-mlflow-metrics` | `querying-mlflow-metrics/` |
| `retrieving-mlflow-traces` | `retrieving-mlflow-traces/` |
| `searching-mlflow-docs` | `searching-mlflow-docs/` |

## Obsidian

Copiadas sem alteração do [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills),
commit `3ccff5338ea700537839b21900aa5358a0402c98` (copiado em 09/10/2026), sob a licença MIT
([licencas/obsidian-skills-LICENSE](licencas/obsidian-skills-LICENSE)). A `obsidian-cli` precisa
do app do Obsidian aberto, então só serve na máquina; a `defuddle` precisa do CLI
(`npm install -g defuddle`).

| Skill | Pasta de origem |
| --- | --- |
| `defuddle` | `skills/defuddle/` |
| `json-canvas` | `skills/json-canvas/` |
| `obsidian-bases` | `skills/obsidian-bases/` |
| `obsidian-cli` | `skills/obsidian-cli/` |
| `obsidian-markdown` | `skills/obsidian-markdown/` |

## Databricks AI Tools

As 34 skills estáveis de
[databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills),
commit `c1964266c7aa6063d89036691d0594420ffa0129` (copiado em 12/10/2026), ficam em
`projetos/databricks/skills/` e são opcionais: `bash install.sh --projeto databricks`.
Guia de uso e pré-requisitos: [projetos/databricks/README.md](projetos/databricks/README.md).

**Licença específica e restrita:** a
[Databricks License](licencas/databricks-agent-skills-LICENSE) permite uso, cópia,
modificação, publicação e redistribuição somente para usar o material dentro dos
serviços Databricks ou conectar-se a eles, de acordo com o acordo e as restrições
aplicáveis. Esta cópia não relicencia o material como MIT ou Apache-2.0. Quem
redistribui deve repassar a licença e preservar os avisos aplicáveis; arquivos
modificados precisam de aviso destacado da alteração. Consulte o texto integral,
inclusive condições de término, e o [NOTICE](licencas/databricks-agent-skills-NOTICE).

Os **353 arquivos originais** de `skills/`, incluindo assets, referências e
scripts, foram copiados sem alteração. Foram acrescentadas **68 cópias integrais
de avisos**: o `LICENSE` e o `NOTICE` da raiz upstream em cada uma das 34 pastas de
skill, para que acompanhem a instalação por pasta. Nenhum arquivo original foi
editado. As duas cópias centrais também ficam em `licencas/`. O
[manifesto SHA-256](licencas/databricks-agent-skills-SHA256SUMS) identifica as três
categorias e permite verificar os 423 arquivos a partir da raiz do repo com
`sha256sum -c licencas/databricks-agent-skills-SHA256SUMS`.

Não foram copiados `experimental/`, `commands/`, `hooks/`, bundles de plugins ou
instaladores upstream. A cópia não instala ferramentas, MCPs ou autenticação e
não executa os scripts incluídos. A maioria das skills depende de
`databricks-core`; `databricks-app-design` depende de `databricks-apps`.
`databricks-mlflow-evaluation` complementa o MLflow genérico já existente neste
repo, sem duplicá-lo.

Para atualizar, copie a árvore `skills/` de um novo commit oficial, preserve os
avisos, confira os bytes com a origem e atualize o pin, catálogo e manifesto.
Não corrija localmente o conteúdo vendorizado; mantenha a identidade do upstream.
O `scripts/sincronizar.sh` não é o fluxo de atualização deste conjunto.

| Skill | Pasta de origem |
| --- | --- |
| `databricks-agent-bricks` | `skills/databricks-agent-bricks/` |
| `databricks-ai-functions` | `skills/databricks-ai-functions/` |
| `databricks-ai-runtime` | `skills/databricks-ai-runtime/` |
| `databricks-aibi-dashboards` | `skills/databricks-aibi-dashboards/` |
| `databricks-app-design` | `skills/databricks-app-design/` |
| `databricks-apps` | `skills/databricks-apps/` |
| `databricks-apps-python` | `skills/databricks-apps-python/` |
| `databricks-core` | `skills/databricks-core/` |
| `databricks-dabs` | `skills/databricks-dabs/` |
| `databricks-data-discovery` | `skills/databricks-data-discovery/` |
| `databricks-dbsql` | `skills/databricks-dbsql/` |
| `databricks-docs` | `skills/databricks-docs/` |
| `databricks-execution-compute` | `skills/databricks-execution-compute/` |
| `databricks-genie-agents` | `skills/databricks-genie-agents/` |
| `databricks-iceberg` | `skills/databricks-iceberg/` |
| `databricks-jobs` | `skills/databricks-jobs/` |
| `databricks-lakebase` | `skills/databricks-lakebase/` |
| `databricks-lakeflow-connect` | `skills/databricks-lakeflow-connect/` |
| `databricks-metric-views` | `skills/databricks-metric-views/` |
| `databricks-ml-training` | `skills/databricks-ml-training/` |
| `databricks-mlflow-evaluation` | `skills/databricks-mlflow-evaluation/` |
| `databricks-model-serving` | `skills/databricks-model-serving/` |
| `databricks-pipelines` | `skills/databricks-pipelines/` |
| `databricks-python-sdk` | `skills/databricks-python-sdk/` |
| `databricks-serverless` | `skills/databricks-serverless/` |
| `databricks-serverless-migration` | `skills/databricks-serverless-migration/` |
| `databricks-setup-local` | `skills/databricks-setup-local/` |
| `databricks-spark-structured-streaming` | `skills/databricks-spark-structured-streaming/` |
| `databricks-synthetic-data-gen` | `skills/databricks-synthetic-data-gen/` |
| `databricks-unity-catalog` | `skills/databricks-unity-catalog/` |
| `databricks-unity-gateway` | `skills/databricks-unity-gateway/` |
| `databricks-unstructured-pdf-generation` | `skills/databricks-unstructured-pdf-generation/` |
| `databricks-vector-search` | `skills/databricks-vector-search/` |
| `databricks-zerobus-ingest` | `skills/databricks-zerobus-ingest/` |
