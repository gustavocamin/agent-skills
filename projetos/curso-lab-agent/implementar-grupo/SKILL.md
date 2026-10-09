---
name: implementar-grupo
description: Implementa um Grupo N da feature Fxx neste repositório, seguindo dono, branch, contrato, testes, CI e handoff do plan.md. Use quando o Gustavo pedir para implementar um grupo já especificado.
---

# Implementar grupo

Implemente o Grupo N da Fxx conforme a spec aprovada. O `AGENTS.md` continua sendo a fonte das regras do repositório.

## Antes de escrever código

1. Execute `git merge-base --is-ancestor fa6c58a HEAD`. Se o código de saída não for 0, pare e avise ao Gustavo que a branch não tem as regras de handoff de 08/10.
2. Leia `AGENTS.md`, `specs/constitution/mission.md`, `tech_stack.md` e `roadmap.md`, e os três arquivos da spec em `specs/features/Fxx-*/`. Confira no `plan.md` que o `Dono` do Grupo N corresponde ao agente e ambiente desta sessão. Anote a linha `Integra`; se faltar, o Claude Code integra. Confirme a branch indicada para o grupo.
3. Se o grupo consome um contrato entre cliente e servidor, leia o schema em `app/server/validation.ts` antes de chamar a rota. Se define um contrato, tipe o corpo de cada pedido em `app/client/src/lib/api.ts`, ao lado da resposta, e crie um teste que passe as fixtures do cliente pelo schema do servidor.

## Durante o trabalho

- Trabalhe só nos caminhos do campo `Toca` do grupo e na branch indicada no `plan.md`. Atualize spec e código juntos nos caminhos permitidos.
- Prove cada teste novo de contrato ou de dado com uma mutação que o faça falhar, numa cópia temporária. Guarde a prova no repositório ou no `validation.md`, conforme o `AGENTS.md`.
- Não escreva `start_here.md`, `specs/constitution/`, o “Registro dos grupos” nem o “Resultado” de `validation.md`, a menos que esta sessão seja a de quem integra (o agente da linha `Integra` do `plan.md`, ou o Claude Code se ela faltar), trabalhando na branch da feature. Numa branch de grupo, ou sendo o outro agente, envie o texto desses arquivos para quem integra no handoff.
- Num grupo ⚠, peça a aprovação do Gustavo antes de **cada** comando ⚠, conforme o `AGENTS.md`. Ao terminar o grupo, pare e mostre o diff ao Gustavo antes do handoff.

## Fechar o grupo

1. Rode `pytest -q` e `ruff check .` na worktree do grupo. Se mexeu em `app/`, rode `npm run format:fix` antes do último commit e, em `app/`, `npm run format`, `npm run typecheck`, `npm run lint`, `npm run lint:ast-grep` e `npm test`. Siga também a exigência de `databricks apps validate` do `AGENTS.md`; no Codex cloud, ela fica com quem integra.
2. Antes de declarar `Desvios da spec: nenhum`, releia **Interfaces** e **Requisitos** de `requirements.md` e compare cada item com o diff. Qualquer nome de campo, rota ou comportamento diferente é um desvio; declare-o item por item.
3. Faça push do commit de código da branch do grupo e espere o CI verde para ter um run verificável. Depois, salve a mensagem completa num arquivo e confira com `python scripts/check_handoff.py --file <arquivo>` antes do último commit com este handoff, em português, no corpo da mensagem. O CI recusa campos ou formatos incompletos; um handoff ruim já enviado se corrige com outro commit `handoff(...)` do mesmo grupo, sem push forçado (vale o último no intervalo):

   ```text
   handoff(Fxx-gN): <resumo>

   Feito: …
   Contrato: <rotas, corpos e tipos definidos ou usados; schema do servidor conferido> (ou "não toca contrato")
   Testes: …
   Mutações: <teste> ← <mutação> (falhou)
   Evidência: <onde ficam no repo as provas citadas; o que você observou e o que foi relatado, com commit ou hash>
   CI: <run> verde
   Desvios da spec: <diff comparado com Interfaces e Requisitos, item por item> (ou "nenhum")
   ```

4. Faça push **somente** da branch do grupo e espere o CI verde também no commit final. Informe o run final a quem integra. Não declare o grupo fechado sem esse resultado; se o ambiente impedir o push, relate o impedimento sem inventar evidência.
