---
name: skill-pessoal
description: Cria, muda ou remove skills mantidas neste repositório para uso no Claude Code e no Codex. Use quando o usuário pedir uma skill pessoal, para todos os projetos ou centralizar uma skill local; não ativa para executar a tarefa que outra skill já cobre.
---

# Manter uma skill central

Localize o clone autorizado de `agent-skills` e leia `AGENTS.md`, `README.md` e
`TERCEIROS.md`. Não suponha um caminho pessoal fixo nem que exista um clone no computador.
Se ele não estiver acessível, prepare um patch em workspace autorizado e explique a limitação.

1. Confirme o escopo: geral em `skills/<nome>/`; específica em
   `projetos/<projeto>/skills/<nome>/`. Nome em kebab-case igual à pasta, descrição que
   discrimine quando usar. Mantenha a entrada curta; detalhes em referências relativas.
2. Use exemplos genéricos. Não copie planos privados, nomes de pessoas, clientes, contas,
   credenciais, emails ou prazos pessoais para este repositório público.
3. Preserve as skills de terceiros sem alteração, seguindo `TERCEIROS.md`. Para conteúdo
   próprio, use a orientação `skill-creator` disponível e exemplos positivos e negativos.
4. Rode `python3 scripts/conferir.py` e os testes da skill alterada. Revise o diff. Não
   instale no HOME real durante testes; use diretórios temporários e `--dry-run`.
5. Entregue mudanças e resultado dos testes. Criar/editar uma skill não autoriza por si só
   push, PR, merge ou instalação no computador. Publique ou instale somente dentro da
   autorização do usuário; prefira revisão em branch separada.

Para sincronizar cópias locais, revise primeiro `scripts/sincronizar.sh` e o diff produzido.
Em modo link, editar a instalação altera diretamente o clone: confira o destino real antes
de escrever. Para remover, identifique dependências e instalação; não apague conteúdo local
ou links fora do escopo aprovado. Não prometa propagação ao cloud antes de verificar a
versão instalada e os pré-requisitos daquele ambiente.
