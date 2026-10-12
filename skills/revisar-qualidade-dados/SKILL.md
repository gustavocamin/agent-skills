---
name: revisar-qualidade-dados
description: Revisa qualidade de dados ligando regras de negócio a métricas, limites, testes e tratamento de falhas. Use para avaliar tabelas ou pipelines, definir validações e planejar reprocessamento ou exceções; não para aprovar números apenas por um perfil estatístico, otimizar consultas isoladas ou executar limpeza em produção sem autorização.
---

# Revisar qualidade de dados

Comece pelo uso do dado e pelo erro que prejudica esse uso. Perfil estatístico ajuda a
descobrir problemas, mas não define sozinho o que está correto nem o que o negócio aceita.

## Revisão

1. **Fixar o contrato.** Identifique consumidor, decisão atendida, granularidade, chaves,
   universo e janela de avaliação. Busque a regra na fonte de negócio; se não existir,
   registre a hipótese e quem pode validá-la, sem inventar um limite de produção.
2. **Traduzir a regra.** Ligue cada regra a dimensão de qualidade, métrica, denominador,
   tratamento de nulos/duplicatas/atrasos e critério de aprovação. Distinga limite aprovado,
   candidato e alerta exploratório. Registre gravidade e consequência da falha. Responsável
   só é confirmado com evidência; sem ela, marque "a confirmar" e proponha quem validar,
   sem atribuir compromisso a uma pessoa.
3. **Verificar evidências.** Leia validações existentes e resultados disponíveis. Se a
   execução estiver no escopo, use consultas limitadas e fontes autorizadas; mostre população,
   período e limitações. Uma amostra aprovada não comprova a qualidade da população inteira.
4. **Derivar testes.** Cubra caso válido, inválido, fronteira e casos vazios ou tardios
   relevantes, com resultado esperado. Separe testes da regra, da transformação e do fluxo
   operacional. Diga o que foi executado, apenas proposto ou ficou inconclusivo.
5. **Planejar a resposta.** Para falhas, explicite bloquear, alertar ou colocar em quarentena,
   sem descartar silenciosamente. Defina correção na origem, reprocessamento idempotente,
   reconciliação e exceções com dono confirmado (ou "a confirmar") e validade. Propostas
   não atribuem responsabilidade nem autorizam execução destrutiva.

## Entrega

Entregue uma tabela por regra com **fonte → dimensão → métrica/limite → testes/evidência →
tratamento/dono**, seguida das principais lacunas e próximos passos. Prefira as regras que
protegem decisões críticas, evitando um catálogo de checks sem consequência definida.

Leia [o contrato e os casos de teste](references/contrato-e-testes.md) ao especificar métricas,
reprocessamento ou exceções, e para conferir exemplos positivos e negativos de acionamento.
Não publique amostras privadas ou segredos nos resultados. Não altere tabelas, regras de
produção, permissões ou agendas sem o escopo e a autorização correspondentes; se só foi
pedida uma revisão, entregue achados e propostas.
