---
name: liberar-disco
description: Mede o disco do Mac e propõe o que liberar — caches que se refazem, worktrees e cópias de tarefas de agentes já mescladas, node_modules e venvs de projetos parados, temporários antigos — sem apagar nada sem o ok do Gustavo. Use quando o disco estiver cheio ou quase (menos de 15 GB livres), quando uma ferramenta falhar por falta de espaço (iCloud que não baixa, npm, pip, git, worktree recusada), antes de abrir worktrees em paralelo, ou quando ele pedir para limpar ou liberar espaço.
---

# Liberar disco

O Mac do Gustavo vive perto do limite (228 GB, com 1 a 6 GB livres em outubro de 2026). Disco
cheio já esvaziou `.git`, venv e `node_modules` pelo iCloud, travou o vitest e fez o setup de
worktree do Codex recusar. Esta skill mede, propõe e só apaga o que ele aprovar, item por item.

## Passos

1. **Medir.** Rode `bash "<pasta desta skill>/scripts/medir.sh"`. No Claude Code, a pasta é
   `${CLAUDE_SKILL_DIR}`; no Codex, a pasta onde este `SKILL.md` está. A varredura leva de 1 a 3
   minutos; passe pastas de projetos como argumentos para limitar a busca. O script só lê.
2. **Classificar** cada linha num destes grupos, nesta ordem de preferência:
   - **Se refaz sozinho:** caches de npm, pip, uv, Homebrew (`brew cleanup --prune=all`),
     Playwright, DerivedData do Xcode, caches de updater (`*.ShipIt`, `*-updater`). Custo: o
     próximo install baixa de novo.
   - **Trabalho de agente já integrado:** worktrees em `.claude/worktrees/` ou
     `~/.codex/worktrees/`, e cópias de tarefas (`~/Documents/Codex/<data>/task-N/`). Confira
     antes: `git -C <pasta> status --short` vazio e o branch mesclado ou sem commits próprios
     (`git -C <pasta> log --oneline <branch-base>..HEAD` vazio). Worktree com mudança ou commit
     não mesclado não entra na lista. Remova worktree com `git worktree remove <pasta>` a partir
     do repo principal, nunca com `rm`.
   - **Temporários de sessões antigas:** pastas em `/private/tmp` e no `$TMPDIR` com mais de 2
     dias (`find ... -maxdepth 1 -mtime +2`), como cópias de repo e venvs de ensaio. Nunca a
     pasta de scratchpad da sessão atual.
   - **Projetos parados:** `node_modules` e venvs de projetos sem commit há mais de 30 dias. Diga
     o comando que os refaz (`npm ci`, `pip install -e ".[dev]"`).
   - **Só o Gustavo faz:** lixeira, Downloads, fotos, simuladores do iOS (`xcrun simctl delete
     unavailable` ele pode rodar), Docker, apps grandes, snapshots do Time Machine. Liste com o
     tamanho; não apague.
3. **Propor** uma tabela única: item, tamanho, grupo, o que se perde, comando. Some o total por
   grupo. Recomende o mínimo que leva o disco a 15 GB livres (o que libera worktrees em
   paralelo) ou, se não der, a 5 GB (o mínimo para o setup de worktree do Codex).
4. **Apagar só o aprovado**, um comando por item, e medir de novo com `df -h /System/Volumes/Data`.
   Mostre o antes e o depois.

## Nunca

- Apagar nada sem o ok explícito do Gustavo nesta conversa; o ok de uma limpeza anterior não vale.
- Esvaziar a lixeira, mexer em `~/Documents` fora de `node_modules`, venvs e worktrees de
  agentes, ou em `~/Library` fora de `Caches` e `Developer/Xcode/DerivedData`.
- Ler ou varrer pastas do iCloud sem `.nosync` no caminho atrás de arquivos grandes: a leitura
  baixa de volta o que o iCloud tinha esvaziado e piora o disco.
- Usar `rm` numa worktree registrada no git, num `.git`, na venv ou no `node_modules` do
  checkout principal de um projeto ativo (o curso-lab, por exemplo), ou em segredos
  (`~/.config/<projeto>/`, `.env`).
- Mexer em `~/.claude`, `~/.codex` (fora de `worktrees/`), `~/.agents` ou nos clones de
  `agent-skills`.
