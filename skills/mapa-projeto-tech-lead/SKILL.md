---
name: mapa-projeto-tech-lead
description: Mapeia um projeto técnico existente para uma liderança entender contexto, responsabilidades, arquitetura, riscos e decisões com evidências. Use para assumir, revisar ou destravar um projeto em andamento; não para iniciar um projeto do zero, criar especificações de implementação ou impor um novo fluxo de desenvolvimento.
---

# Mapa de projeto para tech lead

Produza uma visão utilizável do estado atual: uma página de síntese e uma tabela de evidências,
lacunas e próximos passos. Ajuste ao formato pedido; não crie um pacote de governança por
padrão nem confunda o mapa com um plano de execução.

## Construir a partir de evidências

1. Delimite o projeto, o momento retratado e a decisão que o mapa precisa ajudar. Use fontes
   disponíveis e autorizadas: código, documentação, issues, entregas, operação e conversas.
   Se o acesso for parcial, faça o mapa parcial e diga o que não foi possível verificar.
2. Inspecione as oito dimensões abaixo. Priorize o que pode mudar uma decisão; a ausência de
   documento não prova ausência de prática. Não trate uma proposta ou um README antigo como
   retrato confirmado da implementação atual.
3. Separe **fato observado**, **inferência** e **não confirmado**. Para cada fato relevante,
   registre fonte localizável e data, revisão ou período quando disponível. Registre conflitos
   entre fontes sem escolher arbitrariamente uma versão.
4. Para cada lacuna relevante, indique impacto, responsável confirmado ou “a confirmar” e
   próxima ação verificável. Uma pessoa citada ou autora de um commit não vira responsável
   automaticamente; diferencie dono do projeto, dono da decisão e contato para investigação.
5. Entregue a síntese, a tabela e as poucas perguntas que realmente desbloqueiam decisões.
   Recomendar uma ação não a executa: não crie tickets, altere o projeto ou contate pessoas
   apenas para preencher o mapa.

## Oito dimensões

1. **Negócio e resultado:** problema, usuários, resultado esperado e como o sucesso é medido.
2. **Pessoas e responsabilidade:** decisão, execução, operação, aprovação e dependências humanas.
3. **Arquitetura e fluxo de dados:** fronteiras, componentes, entradas, transformações e saídas.
4. **Qualidade de dados:** regras críticas, cobertura de validação e impacto de falhas.
5. **Entrega e dependências:** estado comprovado, marcos, bloqueios e dependências externas.
6. **Operação e confiabilidade:** monitoramento, incidentes, recuperação e objetivos de serviço.
7. **Segurança e governança:** acesso, classificação, retenção e obrigações aplicáveis conhecidas.
8. **Custos e decisões:** consumo, fatores de custo, escolhas, alternativas e critérios pendentes.

Use [o modelo e os exemplos](references/modelo.md) para montar a entrega ou esclarecer o
acionamento. Marque “não se aplica” somente com justificativa; “não foi encontrado” é lacuna.
Não reproduza segredos ou amostras sensíveis: resuma o achado e cite uma referência apropriada
ao público da entrega. Não publique nem amplie acesso às fontes para facilitar o mapa.
