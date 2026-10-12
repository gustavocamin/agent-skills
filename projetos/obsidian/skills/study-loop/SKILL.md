---
name: study-loop
description: Prepara uma sessão de estudo a partir do plano e dos registros fornecidos pelo usuário, com revisão espaçada e pendências administrativas. Use para acompanhar um ciclo de estudo ou certificação; não resolve exercícios nem substitui a revisão semanal geral do vault.
---

# Study-loop

Prepare a sessão; a recuperação ativa e as respostas são do usuário. Esta é a
fonte canônica do fluxo, tanto no Claude Code (`/study-loop`) quanto no Codex
(`$study-loop`).

## Entradas e ambiente

- Leia as regras do vault e o plano vigente indicado pelo usuário ou identificado
  inequivocamente no contexto autorizado. Use a nota do projeto, o histórico de
  estudo e o guia de objetivos somente quando fornecidos ou referenciados por ele.
  Com vários planos candidatos, pergunte qual usar; não presuma tema nem pasta.
- Extraia do plano as datas, etapas, pausas, revisões, prova e prazos administrativos.
  Registre a fonte de cada prazo. A data e o fuso de referência vêm do pedido ou do
  ambiente, com o fuso declarado; não transforme uma data de exemplo em compromisso.
- Se faltarem plano, início, duração ou histórico, diga o que está desconhecido e
  peça apenas o dado necessário. Ausência de registro não prova ausência de estudo.
- Opera sobre Markdown acessível, local ou no cloud. Não pressupõe sincronização nem
  acesso ao vault pessoal: sem arquivos acessíveis, peça o plano ou um trecho dele.
  A [Obsidian CLI](https://help.obsidian.md/cli) requer o app desktop em execução;
  instalar uma skill no cloud não fornece esse app nem acesso à sessão local.

## Preparar a sessão

1. Determine a etapa e o intervalo atuais somente se o calendário do plano permitir.
   Antes do início, mostre a próxima etapa; numa pausa explícita, respeite a pausa;
   depois do fim, reporte encerramento e a próxima etapa apenas se prevista.
   Datas conflitantes ou plano aparentemente antigo ficam sinalizados para confirmação.
2. Reúna as atividades que o plano pede hoje ou nesta semana (lições, labs e práticas).
   Sem calendário suficiente, liste as próximas atividades em aberto sem atribuir
   semana, atraso ou data de prova.
3. Calcule revisões com os intervalos do plano e as datas efetivamente registradas.
   Se não houver protocolo ou histórico suficiente, marque revisão como desconhecida;
   não aplique automaticamente janelas de um dia ou uma semana.
4. Liste objetivos ainda não auditados, priorizando os da etapa atual, e pendências
   administrativas com seus prazos comprovados. Não invente voucher, plataforma de
   prova, agendamento ou deadline; um checkbox vazio significa apenas não registrado.
5. Compare a próxima ação da nota com o plano vigente. Proponha eventual atualização
   no relatório, sem editar a nota. Cruze a carga com outros planos só quando forem
   fornecidos ou referenciados; sinalize conflitos observáveis sem reagendar nada.

## Saída e limites

Entregue na conversa por padrão. Só crie ou atualize relatório com autorização de escrita
explícita neste pedido ou uma autorização vigente que cubra esse relatório e destino.
Uma pasta configurada indica localização, não permissão. Pedidos de somente leitura ou
resposta só na conversa prevalecem; sem autorização, não persista o resultado.


Entregue um resumo curto com: fontes e data de referência; etapa/semana (ou
"desconhecida"); sessão; revisão espaçada; objetivos; administrativo; sinais e
perguntas pendentes. Cite as seções que sustentam atividades e datas.

Com a escrita autorizada e a pasta de relatórios definida pelas regras do vault ou pelo usuário,
gere `Study-loop YYYY-MM-DD.md` ali; senão, entregue na conversa e pergunte o destino
somente se a persistência for necessária. Leia um relatório existente antes de
atualizar: preserve texto manual, não duplique seções e peça confirmação se não for
possível distinguir o conteúdo gerado. Não sobrescreva arquivos alheios ao fluxo.

- Somente leitura no plano, registros e nota do projeto; escrita limitada ao relatório.
- Não marque checkboxes, responda exercícios/simulados ou escreva resumos de estudo
  pelo usuário. Não adote mudanças de calendário ou de próxima ação automaticamente.

## Exemplos de ativação

- Ativa: "Prepare a sessão de hoje com este plano e meu registro de estudos."
- Ativa: "O que revisar e quais pendências administrativas há nesta certificação?"
- Não ativa: "Resolva este simulado por mim"; "faça a revisão semanal do vault"
  (o último é `thinking-tools`, modo `/week`).
