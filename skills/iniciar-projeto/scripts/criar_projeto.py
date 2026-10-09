#!/usr/bin/env python3
"""Gera um projeto no fluxo spec-first a partir dos templates da skill iniciar-projeto.

    python3 criar_projeto.py --destino <pasta> --respostas <respostas.json>
        [--simular] [--adotar] [--sem-git]

Só usa a biblioteca padrão (Python 3.9+). Renderiza tudo na memória antes de escrever: um
template com chave desconhecida ou bloco sem fechamento para o script sem criar nada.

Nunca sobrescreve. Sem --adotar, o destino precisa estar vazio (ou não existir). Com --adotar,
cria só o que falta e lista o que pulou, para quem chamou integrar à mão.

Templates (em ../assets/<camada>/, com sufixo .tmpl):
- camadas: "base" sempre, mais uma por módulo ligado ("codex", "databricks", "agente");
- "dot_" no começo de um nome de pasta ou arquivo vira "." (dot_claude → .claude);
- {{CHAVE}} vira o valor da chave; {{#se modulo}}…{{/se}} (ou {{#se !modulo}}) mantém o trecho só
  com o módulo ligado (ou desligado), em linha própria (bloco) ou dentro da linha;
- ${{ … }} (GitHub Actions) não é marcador.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ASSETS = SKILL / "assets"
MODULOS = ("codex", "databricks", "agente")
SUFIXO = ".tmpl"
SOMENTE_LEITURA = "specs/features/_template/"
IGNORADOS = {".DS_Store"}
# Pastas que não contam como conteúdo de uma pasta "vazia".
NEUTROS = {".git", ".DS_Store"}

CHAVE = re.compile(r"(?<!\$)\{\{([A-Z][A-Z0-9_]*)\}\}")
ABRE = re.compile(r"^[ \t]*\{\{#se (!?)([a-z]+)\}\}[ \t]*$")
FECHA = re.compile(r"^[ \t]*\{\{/se\}\}[ \t]*$")
EM_LINHA = re.compile(r"\{\{#se (!?)([a-z]+)\}\}(.*?)\{\{/se\}\}")
# Só o que tem cara de marcador do template: chave em maiúsculas ou bloco "se". Chaves duplas de
# f-string do Python ("{{commit}}") e expressões do GitHub Actions ("${{ … }}") passam.
SOBRA = re.compile(r"(?<!\$)\{\{(?:[A-Z][A-Z0-9_]*|[#/]se\b[^{}\n]*)\}\}")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NOME = re.compile(r"[^\W\d_][\w .'-]*")


class ErroTemplate(Exception):
    pass


def slugificar(texto: str) -> str:
    ascii_ = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_.lower()).strip("-")


def juntar(itens: list[str]) -> str:
    itens = [item.strip() for item in itens if item.strip()]
    if len(itens) <= 1:
        return "".join(itens)
    return ", ".join(itens[:-1]) + " ou " + itens[-1]


def lista(itens: list[str], vazio: str) -> str:
    itens = [item.strip() for item in itens if item.strip()]
    return "\n".join(f"- {item}" for item in itens) if itens else vazio


def _texto(respostas: dict, chave: str, obrigatorio: bool = False) -> str:
    valor = respostas.get(chave)
    if valor is None or valor == "":
        if obrigatorio:
            raise ErroTemplate(f"respostas sem {chave}")
        return ""
    if not isinstance(valor, str):
        raise ErroTemplate(f"{chave} precisa ser texto, veio {type(valor).__name__}")
    if "\n" in valor:
        raise ErroTemplate(f"{chave} não pode ter quebra de linha")
    return valor.strip()


def _lista(respostas: dict, chave: str) -> list[str]:
    valor = respostas.get(chave) or []
    if not isinstance(valor, list) or not all(isinstance(item, str) for item in valor):
        raise ErroTemplate(f"{chave} precisa ser uma lista de textos")
    if any("\n" in item for item in valor):
        raise ErroTemplate(f"{chave}: um item não pode ter quebra de linha")
    return [item.strip() for item in valor if item.strip()]


def contexto(respostas: dict) -> tuple[dict[str, str], set[str]]:
    if not isinstance(respostas, dict):
        raise ErroTemplate("as respostas precisam ser um objeto JSON")
    projeto = _texto(respostas, "projeto", obrigatorio=True)
    dono = _texto(respostas, "dono", obrigatorio=True)
    # O nome do dono entra no frontmatter YAML das skills e nas strings das regras do Codex.
    if not NOME.fullmatch(dono):
        raise ErroTemplate(
            f"dono inválido: {dono!r} (use letras, números, espaço, ponto, apóstrofo e hífen, "
            "começando por letra)"
        )
    slug = _texto(respostas, "slug") or slugificar(projeto)
    if not SLUG.match(slug):
        raise ErroTemplate(f"slug inválido: {slug!r} (use minúsculas, números e hífens)")
    modulos = set(_lista(respostas, "modulos"))
    desconhecidos = modulos - set(MODULOS)
    if desconhecidos:
        raise ErroTemplate(f"módulo desconhecido: {', '.join(sorted(desconhecidos))}")
    hoje = _texto(respostas, "data") or date.today().isoformat()
    try:
        date.fromisoformat(hoje)
    except ValueError:
        raise ErroTemplate(f"data inválida (use AAAA-MM-DD): {hoje!r}") from None
    python = _texto(respostas, "python") or "3.11"
    # De 3.11 (os testes do processo usam tomllib) até a mais nova que o ruff conhece como alvo.
    if not re.fullmatch(r"3\.1[1-5]", python):
        raise ErroTemplate(f"versão de Python fora de 3.11 a 3.15: {python!r}")
    alerta = _lista(respostas, "alerta")
    if not any("segredo" in item.lower() for item in alerta):
        alerta.insert(0, "segredos")
    if "databricks" in modulos and not any("databricks" in item.lower() for item in alerta):
        alerta.append("escrita no workspace Databricks")
    invariantes = _lista(respostas, "invariantes")
    ano, mes, dia = hoje.split("-")
    ctx = {
        "PROJETO": projeto,
        "SLUG": slug,
        "DONO": dono,
        "DATA": hoje,
        "DATA_BR": f"{dia}/{mes}/{ano}",
        "ALERTA": juntar(alerta),
        "INVARIANTES": lista(
            invariantes, "- [A CONFIRMAR] Invariantes do produto, fechados na F00."
        ),
        "PYTHON": python,
        "PYTHON_ALVO": "py" + python.replace(".", ""),
    }
    return ctx, modulos


def _modulo(nome: str, origem: str) -> str:
    if nome not in MODULOS:
        raise ErroTemplate(f"{origem}: módulo desconhecido em {{{{#se {nome}}}}}")
    return nome


def renderizar(texto: str, ctx: dict[str, str], modulos: set[str], origem: str) -> str:
    saida: list[str] = []
    pilha: list[bool] = []
    for numero, linha in enumerate(texto.splitlines(keepends=True), 1):
        crua = linha.rstrip("\r\n")
        abre = ABRE.match(crua)
        if abre:
            negar, nome = abre.groups()
            pilha.append((_modulo(nome, origem) in modulos) != bool(negar))
            continue
        if FECHA.match(crua):
            if not pilha:
                raise ErroTemplate(f"{origem}:{numero}: {{{{/se}}}} sem abertura")
            pilha.pop()
            continue
        if all(pilha):
            saida.append(linha)
    if pilha:
        raise ErroTemplate(f"{origem}: bloco {{{{#se}}}} sem fechamento")
    texto = "".join(saida)

    def em_linha(match: re.Match) -> str:
        negar, nome, trecho = match.groups()
        return trecho if (_modulo(nome, origem) in modulos) != bool(negar) else ""

    texto = EM_LINHA.sub(em_linha, texto)

    def trocar(match: re.Match) -> str:
        chave = match.group(1)
        if chave not in ctx:
            raise ErroTemplate(f"{origem}: chave desconhecida {{{{{chave}}}}}")
        return ctx[chave]

    texto = CHAVE.sub(trocar, texto)
    sobra = SOBRA.search(texto)
    if sobra:
        raise ErroTemplate(f"{origem}: marcador não resolvido {sobra.group(0)}")
    return texto


def caminho(relativo: str, ctx: dict[str, str]) -> str:
    partes = []
    for parte in relativo.split("/"):
        if parte.startswith("dot_"):
            parte = "." + parte[4:]
        partes.append(parte)
    relativo = "/".join(partes)
    if relativo.endswith(SUFIXO):
        relativo = relativo[: -len(SUFIXO)]

    def trocar(match: re.Match) -> str:
        if match.group(1) not in ctx:
            raise ErroTemplate(f"{relativo}: chave desconhecida no nome do arquivo")
        return ctx[match.group(1)]

    return CHAVE.sub(trocar, relativo)


def planejar(ctx: dict[str, str], modulos: set[str]) -> list[dict]:
    plano: list[dict] = []
    vistos: set[str] = set()
    for camada in ["base", *sorted(modulos)]:
        raiz = ASSETS / camada
        if not raiz.is_dir():
            continue
        for origem in sorted(raiz.rglob("*")):
            if origem.is_dir() or origem.name in IGNORADOS:
                continue
            relativo = origem.relative_to(raiz).as_posix()
            if not relativo.endswith(SUFIXO):
                raise ErroTemplate(f"{camada}/{relativo}: template sem sufixo {SUFIXO}")
            destino = caminho(relativo, ctx)
            if destino in vistos:
                raise ErroTemplate(f"{destino}: aparece em mais de uma camada")
            vistos.add(destino)
            texto = renderizar(
                origem.read_text(encoding="utf-8"), ctx, modulos, f"{camada}/{relativo}"
            )
            modo = 0o755 if os.access(origem, os.X_OK) else 0o644
            if destino.startswith(SOMENTE_LEITURA):
                modo = 0o444
            plano.append({"caminho": destino, "conteudo": texto, "modo": modo})
    if "codex" in modulos:
        # O Codex acha as skills do repo em .agents/skills; o link evita manter duas cópias.
        plano.append({"caminho": ".agents/skills", "link": "../.claude/skills"})
    return plano


def conteudo_relevante(destino: Path) -> list[str]:
    if not destino.exists():
        return []
    return sorted(item.name for item in destino.iterdir() if item.name not in NEUTROS)


def conflitos(destino: Path, plano: list[dict]) -> list[str]:
    """Caminhos que impediriam a escrita no meio: pasta-mãe que é arquivo ou link quebrado."""
    problemas: set[str] = set()
    for item in plano:
        atual = destino
        for parte in Path(item["caminho"]).parts[:-1]:
            atual = atual / parte
            if atual.is_symlink() and not atual.exists():
                problemas.add(f"{atual.relative_to(destino)}: link quebrado")
                break
            if atual.exists() and not atual.is_dir():
                problemas.add(f"{atual.relative_to(destino)}: existe e não é pasta")
                break
        alvo = destino / item["caminho"]
        if alvo.is_symlink() and not alvo.exists():
            problemas.add(f"{item['caminho']}: link quebrado")
    return sorted(problemas)


def raiz_git(destino: Path) -> Path | None:
    existente = destino
    while not existente.exists():
        existente = existente.parent
    resultado = subprocess.run(
        ["git", "-C", str(existente), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    return Path(resultado.stdout.strip()).resolve() if resultado.returncode == 0 else None


def avisos(destino: Path) -> list[str]:
    mensagens = []
    casa = Path.home().resolve()
    absoluto = destino.resolve()
    sincronizadas = [casa / "Documents", casa / "Desktop", casa / "Library" / "Mobile Documents"]
    if any(pasta == absoluto or pasta in absoluto.parents for pasta in sincronizadas) and not any(
        parte.endswith(".nosync") for parte in absoluto.parts
    ):
        mensagens.append(
            "destino numa pasta que o iCloud pode sincronizar, sem '.nosync' no caminho: "
            "ele pode esvaziar "
            ".git, venv e node_modules (renomeie a pasta para <nome>.nosync)"
        )
    existente = absoluto
    while not existente.exists():
        existente = existente.parent
    livre = shutil.disk_usage(existente).free / 1024**3
    if livre < 15:
        mensagens.append(
            f"só {livre:.0f} GB livres no disco: worktrees em paralelo pedem pelo menos 15 GB"
        )
    return mensagens


def escrever(destino: Path, plano: list[dict], adotar: bool) -> tuple[list[str], list[str]]:
    criados: list[str] = []
    pulados: list[str] = []
    for item in plano:
        alvo = destino / item["caminho"]
        if alvo.exists() or alvo.is_symlink():
            pulados.append(item["caminho"])
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        if "link" in item:
            alvo.symlink_to(item["link"])
        else:
            alvo.write_text(item["conteudo"], encoding="utf-8")
            os.chmod(alvo, item["modo"])
        criados.append(item["caminho"])
    return criados, pulados


def iniciar_git(destino: Path) -> str:
    if (destino / ".git").exists():
        return "git: a pasta já é um repositório; nada feito"
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=destino, check=True)
    return "git: repositório criado na branch main (sem commit)"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--destino", type=Path, required=True, help="pasta do projeto novo")
    parser.add_argument(
        "--respostas", type=Path, required=True, help="JSON com as respostas da entrevista"
    )
    parser.add_argument("--simular", action="store_true", help="só lista o que seria criado")
    parser.add_argument(
        "--adotar", action="store_true", help="pasta com conteúdo: cria só o que falta"
    )
    parser.add_argument("--sem-git", action="store_true", help="não roda git init")
    args = parser.parse_args()

    try:
        respostas = json.loads(args.respostas.read_text(encoding="utf-8"))
        ctx, modulos = contexto(respostas)
        plano = planejar(ctx, modulos)
    except (OSError, json.JSONDecodeError, ErroTemplate) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2

    destino = args.destino.expanduser()
    if destino.is_symlink() and not destino.exists():
        print(f"erro: {destino} é um link quebrado", file=sys.stderr)
        return 2
    if destino.exists() and not destino.is_dir():
        print(f"erro: {destino} existe e não é uma pasta", file=sys.stderr)
        return 2
    raiz = raiz_git(destino)
    if raiz is not None and raiz != destino.resolve():
        print(
            f"erro: {destino} fica dentro do repositório {raiz}. O kit cria a raiz de um "
            "repositório (o CI e as "
            "skills só valem lá): use uma pasta fora dele, ou a própria raiz com --adotar",
            file=sys.stderr,
        )
        return 2
    for aviso in avisos(destino):
        print(f"aviso: {aviso}")
    ocupado = conteudo_relevante(destino)
    problemas = conflitos(destino, plano)

    if args.simular:
        for item in plano:
            existe = (destino / item["caminho"]).exists() or (
                destino / item["caminho"]
            ).is_symlink()
            print(
                item["caminho"]
                + (f" -> {item['link']}" if "link" in item else "")
                + (" (já existe; seria pulado)" if existe else "")
            )
        print(f"{len(plano)} itens; módulos: {', '.join(sorted(modulos)) or 'nenhum'}")
        if ocupado and not args.adotar:
            print("aviso: a pasta não está vazia; sem --adotar, a execução real recusa")
        for problema in problemas:
            print(f"aviso: conflito que impede a escrita: {problema}")
        return 0

    if ocupado and not args.adotar:
        print(
            f"erro: {destino} não está vazia ({', '.join(ocupado[:8])}"
            f"{'…' if len(ocupado) > 8 else ''}); use --adotar para criar só o que falta",
            file=sys.stderr,
        )
        return 1
    if problemas:
        for problema in problemas:
            print(f"erro: {problema}", file=sys.stderr)
        print("nada foi escrito: resolva os conflitos acima e rode de novo", file=sys.stderr)
        return 1
    destino.mkdir(parents=True, exist_ok=True)
    criados, pulados = escrever(destino, plano, args.adotar)
    print(f"{len(criados)} itens criados em {destino}")
    for item in pulados:
        print(f"pulado (já existia): {item}")
    if not args.sem_git:
        print(iniciar_git(destino))
    print(f"módulos: {', '.join(sorted(modulos)) or 'nenhum'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
