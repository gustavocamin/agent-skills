# Aprendizados consolidados

Lições do curso-lab-agent, de 25/09 a 08/10/2026: F00 a F34, 330 commits, 34 PRs e dois agentes (Claude Code e Codex). Cada item traz a regra, o porquê (com a feature de origem, "Fxx") e, depois da seta, onde o kit a aplica.

Use este arquivo para explicar por que uma regra existe, para adaptar um artefato sem perder a lição que ele carrega e para receber aprendizados novos. Lição que vale para qualquer projeto entra aqui e no template que a aplica, juntos (passo final da `replan` de cada projeto).

**O retrato em quatro números:** a revisão independente achou de 3 a 13 problemas em **toda** feature, depois da suíte verde; as features fecharam de 2 a 20 dias antes do prazo; o gargalo foi a validação humana, não o agente; o problema mais caro e repetido foi o iCloud esvaziando o repo.

## Sumário

1. [Constituição, roadmap e replan](#1-constituição-roadmap-e-replan)
2. [Spec e entrevista](#2-spec-e-entrevista)
3. [Requisitos, interfaces e contratos](#3-requisitos-interfaces-e-contratos)
4. [Grupos, dono e paralelismo](#4-grupos-dono-e-paralelismo)
5. [Testes e mutação](#5-testes-e-mutação)
6. [Revisão independente](#6-revisão-independente)
7. [Handoff e integração](#7-handoff-e-integração)
8. [CI e qualidade](#8-ci-e-qualidade)
9. [Evidência e registro](#9-evidência-e-registro)
10. [Documentos vivos](#10-documentos-vivos)
11. [Ambiente local](#11-ambiente-local)
12. [Segredos e permissões](#12-segredos-e-permissões)
13. [Dois agentes](#13-dois-agentes-claude-code--codex)
14. [Deploy e publicação](#14-deploy-e-publicação)
15. [Prazos, escopo e o humano como gargalo](#15-prazos-escopo-e-o-humano-como-gargalo)
16. [Agente de IA no produto](#16-agente-de-ia-no-produto)
17. [Design e interface](#17-design-e-interface)
18. [Anti-padrões e o antídoto de cada um](#18-anti-padrões-e-o-antídoto-de-cada-um)

## 1. Constituição, roadmap e replan

- **A constituição é a fonte da verdade; o `start_here.md` só resume.** Quando os dois divergiram, a constituição venceu e o resumo foi corrigido. → `AGENTS.md`, `start_here.md`.
- **Feche as decisões de arquitetura antes da F01.** Delta virou Lakebase e a aba no Docs virou app em um ou dois dias, e o código da primeira feature (score no JSON) virou dívida até a F05 (F01). → `constitution-interview`, "Decisões em aberto" no roadmap.
- **Uma feature cabe numa branch e num PR.** A F03 original era grande demais e foi dividida em "mockada" (F03) e "execução real" (F04). → roadmap.
- **Pendência sempre vira "Pronto quando" de uma feature nomeada.** A trava do seed mandada "para a F02" sumiu da F02; "sem feature definida" ficou sem dono (F01). Desde a F02, toda pendência ganhou destino. → roadmap, `replan`.
- **Depois de cada feature, um replan transforma lição em regra datada, com o porquê.** Revisão obrigatória, mutação, dono por grupo, handoff conferido e o conferidor no CI nasceram assim. → `replan`, Decisões.
- **Decisões numa entrada datada cada, a mais nova em cima.** No curso-lab, a ordem ficou misturada (crescente e decrescente no mesmo arquivo) e o "uma linha por decisão" se perdeu. → `test_processo.py` confere data e ordem.
- **Regra do marco corrente.** Com uma prova marcada, feature que não servia a ela esperava; features de processo ficavam fora da regra, e cada exceção foi decidida num replan e registrada. → roadmap.
- **Regra que precisa valer adiante vai para o `AGENTS.md` ou para a constituição.** "Corrigir o M4 só por um run novo, nunca à mão" estava só na spec da F32, e a F33 alterou o M4 à mão. → `AGENTS.md`.
- **Emenda à constituição vai no mesmo commit da spec que a motivou**, com uma Decisão datada (F02, F24, F29). → `spec-feature`, `replan`.

## 2. Spec e entrevista

- **Entreviste antes de escrever, em rodadas de 3 a 5 perguntas**, cada decisão com opções, trade-off de uma linha e recomendação; não pergunte o que a constituição já responde. → `spec-feature`, `constitution-interview`.
- **Registre o que foi decidido sem pergunta**, seguindo a constituição, para que possa ser contestado (F02, oito itens; F32). → `spec-feature`.
- **O agente pode propor as respostas e o humano confirmar, desde que fique escrito.** Na F30 a F32, 34 decisões foram confirmadas sem correção. → "Perguntas respondidas" no template.
- **Resposta de entrevista envelhece.** Quando a realidade muda no meio da feature, a mudança entra datada, sem reescrever a resposta original (F01). → "P (data)" no template.
- **Detalhe decidido na implementação volta à spec no próprio grupo** ("Decidido na implementação: …", F03, F26, F29), para "nada no código fora da spec" continuar verdade. Código auxiliar criado no caminho também entra no plano (F01). → template do plano, `implementar-grupo`.
- **Mapeie, com data, o que existe hoje** nos pontos que a feature toca, inclusive a infraestrutura de teste: "nada muda" fica conferível (F28, F31, F32). → template do plano, `spec-feature`.
- **Spike antes de escolher tecnologia**, curto, sem código de produção, com a entrada real e um registro comparativo. Os achados mudaram requisitos: o modelo omitia rótulos com objeto livre, o export real trazia tabelas HTML de 1 MB, o limite real do serviço era 15 MB (F02, F24, F25). → `tech_stack`, `spec-feature`.
- **Fatia piloto ponta a ponta antes de escalar** (código, deploy, execução real, aceite), sem prometer o todo. A lição portátil L4.5 (F33) virou o formato das 38 seguintes (F35). → `spec-feature`.
- **Material feito fora do fluxo entra por um Grupo 0 que importa sem mudar nada**; as correções vêm em grupos seguintes, com diffs separados (F20). → `SKILL.md`, adoção.
- **Uma spec por feature, conferindo antes se ela já existe.** Três specs escritas em paralelo por subagentes numa branch só geraram uma duplicata da F30, vista só depois do merge. → `spec-feature`.
- **Quantifique o problema de interface na spec e meça de novo no fim.** A página do módulo tinha "cerca de 124 telas"; depois, a aba mais longa ficou com um quinto (F03).
- **Ensaie a mudança em massa antes da spec**, sem commit, para medir o tamanho e provar que é segura (F30: 49 arquivos, desfeito).

## 3. Requisitos, interfaces e contratos

- **Interfaces trazem o corpo de cada pedido e de cada resposta**, com campos, tipos e códigos de erro. O contrato da F31 tipou só a resposta: a tela mandava `given` e o servidor exigia `answer`, e todo POST real daria 400. Nas F24, F25 e F26, os códigos de erro só entraram pela revisão. → template de requisitos, "Contrato" no `AGENTS.md`.
- **Entrada que vira sintaxe precisa ser validada.** No kit, um nome com `:` ou aspas quebrava o YAML das skills e as strings das regras do Codex, sem erro nenhum: o gerador passou a recusar a entrada. → `criar_projeto.py`.
- **Contrato se prova com teste do consumidor contra o validador do produtor.** O teste escrito por quem escreveu o código repete o mesmo engano (F31); um contrato entre TypeScript e Python ficou sem teste e quebraria em silêncio (F26). → `AGENTS.md`, `tech_stack`.
- **O mesmo dado com dois nomes é onde o paralelo erra.** `answer` no pedido e `given` na resposta e na tabela (F31). Nomeie uma vez e repita.
- **O contrato congela a assinatura e libera o comportamento**; parâmetro novo só entra como opcional, e quem usa testa com a função real e fixture própria (F28).
- **CLI especificada por inteiro** (formas de chamada, saída, códigos 0/1/2, função importável, regra de leitura) permitiu delegar o grupo ao outro agente e achar bugs precisos na revisão (F26, F34). → template de requisitos.
- **Processo longo tem a tabela "como terminou → status"**, inclusive a falha transitória que não grava nada e é refeita depois (F02).
- **Requisito diz o caso vazio e o de inconsistência que já existe** ("banco novo, progresso vazio"; "referência já órfã não bloqueia", F26). → template de requisitos.
- **Ids publicados são contrato estável.** O progresso referenciava o id sem chave estrangeira: a remoção passou a ser recusada, com liberação explícita e registrada (F26). → bloco Databricks do `tech_stack`.
- **Formato novo continua compatível**: campo opcional com default igual ao comportamento antigo e um teste de que o formato antigo segue válido (F24, F25).
- **Valor vazio com sentido especial é recusado na entrada.** `timed_forms: []` era lido como "todas medem" (F28).
- **Fato sobre produto externo leva URL e data**, e a reconferência fica agendada antes do prazo (F20, F22). Versão de dependência se confirma na doc antes de citar: "Spark 3.5" virou 4.1 (F21). → "Docs atuais" no `AGENTS.md`.
- **Dado desconhecido não se inventa.** A data da prova DEA ficou nula, com teste e gatilho de reconferência (F22). → `SKILL.md`, passo de semear.

## 4. Grupos, dono e paralelismo

- **Grupo de contrato primeiro, paralelos depois, com `Toca` disjunto.** Deu zero conflito de código em todos os merges de grupo (F28, F29, F31). O commit do contrato avisa que os paralelos podem começar, depois do push da branch da feature. → template do plano.
- **"Arquivos compartilhados" com dono**: depois do grupo do contrato, só quem integra mexe neles (F28). → template do plano.
- **`Toca` explícito torna o paralelismo conferível.** "Quando pode rodar em paralelo" não era conferível (achado da F29); `Toca` virou obrigatório e testado. O `Toca` não inclui os arquivos de quem integra (F33 incluiu `start_here.md`). → `test_processo.py`, `spec-feature`.
- **⚠ só no grupo ou no passo que toca o ambiente real** ("⚠ no deploy", F03, F26): o código do grupo pode ir em paralelo. → template do plano.
- **Grupos ⚠ em sequência, também entre features** que dividem publicação e deploy (F31 e F32). → `AGENTS.md`.
- **Antes de um ⚠ caro, um grupo de preparação sem código** confere base, versões, suíte e uma fumaça; execução e aprovação de algo irreversível são dois ⚠, com o diff mostrado entre eles (F32). → `spec-feature`.
- **Ordem de valor com corte mínimo por grupo**, para o prazo apertado (F02, F24, F28, F31). → template do plano.
- **Configurar a fronteira de permissões de um agente já é um grupo ⚠**, e os grupos que dependem da ferramenta só começam depois dele (F29).
- **Grupo só de leitura corre em paralelo com qualquer outro** (F29).
- **Subagentes em worktrees para grupos sem ⚠; os ⚠ ficam com o agente principal**, em sequência (F26, F27). Um subagente travou num `tsc` e o principal assumiu. → `CLAUDE.md`.
- **Trocar o dono é correção da spec, datada** (F28, F33). → `AGENTS.md`.
- **Grupo cuja saída é dado transcrito pelo agente termina numa parada para revisão humana**, com tamanho de amostra definido, mesmo sem ⚠ (F01).

## 5. Testes e mutação

- **Mutação em camadas: autor, quem integra e revisor.** Cada camada achou o que a anterior deixou: na F29, as 9 mutações do autor passaram e o teste das regras era fraco; a mutação de quem integra achou o furo, e isso virou regra. Na F31, quem integra achou 2 testes fracos e o revisor 5. → `AGENTS.md`, tabela de mutações no template.
- **Mutação que sobrevive pode ser mal escolhida, cair numa coincidência da fixture ou ser equivalente**: repita com uma limpa antes de chamar o teste de fraco (F31, F34). → template de validação.
- **Fixture em que o caminho errado dá a mesma resposta esconde bug** (F28, F31). → `implementar-grupo`.
- **Teste que só confere "recusou" passa com uma implementação constante**; confira a lista exata de problemas (F34).
- **Teste confere a decisão, não a presença de um texto.** O teste das regras do Codex procurava strings e foi reescrito para avaliar cada comando contra uma tabela, conferida também pelo `codex execpolicy` (F29). → `EXPECTED_DECISIONS` no `test_processo.py`.
- **Teste de configuração confere os valores críticos**, não só a chave: `"never"` e `":full-access"` passavam nos 30 testes (F29). → teste da config do Codex.
- **Bug: primeiro o teste que o reproduz, visto falhando no código antigo** (F27). → `implementar-grupo`.
- **Artefatos reais viram régua.** Os gabaritos reais foram a régua do "passa" e fixtures adversárias a do "falha" (F03); os 11 handoffs reais do histórico viraram casos com a lista exata de problemas (F34).
- **Mock com os objetos reais do SDK e um smoke real, uma vez.** O smoke achou 4 divergências que viraram fixture (F03); o run real de 1 h achou uma exceção fora da lista de retry (F02). → `implementar-grupo`.
- **Teste contra sistema real é marcado, fica fora do CI, pula sem a variável de ambiente e limpa tudo no `finally`** (F03). → marcador `integration` no `pyproject.toml`.
- **Teste real num ambiente descartável.** A F26 usou um branch do banco com validade, que sumiu sozinho. Nas F24 e F25, as análises de teste ficaram no banco real e uma delas virou a "primeira tentativa" medida (apagadas com backup na F27). → `tech_stack`.
- **Testes sem rede**: regra de negócio em funções puras compartilhadas, fakes ricos (store que trava, LLM que desobedece, repo git com origin local, banco em memória) (F23, F26). → `tech_stack`.
- **Banco falso que responde pelo texto do SQL não exercita a semântica** (`ON CONFLICT`, `DELETE`); só o teste estático do SQL pegou essas mutações (F31).
- **Teste que lê estado vivo do repo quebra quando o produto muda esse estado** (6 testes presos ao `NEXT MODULE`, F02). Fixe o estado no teste.
- **Tela nova ou alterada exige teste de componente.** R7–R10 e R13 da F25 ficaram só com a conferência no navegador. → `tech_stack`.
- **Olhar a tela ainda acha o que os testes não acham** (F02, F03, F28): o item humano leva o caso concreto. jsdom não faz layout, então os 375 px ficam na conferência manual. → template de validação.
- **Medir antes de corrigir teste instável.** A causa era o excesso de workers, não o limite suspeito; os limites ficaram em cerca de 2× o pior caso medido, com a mesma configuração no local e no CI (F34). → `tech_stack`.
- **Suítes rodando juntas na mesma máquina dão timeouts falsos** (F30, F33).
- **Todo caminho que o texto manda o usuário rodar é executado no teste**, e número de texto gerado se confere contra a fonte (F32).

## 6. Revisão independente

- **Achou problema em toda feature, depois da suíte verde**: F01 com 5 correções; F02 com 10 bugs, depois de dois runs reais verdes; F03 com 13 furos; F23 a F27 com 2 a 13; F28 com 3; F29 com 6, 1 crítico; F30 com 8; F31 com 8; F32 com 7; F34 com 6. Virou obrigatória em degraus: com ⚠ (pós-F03), em toda feature (pós-F26), com mutação (pós-F27) e pelo outro agente (F29). → `validate-feature`.
- **Sessão nova, sem histórico, só com constituição, spec e diff**; com dois agentes, quem revisa é o que não integra. → prompt da `validate-feature`.
- **Peça bugs com cenário concreto e reproduza cada achado antes de corrigir** (F03). → prompt.
- **Dê ao revisor os pontos de maior risco** (F31) e peça também o que ficou provado sem bug (F26). → template de validação, prompt.
- **Faça a triagem**: corrija o que código natural abriria e registre o adversarial como limite conhecido, para um controle mais forte (F03). → "Limites conhecidos".
- **A revisão também acha erro no registro de quem integra e documento velho** (F27, F32, F33). → item 4 do prompt.
- **Leitura divergente do revisor é ambiguidade**: o comportamento fica, o requisito é reescrito e entra o teste que mata a mutação (F28).
- **A revisão precisa de sessão própria.** Chamar o CLI do outro agente de dentro da sessão terminou em erro, sem relatório (F33). → `validate-feature`.
- **Uma revisão vale só para a versão revisada** (F21).

## 7. Handoff e integração

- **O handoff vai no último commit do grupo, com sete campos**: Feito, Contrato, Testes, Mutações, Evidência, CI e Desvios da spec. → `AGENTS.md`, `check_handoff.py`.
- **"Desvios: nenhum" só depois de reler Interfaces e Requisitos, item por item.** O handoff da F31 dizia "nenhum" e havia dois desvios, um deles o POST errado. → `implementar-grupo`.
- **O conferidor do CI checa a forma, não o conteúdo**; o conteúdo é de quem integra, na coluna "Handoff conferido" (F34). → `check_handoff.py`, template de validação.
- **Handoff ruim se corrige sem push forçado**: vale o último handoff do grupo no intervalo, com o grupo lido de qualquer ponto do assunto (F34). → `check_handoff.py`.
- **Quem integra confere cada handoff que não fez**: refaz os desvios, confere o contrato e faz mutação própria. → `AGENTS.md`.
- **Merge `--no-ff` só com o CI do grupo verde, suíte inteira depois e transcrição no "Registro dos grupos"** (F28, F29). → `AGENTS.md`.
- **Arquivos de estado têm um só escritor**: `start_here.md`, constituição, "Registro dos grupos" e "Resultado" ficam com quem integra (F29). Os donos do Codex não marcaram os próprios checkboxes e quem integra os marcou (F31). → `AGENTS.md`.
- **Feature feita por um agente só perde as salvaguardas cruzadas.** A F33 não teve revisão nem mutação do outro agente, e quem a fez abriu 4 PRs e escreveu o roadmap. → "Integra" só por decisão do dono humano.
- **Branch de partida fora da `main` é desvio registrado** (F31 nasceu da branch de outra feature).

## 8. CI e qualidade

- **O CI decide**: nada entra na branch da feature nem na `main` com o CI vermelho. → `AGENTS.md`.
- **O CI roda os mesmos checks do gate de deploy.** Um lint que só o deploy rodava barrou o deploy com o CI verde (F23). → `tech_stack`.
- **Regra que falhou na prática vira gate de CI, provado com vermelho → verde numa branch descartável** (`--prova`), com os runs registrados e a branch apagada (F30, F34). O handoff do próprio grupo passou pelo gate novo. → `replan`, convenção de branches.
- **O passo barato e rápido vem logo depois da instalação** (F30). → ordem do `ci.yml`.
- **Mudança em massa entra isolada, antes de grupos em paralelo.** O formatador nunca rodado na base gerava diff de ruído a cada grupo (F28); a formatação virou a F30, provada refazendo o commit numa cópia e comparando byte a byte. → `tech_stack`.
- **Sem hook de pre-commit**: seria dependência nova e rodaria fora do sandbox do Codex. A cobrança fica no CI e no script local (`--file`) (F30, F34).
- **Decida o escopo do lint para artefatos gerados antes do primeiro run** (o `ruff` leu células `%sql` de notebook como Python: 361 erros, F02).
- **Meça quanto um passo novo custa no CI** (F34: menos de 1 s) e prove uma mudança não funcional pela mesma contagem de testes (F29, F30).

## 9. Evidência e registro

- **Todo resultado diz se foi observado por quem escreve, relatado pelo humano ou repassado de outro agente, com o commit ou o hash** (F33; regra de 08/10). Contagem, data e PR não identificam o que foi testado (F01). → `AGENTS.md`.
- **Prova fora do repo se perde.** `/tmp`, scratchpad e prints de biblioteca externa citados em handoffs (F28, F33, F34) levaram à regra "nunca só numa pasta temporária". → `AGENTS.md`.
- **Aceite manual vale só para o hash testado**: mudar o artefato reabre o item, e a confirmação antiga não se reaproveita (F33). Autorização também é por ação e por versão. → `validate-feature`.
- **Teste local não é prova da plataforma**, e simulação declara o próprio limite: o bundle que convertia `.ipynb` só apareceu depois do deploy (F33). → `implementar-grupo`.
- **Saída real colada no `validation.md`**, com tabela de passo, resultado e tempo, e as contagens do ambiente real antes e depois (F26).
- **Prova negativa por diff restrito**: "nenhum código mudou" é `git diff main...HEAD -- <pastas de código>` vazio (F32).
- **Quando o código muda depois do teste real, diga por que o resultado ainda vale** (F03).
- **Custo zero por condição do plano não é custo medido** (F33).
- **Identificador pessoal em arquivo versionado não sai do histórico.** O email do perfil ficou nos registros de quatro features até a revisão da F27 achar. → invariante no `AGENTS.md`.

## 10. Documentos vivos

- **O `start_here.md` resume e aponta, com teto.** O do curso-lab cresceu de 135 para 351 linhas em 12 dias, com 44% de registro diário, o fechamento da F34 em seis lugares e "Próximo" contraditório. → `start_here.md` enxuto, teto de 150 linhas testado.
- **A atualização do `start_here.md` vai no PR em curso**, não num PR próprio (houve dois só para ele). → `AGENTS.md`.
- **Números copiados envelhecem**: "49 arquivos" eram 47 (F30); "928 testes" eram 943 (F34). Confira antes de copiar. → comentário no `start_here.md`.
- **Spec antiga que outra feature mudou ganha emenda "desde a Fxx"** e continua verdadeira (F20, F23, F24, F28). → `AGENTS.md`.
- **Spec fora do template é difícil de conferir e de retomar.** A F33 saiu sem Integra, Invariantes e Perguntas, e o `validation.md` dela virou um diário de 18 seções. → `test_processo.py` confere as seções.
- **As seções que se repetiram nas specs entraram no template**: mapa requisito → teste, mutações por camada, revisão independente, limites conhecidos, "Para o replan", "Decidido na implementação", "O que existe hoje", "Arquivos compartilhados" e "Ordem de valor". → templates de feature.
- **Template somente leitura atrasou as regras novas** (F29): quando uma regra muda, o template muda no mesmo replan (`chmod u+w` só para isso).

## 11. Ambiente local

- **Repo fora do iCloud.** Foi o problema mais caro e mais repetido: venv com arquivos vazios (F22); 869 arquivos do `.git` e 46 mil do `node_modules` (F26); 62 mil do `node_modules`, 83 de `app/client` e cópias `* 2.md` bloqueando a publicação (F27); packfiles corrompidos (F33). A marca "Manter baixado" não segurou com o disco cheio; a saída foi a pasta `.nosync`. → pré-voo do `SKILL.md`, aviso do gerador, `tech_stack`.
- **Disco é recurso de processo.** Uma worktree com o app custa cerca de 1 GB (venv de 158 MB e `node_modules` de 836 MB); o disco chegou a 1,7 GB e travou o paralelo. Referência: 15 GB para grupos locais em paralelo, 5 GB no mínimo para abrir uma worktree, e grupos sem ⚠ no cloud quando falta espaço (F28, F29, F34). → aviso do gerador, `setup-worktree.sh`, `tech_stack`.
- **Cada worktree tem a própria venv**: a instalação editável de outra venv importava o código do checkout principal (F29). → `setup-worktree.sh`.
- **O setup de worktree é idempotente**, não faz nada no checkout principal e não escreve através de link (F29). → `setup-worktree.sh`.
- **Carga da máquina pesa nas medições**: um processo do sistema a 99% de CPU distorceu os tempos (F34). Registre carga e hardware com a medição.
- **Confira a ferramenta antes de planejar**: o CLI do Codex instalado estava quebrado (F29).
- **Configuração local que suja a árvore vai para o `.git/info/exclude`** (F25, F27).

## 12. Segredos e permissões

- **Nenhum segredo versionado, com varredura automática** de tokens comuns (F02, F20, F29). → `test_processo.py`.
- **Segredo local em `~/.config/<projeto>/`, com `chmod 600`, fora do repo e do iCloud** (F02). → `tech_stack`.
- **Recuse rodar quando uma variável de ambiente venceria a credencial pretendida** (uma chave de API venceria o perfil OAuth, F02).
- **Erro de SDK que imprime o host passa por um filtro antes da tela**, com teste (F26). → `tech_stack`.
- **Regra `allow` roda fora do sandbox.** Com o `git add` liberado, um `-f` levaria o `.env` ao commit apesar da leitura negada (achado crítico da F29): `git add` pede aprovação e `-f` é proibido. A revisão independente deste kit achou o mesmo furo no `git push` liberado, herdado do curso-lab: `--receive-pack=<comando>` executa o comando na máquina, e `--all`, `+branch` ou `x:main` chegam à `main` ou forçam o push. No kit, todo push pede aprovação. → regras do Codex, `.claude/settings.json`.
- **Um ⚠ que fica só no texto não trava nada.** No teste de ponta a ponta do kit, os ⚠ ditos na entrevista (chave de LLM, banco) não chegavam a nenhuma regra de comando: o grupo que cria um comando que toca ambiente real o põe nas regras dos agentes, e o `start_here.md` nasce com essa pendência. → `AGENTS.md`, `start_here.md`.
- **Regra por prefixo deixa passar casos** (flag depois do destino, `git -C`, refspec `x:main`): eles ficam listados como limite aceito, com a camada seguinte cobrindo (F29). → comentário das regras, `CLAUDE.md`.
- **O GitHub Free não protege a `main` de um repo privado**: a regra fica escrita, e quem integra confere a `main` antes de cada merge (F29, F34). → `AGENTS.md`.
- **O perfil de permissões do Codex some quando a conversa força um modo de sandbox** (F29). → seção Codex do `AGENTS.md`.
- **Credencial dada a agente remoto é dedicada, com escopo mínimo, validade curta e revogação datada**; risco aceito fica registrado com validade e com a feature que o revisita (F02, replan pós-F34). → `tech_stack`.
- **Destrutivo com rede de segurança**: backup local antes, apagar só o que tem marcador de posse, falhar fechado diante do desconhecido (F27, F33). Quando o classificador do agente barra, o humano roda o comando. → "Operação" no `tech_stack`.
- **Invariante vale no próprio banco**, por grants mínimos, conferidos depois de cada DDL ou deploy (F23). → bloco Databricks.

## 13. Dois agentes (Claude Code + Codex)

- **O `AGENTS.md` é a fonte única; o `CLAUDE.md` o importa na primeira linha** e guarda só o que é do Claude Code (F29). → templates, `test_processo.py`.
- **Skills numa cópia só, com o link `.agents/skills` → `../.claude/skills`** (F29). → gerador.
- **A memória automática de um agente não chega ao outro**: o que vale para os dois vai para o `AGENTS.md` ou para a constituição (F29). → `CLAUDE.md`.
- **Divisão por tipo de trabalho**: contrato e ⚠ com quem integra e tem credencial; grupos sem ⚠ no Codex cloud, em paralelo, que não gasta disco (F28). → `spec-feature`.
- **Ensaie o protocolo antes de confiar**: uma fumaça de leitura com prompt fixo e critérios de aprovação, e um grupo real integrado pelo outro agente. A primeira fumaça falhou porque a aprovação dos comandos ⚠ estava fora da lista do protocolo (F29). → `fluxo.md`, ativação do Codex.
- **Confira a branch base de cada conversa do agente.** As 5 primeiras worktrees do app do Codex saíram da `main` (sem `AGENTS.md`, setup com 127). → sinais de base errada no `AGENTS.md`.
- **O agente nunca devolve trabalho para o checkout local de quem integra** ("Hand off" para "Local", F29). → `AGENTS.md`.
- **O cloud parte do repositório remoto**: quem integra faz push da branch da feature antes de abrir um grupo lá (F29). → `AGENTS.md`.
- **O Codex cloud agiu no GitHub com a identidade do dono humano** (push e leitura do CI, F34), ao contrário do que a regra dizia: a regra foi atualizada, e quem integra confere a `main` e a branch da feature antes de cada merge. → `AGENTS.md`.
- **`Integra: Codex` só por decisão do dono humano** (F33). → `AGENTS.md`.
- **Sessão de quem integra sem credencial nem o outro agente**: revisão por subagente, com o motivo registrado, e os ⚠ com o humano, guiados por um roteiro com pré-checagens e a saída esperada de cada comando (F30, F31).
- **Os dois agentes formatam igual** porque a versão do formatador vem do lockfile e o fechamento de grupo roda o formatador (F28, F30).
- **Commits em português e testes com nome de domínio.** A F33 teve 8 de 10 commits em inglês e testes `test_f33_*` (F33). → `AGENTS.md`.
- **Configuração do agente se confere com os verificadores offline da própria ferramenta** (`codex execpolicy check`) (F29). → `test_processo.py`.

## 14. Deploy e publicação

- **Conteúdo como dado publicado**: o git é a fonte da verdade, e uma publicação idempotente projeta o conteúdo num banco, grava o commit e responde "nada mudou" na segunda execução; mudar conteúdo não pede redeploy (F23, F26). → bloco Databricks.
- **Um `--check` só de leitura depois de cada merge diz se o banco está atrás da `main`**; ele ficou pendente várias vezes (F26, F28, F31, F32). → `validate-feature`, passo 10.
- **Publicação e deploy saem da branch no último grupo ⚠** (F28, F31), longe do evento crítico de uso (F28).
- **DDL idempotente aplicada pelo app ao subir** mantém o grupo de contrato sem ⚠: o banco só muda no deploy (F31).
- **SPA com chunks com hash quebra nas abas abertas antes do redeploy**: trate a falha de carga com uma recarga, com trava (F02).
- **Plataforma que desliga sozinha** (o app para em 24 h) pede um `start` antes do deploy ou da conferência (F26). → bloco Databricks.
- **A plataforma pode reescrever o que você pede**: leia o valor efetivo de volta pela API (F02).
- **O artefato implantado se confere por GET autenticado** (status, tipo, bytes, SHA-256): um 200 pode ser o fallback do SPA (F33). → bloco Databricks.

## 15. Prazos, escopo e o humano como gargalo

- **As features fecharam de 2 a 20 dias antes do prazo**, e cada folga exigiu um replan (F02, F03, F23 a F31).
- **O gargalo foi a validação humana, as credenciais e o uso real.** "Um dia real de estudo" levou 9 dias (F23); F30, F31 e F32 ficaram com itens humanos abertos; a F35 decidiu fechar sem esperar o teste manual, com o resultado entrando depois. → seção "Aguardando" no `start_here.md`.
- **Fechar com item aberto é anti-padrão.** A F31 fechou com 3 itens humanos abertos e a F32 com 13 `[ ]`. Item adiado sai do checklist só por decisão registrada e vira pendência com dono e data. → `validate-feature`, passo 8.
- **Não provoque um cenário caro só para testá-lo**: se ele não acontecer, vira herança numa tabela, com a feature que o confere (F32).
- **Ampliação de escopo durante a spec fica registrada com o porquê** (F03), e pedido novo depois do fechamento vai para a próxima feature, sem reabrir (F27).
- **O que o classificador do agente ou um proxy recusa** (apagar branch remota, `DELETE` de dados) sobra para o humano; liste no `start_here.md` (F27, F30, F31).

## 16. Agente de IA no produto

Vale quando o projeto constrói um agente (módulo `agente` do gerador, que leva estas regras ao `tech_stack`).

- **Defesa em camadas**: prompt → trava na tool → guarda determinística depois do run, fora do alcance do agente → credencial mínima → permissão na plataforma. Com shell no sandbox, a trava na tool não basta (F02). Cada camada heurística tem limites conhecidos e um corpus real contra falso positivo (logs de 489 e 580 eventos, F02); a lista de bloqueio furada 13 vezes virou lista do que é permitido (F03).
- **Sonda única, versionada e só de leitura** antes da feature que libera o acesso externo; qualquer outro uso reprova o run (F02). Capacidade nova entra bloqueada pela guarda até a feature que a libera (F03).
- **Avaliador LLM aceita o relato do agente mesmo quando contradiz a saída do comando** (spike da F02): critério de rubrica se confere no artefato. Duas iterações de rubrica são o normal (F32).
- **A checagem que o agente roda antes do commit é o mesmo código que a guarda reaproveita** (F02).
- **Tool que commita sozinha** commita só o próprio caminho, recusa arquivo sujo, faz rollback se o commit falhar e nunca faz commit vazio (F01). Invariante do agente vira trava no código da tool, testada nos dois sentidos (F01).
- **Lição de cada revisão humana vira versão nova do agente**, registrada; comportamento bom que o agente teve sozinho vai para o prompt (F02). Fora da feature que valida uma versão nova, não se mexe no prompt nem no manifest (F32).
- **O agente nunca edita as próprias instruções, e artefato aprovado é imutável** (F01, F02).
- **Custo vem do contexto relido a cada passo, não da escrita** (30 e 50 milhões de tokens de cache no M2 e no M3; 32 objetivos custaram só 14% a mais que 19). Limite a lista de leitura no prompt (F02, F32).
- **Teto por sessão é hipótese**: foi de US$ 50 a 100 em dois dias; uma sessão ficou 10,7 h parada no teto sem virar `budget_reached`. Vigie, permita subir o teto sem reiniciar e limite os runs completos por artefato (F02).
- **Spike de runtime com teto baixo**, depois de conferir créditos e pré-requisitos da conta (F02). Processo longo sobrevive à queda do cliente e retoma sem perder evento (F02).
- **Aprovação humana presa ao commit que a guarda conferiu**, e o passo depois da ação irreversível é idempotente e repetível (F02).
- **Recusa do classificador de segurança do modelo é erro de sessão previsto** (F02, F32). Autonomia maior (merge sem humano) só depois de evals.

## 17. Design e interface

- **Mockups em HTML estático, fora do app** (desktop e 375 px, claro e escuro), aprovados antes do código, em rodadas registradas (F25).
- **Cada elemento do mockup mapeado para um componente da biblioteca**, ou para o motivo de não haver; desvios registrados (F25).
- **Os mockups trouxeram requisitos que a entrevista não tinha** (F25): registre-os como perguntas daquela fase.
- **Acessibilidade medida com número** (contraste ≥ 4,5:1 por token e por tema, F25).
- **"Casca completa"**: a área de uma feature futura aparece como "aguardando Fxx", em vez de sumir (F23).

## 18. Anti-padrões e o antídoto de cada um

| Anti-padrão | Onde aconteceu | Antídoto no kit |
|---|---|---|
| Repo em pasta sincronizada | F22, F26, F27, F33 | `.nosync`, aviso do gerador |
| Contrato que tipa só a resposta | F31 | Interfaces com o corpo do pedido; teste contra o validador |
| Handoff autodeclarado sem conferência | F28, F31, F33 | conferidor no CI e "Handoff conferido" |
| Teste fraco que passa nas mutações do autor | F28, F29, F31 | mutação de quem integra e do revisor |
| Spec divergindo do código, vista só na revisão | F01, F02, F03 | revisão independente obrigatória |
| Caminho de erro sem teste | F01, F02, F03 | requisitos com caso vazio e de erro; revisor pede cenário |
| Mock divergente do real | F02, F03 | objetos reais do SDK e smoke |
| Dado de teste deixado em produção | F24, F25 | ambiente descartável |
| Feature fechada com itens abertos | F31, F32 | regra de fechamento da `validate-feature` |
| Evidência só fora do repo | F28, F33, F34 | regra de evidência |
| Agente na base ou branch errada | F29, F30, F31 | sinais de base errada; conferir a branch |
| Pendência sem dono | F01 | "Pronto quando" de feature nomeada |
| Documento de navegação que só cresce | `start_here`, Decisões | teto e ordem testados |
| Um agente fazendo tudo fora do protocolo | F33 | `Integra` por decisão; revisão do outro agente |
| Regra sem trava que diverge da realidade | F29, F34 | auditoria no `replan` |
| Teste de interface instável contornado | F02 a F34 | medir e corrigir a causa |
| Teto de custo fixado antes de medir | F02 | teto como hipótese, vigiado |
| Heurística como trava principal | F02, F03 | defesa em camadas e lista do permitido |
