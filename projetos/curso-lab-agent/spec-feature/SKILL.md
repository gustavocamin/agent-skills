---
name: spec-feature
description: Planeja uma feature do roadmap no formato spec-first — entrevista o Gustavo e gera plan.md, requirements.md e validation.md em specs/features/Fxx-nome/, com o dono de cada grupo de tarefas (Claude Code ou Codex). Use quando ele pedir para planejar, especificar ou começar uma feature, antes de qualquer código.
---

# spec-feature

Não escreva código nesta skill. O produto é a spec.

## Passos

1. Leia `AGENTS.md` e `specs/constitution/` (mission, tech_stack, roadmap).
2. Identifique a feature (ID e nome no roadmap). Se o pedido não está no roadmap, pare e sugira a skill `replan`.
3. Crie a branch `feature/Fxx-<nome-curto>` a partir da `main`.
4. **Entreviste antes de escrever.** Rodadas curtas (3–5 perguntas), cobrindo:
   - escopo: o que entra e o que fica para outra feature;
   - requisitos: comportamento observável esperado;
   - validação: como ele vai saber que ficou bom (automático e humano);
   - riscos: segredos, custo, limites da Free Edition, invariantes do `AGENTS.md` afetados.
   Não pergunte o que a constituição já responde.
5. Crie `specs/features/Fxx-<nome-curto>/` a partir de `specs/features/_template/` e preencha os três arquivos. O template é somente leitura: um arquivo copiado herda isso, então libere a escrita só nos arquivos novos. Nível de detalhe: muito contexto de objetivo, público e restrições; pouco micromanagement de implementação. Tarefas em grupos implementáveis sozinhos; marque ⚠ os que tocam segredos, workspace Databricks ou `exam_map`.
   - **Dono por grupo:** proponha `Dono: Claude Code`, `Dono: Codex (cloud)` (o padrão para grupo do Codex sem ⚠) ou `Dono: Codex` (local, para grupo ⚠ ou quando o cloud não servir) na linha logo abaixo do título de cada grupo, com `Branch` quando o grupo roda fora da branch da feature e `Toca` em todo grupo quando o plano tem os dois donos. O formato e o protocolo estão no `AGENTS.md` (seção "Dois agentes").
   - Grupos de donos diferentes só correm em paralelo com `Toca` disjunto; grupos ⚠ nunca correm em paralelo; o Codex só é dono de grupo ⚠ fora do cloud.
   - **Quem integra:** proponha a linha `Integra: Claude Code` logo abaixo do título do `plan.md`. `Integra: Codex` só entra se o Gustavo pedir.
   - **Contrato:** se um grupo define rotas ou corpos entre cliente e servidor e outro os consome, diga no plano qual grupo é o do contrato. A seção Interfaces do `requirements.md` lista o corpo de cada pedido e de cada resposta, com os nomes dos campos.
   - No `validation.md`, preencha o "Registro dos grupos" com uma linha por grupo (dono e branch); o resto da linha é de quem integra.
6. Mostre um resumo de uma tela, com o dono de cada grupo, e peça correções. Aplique-as nos três arquivos de forma consistente.
7. Commit só das specs: `spec(Fxx): plano, requisitos e validação`.
8. Termine lembrando: abrir uma conversa nova antes de implementar (`/clear` no Claude Code; `/new` no Codex CLI ou uma conversa nova no app do ChatGPT) e pedir "implemente o Grupo N da Fxx" ao dono do grupo, que segue a skill `implementar-grupo` (`$implementar-grupo` no Codex, `/implementar-grupo` no Claude Code).
