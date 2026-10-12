# Modelo mínimo e exemplos

## Quando entra

Exemplos positivos:

- “Vou assumir este projeto. Quero entender o que entrega, quem decide e onde estão os riscos.”
- “Use o repositório e estes documentos para montar um mapa do estado atual.”
- “O pipeline já existe, mas ninguém sabe quais dependências bloqueiam a próxima entrega.”
- “Revise o mapa anterior à luz destes incidentes e mudanças de arquitetura.”

Exemplos negativos:

- “Comece um aplicativo do zero e defina a arquitetura.” É criação de projeto.
- “Escreva a spec desta funcionalidade e implemente por etapas.” É desenvolvimento.
- “Conserte esta consulta SQL.” É uma correção pontual, sem pedido de mapa.
- “Faça um organograma da empresa inteira.” O escopo não é um projeto técnico existente.

## Uma página de síntese

Use frases curtas e as fontes da tabela como referências; evite repetir todas as linhas.

- **Escopo e retrato:** projeto, data, versão/período e fontes acessíveis
- **Resultado:** quem usa, problema resolvido, resultado esperado e métrica conhecida
- **Funcionamento:** fluxo principal de entrada a saída, com fronteiras e dependências
- **Estado comprovado:** o que funciona, o que está em construção e o que está bloqueado
- **Riscos prioritários:** consequência, evidência, urgência e mitigação candidata
- **Decisões necessárias:** decisão, dono confirmado ou a confirmar, informação que falta
- **Próximos passos:** ações pequenas, em ordem de impacto, que reduzem as principais lacunas

Não invente datas ou percentuais de conclusão. Quando uma alegação só aparece numa reunião,
registre-a como relato atribuído, não como verificação técnica. Se não houver evidência para
um estado, escreva “não confirmado” em vez de usar uma cor de saúde arbitrária.

## Tabela de apoio

Uma linha por dimensão é o ponto de partida; divida apenas quando houver mais de uma questão
que exige responsáveis ou ações diferentes. As perguntas abaixo orientam a coleta, não são
um questionário obrigatório para a pessoa preencher.

| Dimensão | O que verificar |
| --- | --- |
| Negócio e resultado | Usuário, resultado, critério de sucesso e impacto de não entregar |
| Pessoas e responsabilidade | Quem decide, implementa, opera e aceita o resultado |
| Arquitetura e fluxo de dados | Origem → processamento → armazenamento → consumo; fronteiras e contratos |
| Qualidade de dados | Regras críticas, testes existentes, lacunas e tratamento de dados inválidos |
| Entrega e dependências | Evidência de entrega, próximos marcos e bloqueios internos/externos |
| Operação e confiabilidade | Alertas, objetivos de serviço, falhas recentes e restauração/reprocessamento |
| Segurança e governança | Acesso efetivo, classificação, retenção e obrigações confirmadas |
| Custos e decisões | Medição, principais fatores de custo e decisões com alternativas e critérios |

Preencha a tabela de saída com estas colunas:

| Dimensão | Fato ou inferência e fonte | Lacuna ou conflito e impacto | Responsável | Próxima ação |
| --- | --- | --- | --- | --- |
| Operação e confiabilidade | Fato observado: o teste de restauração consta no relatório de ensaio, seção 2, revisão consultada | Não confirmado: o ensaio cobre o ambiente em uso; risco de recuperação não demonstrada | A confirmar; o relatório não define quem responde pela recuperação | Comparar escopo do ensaio com a configuração atual e confirmar o dono da recuperação |

A linha acima é um exemplo fictício de redação, não um achado reutilizável.

## Fontes e tratamento de incerteza

- Código/configuração: caminho e trecho ou símbolo, com revisão quando disponível.
- Issues, decisões e documentos: link ou identificador local, seção e data/revisão.
- Métricas e operação: origem, janela observada e limitações de cobertura.
- Relatos: pessoa ou papel atribuído na fonte e contexto; sinalize que não foram verificados.

Mantenha referências acessíveis ao público autorizado do mapa. Se precisar restringir detalhes,
descreva a evidência sem copiar dados protegidos; não prometa acesso que você não verificou.

Conflito útil: “O documento descreve execução diária; a configuração consultada indica outra
frequência. Não foi verificado qual versão está implantada.” A próxima ação é verificar o
deploy, não alterar o agendamento para torná-lo igual ao documento.

Use prioridade qualitativa sustentada por consequência e urgência. Não derive certeza de uma
pontuação inventada nem transforme toda lacuna em bloqueio. Pare quando houver cobertura das
oito dimensões com evidências ou lacunas explícitas e próximos passos suficientes para a
decisão pedida; investigação adicional pode ser recomendada separadamente.
