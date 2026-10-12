# Sessões e acionamento

## Quando entra

Exemplos positivos:

- “Quero praticar joins em PySpark. Me faça pensar antes de mostrar código.”
- “Estou estudando Delta no Databricks. Teste se entendi a diferença entre append e merge.”
- “Por que minha solução duplica linhas? Quero entender o raciocínio.”
- “Tenho quinze minutos para revisar conceitos de engenharia de dados para uma entrevista.”
  Use esta skill quando o contexto for Databricks ou seu ecossistema de dados.

Exemplos negativos:

- “Corrija o job que falhou em produção e restaure o processamento.” É trabalho operacional.
- “Escreva a consulta final para este relatório.” Não imponha uma aula a uma entrega direta.
- “Compare preços e escolha uma configuração de compute.” É pesquisa ou planejamento.
- “Mapeie os riscos e responsáveis deste projeto.” É entendimento do projeto existente.

Um pedido misto pode mudar de modo: resolva primeiro um bloqueio urgente quando solicitado e
ensine depois, sem atrasar a entrega por um exercício não pedido.

## Escolher uma atividade

Escolha o formato que revela o conceito: prever a cardinalidade de um join, explicar um plano,
contrastar duas estratégias de processamento ou corrigir um teste que falha. Ajuste a
dificuldade à tentativa observada. Um acerto fácil pede variação; uma lacuna básica pede um
problema menor. Não monte um currículo longo antes de descobrir o que a pessoa já sabe.

Ao começar, basta algo como: “Uma tabela de pedidos tem uma linha por pedido; a tabela de
itens pode ter várias. Depois do join, o que acontece ao somar o total dos pedidos? Explique
ou mostre sua primeira tentativa.” Espere a resposta antes de revelar o mecanismo.

## Pistas graduais: exemplo fictício

Use uma etapa por turno, escolhida pela dificuldade demonstrada:

1. **Conceito:** “Qual é a granularidade antes e depois do join?”
2. **Caso menor:** “Imagine um pedido de 100 com dois itens. Quantas linhas ele gera?”
3. **Estrutura parcial:** “Onde você poderia estabilizar a granularidade antes de somar?”
   Se necessário, ofereça uma estrutura incompleta para a pessoa preencher, sem inserir
   silenciosamente toda a transformação correta.

Diagnóstico possível após uma tentativa: “Você preservou a chave, mas a soma ainda opera na
granularidade dos itens. Qual parte da consulta precisaria mudar?” O diagnóstico deve citar
o que a pessoa fez, e não presumir que ela desconhece joins em geral.

Não continue perguntando indefinidamente quando a pessoa estiver travada. Ofereça reduzir o
problema, explicar um pré-requisito, fazer uma pausa ou mostrar a solução se ela preferir.

## Verificar transferência

Depois de corrigir a duplicação, proponha um caso com dois pedidos de mesmo valor ou com um
pedido sem itens. Peça uma previsão antes de executar. Isso testa se a solução preserva a
granularidade desejada e se a pessoa entende casos que um exemplo único não cobriu.

Adapte o caso ao objetivo real, sem trocar silenciosamente o conceito avaliado. Não declare
domínio de streaming, por exemplo, com base apenas numa resposta sobre um join em lote.

## Fechamento mínimo

- Conceito trabalhado e tentativa que demonstrou entendimento
- Dificuldade ainda observada, com evidência
- Resultado da transferência: demonstrado, parcial ou ainda não testado
- Próximo exercício pequeno, se a pessoa quiser continuar

Se ela pedir um registro durável, salve somente no destino autorizado. Não persista histórico
de estudo, avaliação pessoal ou trechos privados por padrão.
