# Contrato, testes e tratamento

## Quando entra

Exemplos positivos:

- “Revise a qualidade desta tabela antes de ela alimentar o painel comercial.”
- “Transforme estas regras de negócio em validações com métricas e limites.”
- “O pipeline aceita duplicatas. Defina os testes e como tratar reprocessamentos.”
- “Quero revisar as exceções atuais e saber se mascaram problemas de qualidade.”

Exemplos negativos:

- “Deixe esta consulta mais rápida.” É otimização, salvo se também houver dúvida de correção.
- “Apague todos os registros suspeitos.” Não assuma a regra nem a autorização de revisão
  como permissão de apagar; esclareça critério e siga as permissões da ação solicitada.
- “Ensine joins com exercícios.” É tutoria.
- “Monte um gráfico destes dados.” Não imponha uma auditoria completa sem necessidade.

## Contrato de uma regra

Registre o mínimo que torna o resultado reproduzível:

| Campo | O que explicitar |
| --- | --- |
| Regra e fonte | Comportamento de negócio, fonte, versão/data e responsável por confirmar |
| Escopo | Entidade, granularidade, chave, filtros e população elegível |
| Tempo | Janela, fuso, tempo do evento ou ingestão, corte e tolerância de atraso |
| Dimensão | O atributo de qualidade que a regra protege |
| Métrica | Fórmula, unidade, numerador, denominador e agregações |
| Semântica | Nulo, vazio, duplicata, igualdade, arredondamento e denominador zero |
| Aprovação | Operador e limite; aprovado, candidato ou exploratório |
| Resultado | Valor, período, fonte de execução e aprovado/falhou/inconclusivo |
| Resposta | Gravidade, impacto, ação, dono e condição de resolução |

“Sem dados” pode ser uma falha de volume ou um período legítimo sem atividade; não converta
automaticamente denominador zero em 100% de aprovação. O contrato deve decidir ou registrar
o resultado como inconclusivo. Diferencie limite por linha, por lote e por janela móvel.

## Dimensões que ajudam a escolher a métrica

- **Completude:** proporção preenchida entre os registros em que o campo é exigido.
- **Unicidade:** duplicação na chave e granularidade acordadas; repetição pode ser legítima.
- **Validade:** conformidade com domínio, formato, faixa ou regra aplicável.
- **Consistência:** concordância entre campos, estados, sistemas ou etapas comparáveis.
- **Integridade referencial:** referências sem correspondente no universo e instante definidos.
- **Atualidade:** idade do dado ou atraso em relação ao momento exigido pelo consumidor.
- **Exatidão:** correspondência com referência confiável; formato válido não demonstra exatidão.
- **Volume/cobertura:** ausência ou mudança de cobertura esperada; anomalia é sinal, não prova
  de erro sem levar em conta sazonalidade, calendário e mudanças conhecidas.

Use somente as dimensões relevantes; uma regra pode precisar de mais de uma métrica. Um bom
valor agregado não elimina falhas num segmento crítico. Explicite o nível de desagregação
necessário antes de escolher um limite global.

## Exemplo fictício: unicidade de pedido

Regra: “A saída publicada contém uma linha por pedido elegível.” Fonte: contrato fictício do
consumidor. A confirmação desse contrato é pré-requisito para usar a regra num projeto real.

- Universo: pedidos elegíveis no corte acordado, após o tratamento de eventos definido.
- Chave: identificador do pedido; nulidade da chave é validada por uma regra separada.
- Métrica de duplicação: linhas com chave preenchida menos quantidade de chaves distintas,
  divididas pelo total de linhas com chave preenchida, no mesmo escopo.
- Limite candidato: zero linhas excedentes, caso o dono confirme unicidade estrita.
- Exemplo: chaves `[A, A, B]` geram 1 linha excedente em 3, não “1 pedido duplicado em 2”.
  As duas métricas são diferentes; escolha a que representa a consequência avaliada.
- Universo vazio ou todas as chaves nulas: não há denominador para esta métrica. Avalie a
  regra separada de volume/completude e não registre aprovação automática de unicidade.

Não copie este limite ou chave para outras tabelas sem verificar granularidade e contrato.

## Matriz de testes

Para cada regra, derive entradas pequenas com saídas esperadas; prefira dados sintéticos.

| Caso | O que demonstrar |
| --- | --- |
| Válido | Um dado conforme passa e preserva o resultado de negócio |
| Inválido | A violação escolhida é detectada e recebe a resposta definida |
| Fronteira | O valor igual ao limite e seus vizinhos obedecem ao operador acordado |
| Nulo/vazio | Ausência de campo, tabela vazia e denominador zero têm estados explícitos |
| Duplicata | Repetição legítima e repetição indevida são separadas pela granularidade |
| Atraso | Eventos dentro e fora da tolerância seguem a política de fechamento/correção |
| Reexecução | Rodar a mesma entrada novamente não altera indevidamente o resultado final |
| Evolução | Mudança de esquema ou regra não converte dados incompatíveis em aprovação |

Adapte os casos ao risco, sem exigir todos para qualquer campo. Registre evidência da
execução, comparação com o esperado e limites do ambiente. Uma consulta escrita mas não
executada é um teste proposto. Ausência de acesso a uma referência torna exatidão inconclusiva.

## Falhas, reprocessamento e exceções

Antes de recomendar reprocessamento, identifique período/partições/chaves afetados, origem
reproduzível, consumidores e efeitos colaterais. Especifique:

1. Correção da causa e versão de transformação/regra a usar.
2. Simulação ou ensaio isolado, estimativa de volume/custo e critério para prosseguir.
3. Escrita idempotente, deduplicação e política para eventos tardios; não presuma que repetir
   um job é seguro só porque as entradas são iguais.
4. Reconciliação antes/depois: contagens, somas ou invariantes relevantes, e ausência de
   efeitos duplicados nos destinos e notificações.
5. Critério de sucesso, observação pós-execução e forma de recuperar o estado anterior quando
   tecnicamente possível; se não for, explicite o risco antes da execução autorizada.

Uma exceção precisa de regra afetada, justificativa, escopo restrito, responsável/aprovador,
validade ou condição de revisão e forma de acompanhar impacto. Não esconda exceções no
denominador: mostre separadamente população total, excluída e avaliada, com reconciliação.
Exceção vencida ou sem dono volta como pendência, não como autorização tácita.

Quarentena preserva rastreabilidade sem divulgar dados indevidamente. Não confunda separar
registros para revisão com descartá-los definitivamente. Publicar dados parciais requer um
critério de negócio explícito para a consequência nos consumidores.
