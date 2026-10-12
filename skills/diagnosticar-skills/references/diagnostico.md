# Diagnóstico somente leitura

Python 3.10+ e o clone com `scripts/instalar.py` são necessários. Comando:

```bash
python3 "<pasta da skill>/scripts/diagnosticar.py" \
  --repo "<clone agent-skills>" --agente codex \
  --destino "<projeto>/.agents/skills" --projeto obsidian
```

`--destino` pode repetir; sem ele lê apenas as pastas pessoais correspondentes ao agente.
`--agente` aceita `claude`, `codex`, `ambos` (padrão). `--projeto` pode repetir e só seleciona
skills do projeto, nunca altera arquivos. `--json` gera relatório estruturado em stdout.
Para uma instalação com `--em`, informe ambos os caminhos relevantes explicitamente.
O script não faz rede, não segue symlinks internos para calcular conteúdo, não cria cache,
manifesto ou relatório em disco e não tenta executar os programas encontrados.

## Interpretar

- `igual`: conteúdo corresponde à fonte; não prova que o agente carregou a skill.
- `link-fonte`: aponta diretamente à fonte; alterações no clone têm efeito imediato.
- `ausente`: não está nesse destino; outro escopo pode ter precedência.
- `atualizacao-gerenciada`: instalado igual à baseline, fonte mudou; atualização pode ser
  proposta após revisão, mas o diagnóstico não a executa.
- `edicao-local`: instalado difere da baseline. Preserve e compare antes de decidir.
- `divergente-sem-proveniencia`: sem baseline confiável, não distingue cópia antiga de edição.
- `origem-diferente`: manifesto pertence a outro clone, não alegar atualização segura.
- `erro-leitura`: não concluir sobre conteúdo que não pôde ser inspecionado.

O commit descreve a fonte; `fonte_modificada` informa alterações locais. Não é uma versão
semântica do produto. A versão do Claude Code/Codex só é confirmada se o usuário fornecer
saída de versão ou autorizar verificação apropriada. Compatibilidade runtime permanece não
verificada até uma sessão real. Os 35 wrappers Claude usam comandos/Skill do Claude;
Codex usa os SKILL.md instalados e não importa `.claude/commands` nem agentes Claude.

Obsidian CLI exige o app desktop aberto: binário encontrado não comprova isso. Workflows
baseados em arquivos podem ler um vault acessível sem a CLI. `liberar-disco` exige macOS;
MLflow exige suas dependências e acesso autorizado ao tracking, que não são testados aqui.

## Acionamento

Positivos: “A skill ficou velha depois do pull”; “Por que Codex não acha study-loop?”;
“Compare skills instaladas com a fonte, sem alterar nada”.
Negativos: “Instale minhas skills” (instalação autorizada em outro fluxo);
“Explique Databricks” (tutoria); “Limpe o disco” (liberar-disco em macOS).

## Limites de evidência

Datas de arquivos sozinhas não comprovam versão. Um hash diferente comprova divergência,
não sua causa. Não publique relatório bruto: caminhos podem revelar nomes e locais privados.
A saída é para revisão privada do usuário, com segredos e caminhos pessoais omitidos ao
preparar um issue público.
