---
name: comms-check
description: Faz o check-in de um plano de prática de comunicação fornecido pelo usuário, comparando semana, marcos e registros. Use para acompanhar esse ciclo; não conduz simulação executiva, escreve respostas de treino nem faz a revisão semanal geral do vault.
---

# Comms-check

Acompanhe o ciclo de comunicação sem registrar progresso pelo usuário. Esta é a
fonte canônica do fluxo no Claude Code (`/comms-check`) e no Codex (`$comms-check`).

## Entradas e ambiente

- Leia as regras do vault e o plano vigente indicado pelo usuário ou identificado
  inequivocamente no contexto autorizado. Se houver mais de um, pergunte qual vale.
- Do plano, extraia início, duração, limites da semana, pausas, checklists, tipos de
  sessão, marcos e sinais de atenção. Não presuma ciclo de 12 semanas, dias fixos,
  evento externo, data de prova ou ligação com outro projeto.
- Declare a data e o fuso de referência do pedido ou do ambiente e cite as fontes das
  datas. Dados ausentes ou conflitantes ficam desconhecidos, nunca preenchidos com
  datas históricas, exemplos ou preferências presumidas.
- Leia Markdown acessível, local ou no cloud. Sem o plano acessível, peça o arquivo
  ou trecho necessário. A [Obsidian CLI](https://help.obsidian.md/cli) precisa do app
  desktop em execução; estes arquivos de skill não tornam a CLI disponível no cloud
  nem sincronizam o vault.

## Preparar o check-in

1. Calcule a semana apenas com calendário suficiente. Antes do início confirmado,
   apresente a primeira sessão prevista; durante pausa declarada, não cobre falha;
   após o término previsto, sugira retrospectiva sem inventar outra semana.
   Sem datas suficientes, acompanhe o checklist sem numerar a semana nem alegar atraso.
2. Mostre itens marcados e abertos da semana, e os abertos da anterior quando houver.
   Diferencie "não registrado" de "não feito"; se houver evidência de execução mas
   checkbox vazio, peça confirmação sem marcar nada.
3. Identifique o tipo de semana/sessão somente se estiver registrado. Inclua os marcos
   que o plano vincula à semana atual, sem importar regras de outro ciclo.
4. Avalie sinais de atenção apenas contra os gatilhos definidos no plano e com
   evidência observável. Falta de dados gera "não foi possível avaliar", não falha.
5. Cruze carga com planos paralelos fornecidos ou referenciados, apontando picos
   simultâneos comprovados. Qualquer ajuste fica como proposta, sem replanejamento.

## Saída e limites

Entregue na conversa por padrão. Só crie ou atualize relatório com autorização de escrita
explícita neste pedido ou uma autorização vigente que cubra esse relatório e destino.
Uma pasta configurada indica localização, não permissão. Pedidos de somente leitura ou
resposta só na conversa prevalecem; sem autorização, não persista o resultado.


Resumo curto com fontes, data de referência, semana/tipo (ou "desconhecido"),
atividades previstas, feito registrado, pendências anteriores, marcos e sinais.
Para cada sinal, mostre critério e evidência; se não houver evidência suficiente,
diga qual entrada falta.

Com escrita autorizada e pasta de relatórios definida nas regras do vault ou pelo usuário, gere
`Comms-check YYYY-MM-DD.md` ali; caso contrário, entregue na conversa. Reexecuções
atualizam somente conteúdo gerado, após ler o arquivo existente, preservando texto
manual e evitando duplicatas. Conflito de autoria exige confirmação.

- Plano, banco de exercícios e demais notas ficam somente leitura.
- Não marcar checkboxes, redefinir cronograma ou executar treino pelo usuário.
- Para preparar ou avaliar uma simulação executiva, use a skill existente `exec-sim`;
  o check-in não mantém uma segunda versão dessa rotina.

## Exemplos de ativação

- Ativa: "Confira a semana atual deste plano de comunicação e o que ficou pendente."
- Ativa: "Meu ciclo está pausado; o que o plano prevê para a retomada?"
- Não ativa: "Revise a transcrição do meu simulador executivo" (é `exec-sim`);
  "faça a revisão semanal de todos os meus projetos" (é `thinking-tools`, `/week`).
