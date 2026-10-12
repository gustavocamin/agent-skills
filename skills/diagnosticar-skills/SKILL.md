---
name: diagnosticar-skills
description: Diagnostica por leitura a origem e a instalação de skills, divergências de hash, versão, caminhos, pré-requisitos e compatibilidade Claude Code/Codex. Use quando uma skill sumiu, ficou antiga ou não funciona em certo ambiente; não instala nem corrige automaticamente.
metadata:
  compatibility: Python 3.10+, clone acessível de agent-skills e permissão de leitura nos destinos escolhidos.
---

# Diagnosticar skills

Identifique o ambiente alvo e a raiz do clone. Diagnosticar este container não comprova a
instalação no computador do usuário. Não procure credenciais nem execute instaladores,
comandos de autenticação, CLIs de terceiros ou correções.

Execute o helper desta skill com caminhos explícitos, conforme
[referência de diagnóstico](references/diagnostico.md). Ele importa apenas o módulo local
do instalador do clone para compartilhar o algoritmo de hash; não chama a instalação.

Mostre origem/commit, destino efetivo, hash da origem/instalado/baseline, divergência,
pré-requisitos observáveis e limites de compatibilidade. Ausência de dados é “não verificado”,
não falha confirmada. Um binário encontrado não comprova versão, login ou app aberto.

Feche com uma tabela curta: item, evidência, impacto, próximo passo proposto. Para divergência
local, proponha comparar o diff e preservar a edição; nunca execute `--forcar`, atualização,
remoção ou reinstalação como consequência do diagnóstico. Peça autorização antes da mudança.
