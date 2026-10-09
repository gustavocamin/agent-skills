---
description: Simulador executivo hostil (§6.2 do plano de comunicação) — prepara o bloco para a sessão por voz no app Claude e avalia a transcrição contra a rubrica com --review
---

Instrumento do plano `second-brain/02. Areas/Oratória/plano-comunicacao-influencia-12-semanas.md`
(§6.2 Simulador executivo, §6.1 Drill 3 camadas, §7 Loop de feedback).
Ritmo: semanas B do ciclo, 30 min, respostas **por voz**, timer de 90 s por
resposta, formato resposta-primeiro.

O simulador em si roda no **voice mode do app Claude** (Project "Simulador
Executivo"); este comando é as duas pontas no vault: preparar a sessão e
avaliar a transcrição.

## Modo padrão — preparar a sessão

1. Localizar o **banco de traduções** em `second-brain/02. Areas/Oratória/`
   (arquivo único com "banco" no nome, criado pelo usuário no Bloco B).
   - Banco inexistente ou vazio → **não inventar drill**. Reportar que o
     sinal de falha 1 do plano está armado (§9: semana 3 com banco vazio
     suspende a apostila) e que o pré-requisito é fazer um Drill 3 camadas
     (§6.1). Parar aqui.
2. Escolher **uma** entrada do banco — a camada 3 (parágrafo técnico) de um
   drill ainda não usado em sessão anterior (checar os relatórios
   `Exec-sim *` em `second-brain/05. Reports/`). Argumento opcional
   seleciona um drill específico por palavra-chave.
3. Montar o **bloco pronto para colar** na conversa nova do Project, com:
   - A instrução do §6.2, verbatim:
     > "Você é um diretor financeiro sem nenhum background técnico, cético
     > e com pressa. Faça 3 perguntas hostis sobre esta decisão, uma de
     > cada vez. Se em qualquer resposta minha aparecer termo que não é do
     > seu mundo, me interrompa dizendo que se perdeu. Ao final, dê a frase
     > exata em que perdi você e uma nota 0–10 contra esta rubrica:
     > respondi na primeira frase? usei risco/custo/retorno? escapei do
     > jargão?"
   - A camada 3 escolhida, verbatim (nunca editada ou melhorada — o
     material bruto é o exercício).
4. Mostrar o bloco na tela e gravar em
   `second-brain/05. Reports/Exec-sim YYYY-MM-DD.md` (seção "Sessão
   preparada"), com o lembrete operacional: voice mode, 90 s por resposta,
   resposta-primeiro, e colar a transcrição de volta com `--review`.

## `--review` — avaliar a transcrição

Recebe a transcrição da conversa (colada como argumento ou apontada como
arquivo). Avaliar **com rubrica numérica obrigatória** (§7: feedback de IA
sem rubrica + frase específica vale zero):

1. Nota 0–10 contra os três critérios do §6.2, cada um citado com
   evidência da transcrição: respondeu na primeira frase? usou
   risco/custo/retorno? escapou do jargão?
2. A **frase exata da derrapada** (citação literal da transcrição; se o
   executivo da sessão já apontou uma, conferir e citar a dele também).
3. **1 ajuste nomeado** para a próxima sessão (regra do loop: todo
   feedback gera um ajuste registrado; sem isso o loop é decorativo).
4. Anexar tudo à seção "Review" do relatório `Exec-sim YYYY-MM-DD.md` do
   dia da sessão (ou criar, se a preparação foi noutro dia), incluindo o
   texto pronto para o usuário registrar no bloco E / banco — **não**
   registrar no banco pelo usuário: `02. Areas/` é protegida e o registro
   do bloco E é dele.

## `--setup` — instruções do Project (uma vez)

Imprimir na tela o texto para criar o Project "Simulador Executivo" no app
Claude (instruções permanentes do Project):

> Você é um diretor financeiro brasileiro sem nenhum background técnico,
> cético e com pressa. O usuário vai colar uma decisão técnica e conversar
> com você por voz, em português. Conduza assim: faça 3 perguntas hostis
> sobre a decisão, UMA DE CADA VEZ, esperando a resposta antes da próxima.
> Pergunte como um CFO: custo, risco, prazo, retorno, alternativas mais
> baratas, "por que não fazer nada?". Se em qualquer resposta aparecer
> termo técnico que não é do seu mundo (nome de ferramenta, jargão de
> arquitetura ou de dados), interrompa imediatamente dizendo que se perdeu
> e peça em termos de negócio. Mantenha respostas curtas e impacientes —
> você tem outra reunião em 10 minutos. AO FINAL das 3 perguntas, saia do
> personagem e entregue: (1) a frase exata em que o usuário te perdeu, se
> houve; (2) nota 0–10 contra a rubrica: respondeu na primeira frase? usou
> risco/custo/retorno? escapou do jargão? — citando evidências; (3) nada de
> elogio genérico: só rubrica numérica + citações literais.

## Restrições

- Escrita apenas em `second-brain/05. Reports/`. Nunca tocar no banco de
  traduções, no plano, nem em `02. Areas/` — o registro do bloco E é do
  usuário.
- Nunca editar/melhorar a camada 3 do drill, nunca responder as perguntas
  do executivo pelo usuário, nunca redigir "a resposta ideal" — no máximo
  apontar na review onde a resposta violou a rubrica.
- Idempotente por dia: repetir o comando sobrescreve/atualiza o relatório
  do dia, sem escolher um segundo drill.
