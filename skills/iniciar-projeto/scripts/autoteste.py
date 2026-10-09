#!/usr/bin/env python3
"""Autoteste do kit: gera projetos de exemplo e confere que nascem verdes.

    python3 autoteste.py [--python <interpretador com pytest e ruff>] [--manter]

Para cada uma das 8 combinações de módulos: gera o projeto, procura marcador que sobrou, confere
a recusa de pasta ocupada e o --adotar, cria uma feature de exemplo e roda pytest e ruff. Nas
variantes sem módulos e com todos, prova com mutações que os testes do processo pegam um projeto
quebrado. Confere também que o gerador recusa entradas ruins sem escrever nada. Só usa a biblioteca
padrão; o interpretador indicado precisa ter pytest e ruff (a venv de um projeto gerado serve).
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
GERADOR = KIT / "scripts" / "criar_projeto.py"
MODULOS = ("codex", "databricks", "agente")
BASE = {
    "projeto": "Painel de Vendas",
    "dono": "Fulana",
    "data": "2026-10-08",
    "alerta": ["segredos", "o banco de produção"],
    "invariantes": ["O app nunca escreve no schema de vendas."],
}
VARIANTES = {
    "-".join(combo) or "nenhum": {**BASE, "modulos": list(combo)}
    for tamanho in range(len(MODULOS) + 1)
    for combo in itertools.combinations(MODULOS, tamanho)
}
COM_MUTACOES = {"nenhum", "codex-databricks-agente"}
ENTRADAS_RUINS = {
    "dono com dois-pontos": {"projeto": "X", "dono": "Equipe: Dados"},
    "dono com aspas": {"projeto": "X", "dono": 'Ana "Nina"'},
    "data inexistente": {"projeto": "X", "dono": "Ana", "data": "2026-13-45"},
    "alerta como texto": {"projeto": "X", "dono": "Ana", "alerta": "o banco"},
    "módulo desconhecido": {"projeto": "X", "dono": "Ana", "modulos": ["outro"]},
    "python fora da faixa": {"projeto": "X", "dono": "Ana", "python": "3.99"},
    "lista no topo": ["X"],
}
SOBRA = re.compile(r"(?<!\$)\{\{(?:[A-Z][A-Z0-9_]*|[#/]se\b[^{}\n]*)\}\}")
PLANO = """# F01 — Exemplo · Plano

Integra: Claude Code
Branch: `feature/F01-exemplo`

## Objetivo

Exemplo do autoteste.

## Grupos de tarefas

### Grupo 1 — Contrato
Dono: Claude Code · Toca: `src/contrato.py`
- [ ] Tarefa

### Grupo 2 — Tela
Dono: {dono2} · Branch: `feature/F01-exemplo--g2-{sufixo}` · Toca: `src/tela.py`
- [ ] Tarefa

## Fora do escopo desta feature

- nada
"""


def rodar(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False, env=env)


def checar(condicao: bool, mensagem: str, falhas: list[str]) -> None:
    print(("ok    " if condicao else "FALHA ") + mensagem)
    if not condicao:
        falhas.append(mensagem)


def entradas_ruins(base: Path, falhas: list[str]) -> None:
    print("\n== entradas ruins")
    for descricao, respostas in ENTRADAS_RUINS.items():
        arquivo = base / "ruim.json"
        arquivo.write_text(json.dumps(respostas), encoding="utf-8")
        destino = base / "ruim"
        resultado = rodar(
            sys.executable, str(GERADOR), "--destino", str(destino), "--respostas", str(arquivo)
        )
        checar(
            resultado.returncode == 2 and not destino.exists(),
            f"recusa {descricao} sem escrever",
            falhas,
        )
    arquivo_comum = base / "ocupa"
    arquivo_comum.write_text("x", encoding="utf-8")
    (base / "ok.json").write_text(json.dumps({"projeto": "X", "dono": "Ana"}), encoding="utf-8")
    resultado = rodar(
        sys.executable,
        str(GERADOR),
        "--destino",
        str(arquivo_comum),
        "--respostas",
        str(base / "ok.json"),
    )
    checar(resultado.returncode == 2, "recusa destino que é arquivo", falhas)


def variante(nome: str, respostas: dict, python: str, base: Path, falhas: list[str]) -> None:
    print(f"\n== variante {nome}")
    arquivo = base / f"{nome}.json"
    arquivo.write_text(json.dumps(respostas), encoding="utf-8")
    projeto = base / nome
    simulado = rodar(
        sys.executable,
        str(GERADOR),
        "--destino",
        str(projeto),
        "--respostas",
        str(arquivo),
        "--simular",
    )
    checar(simulado.returncode == 0 and not projeto.exists(), "--simular não escreve nada", falhas)
    gerado = rodar(
        sys.executable, str(GERADOR), "--destino", str(projeto), "--respostas", str(arquivo)
    )
    checar(
        gerado.returncode == 0,
        f"gera o projeto ({gerado.stdout.strip().splitlines()[-1:]})",
        falhas,
    )
    if gerado.returncode:
        print(gerado.stderr)
        return

    sobras = [
        f"{caminho.relative_to(projeto)}: {achado.group(0)}"
        for caminho in projeto.rglob("*")
        if caminho.is_file() and ".git" not in caminho.parts
        for achado in [SOBRA.search(caminho.read_text(encoding="utf-8", errors="ignore"))]
        if achado
    ]
    checar(not sobras, f"nenhum marcador sobrou {sobras[:3]}", falhas)

    de_novo = rodar(
        sys.executable, str(GERADOR), "--destino", str(projeto), "--respostas", str(arquivo)
    )
    checar(de_novo.returncode == 1, "recusa pasta ocupada sem --adotar", falhas)
    adotar = rodar(
        sys.executable,
        str(GERADOR),
        "--destino",
        str(projeto),
        "--respostas",
        str(arquivo),
        "--adotar",
    )
    checar(
        adotar.returncode == 0 and "0 itens criados" in adotar.stdout,
        "--adotar não sobrescreve nada",
        falhas,
    )

    codex = "codex" in respostas.get("modulos", [])
    feature = projeto / "specs" / "features" / "F01-exemplo"
    feature.mkdir(parents=True)
    plano = PLANO.format(
        dono2="Codex (cloud)" if codex else "Claude Code", sufixo="codex" if codex else "claude"
    )
    (feature / "plan.md").write_text(plano, encoding="utf-8")
    for nome_arquivo in ("requirements.md", "validation.md"):
        origem = projeto / "specs" / "features" / "_template" / nome_arquivo
        (feature / nome_arquivo).write_text(origem.read_text(encoding="utf-8"), encoding="utf-8")

    testes = rodar(python, "-m", "pytest", "-q", "-p", "no:cacheprovider", cwd=projeto)
    resumo = (
        testes.stdout.strip().splitlines()[-1:]
        if testes.stdout
        else testes.stderr.strip().splitlines()[-1:]
    )
    checar(testes.returncode == 0, f"pytest verde {resumo}", falhas)
    if testes.returncode:
        print(testes.stdout[-3000:])
    lint = rodar(python, "-m", "ruff", "check", "--no-cache", ".", cwd=projeto)
    checar(lint.returncode == 0, "ruff limpo", falhas)
    if lint.returncode:
        print(lint.stdout[-2000:])
    # Os arquivos Python do kit nascem formatados e dentro do limite de linha do projeto.
    formato = rodar(
        python, "-m", "ruff", "format", "--check", "--no-cache", "scripts", "tests", cwd=projeto
    )
    linha = rodar(
        python,
        "-m",
        "ruff",
        "check",
        "--no-cache",
        "--select",
        "E501",
        "scripts",
        "tests",
        cwd=projeto,
    )
    checar(
        formato.returncode == 0 and linha.returncode == 0, "formatados e com linhas curtas", falhas
    )
    if formato.returncode or linha.returncode:
        print(formato.stdout[-1500:], linha.stdout[-1500:])

    if nome not in COM_MUTACOES:
        return
    # Mutações: os testes do processo precisam pegar um projeto quebrado.
    roadmap = projeto / "specs" / "constitution" / "roadmap.md"
    for descricao, alvo, velho, novo in (
        ("grupo sem Toca", feature / "plan.md", " · Toca: `src/contrato.py`", ""),
        (
            "título de grupo com hífen",
            feature / "plan.md",
            "### Grupo 2 — Tela",
            "### Grupo 2 - Tela",
        ),
        (
            "requisitos sem Interfaces",
            feature / "requirements.md",
            "## Interfaces",
            "### Interfaces",
        ),
        (
            "CI sem o conferidor",
            projeto / ".github/workflows/ci.yml",
            "      - run: python scripts/check_handoff.py --ci\n",
            "",
        ),
        (".gitignore sem .env", projeto / ".gitignore", "\n.env\n", "\n"),
        (
            "settings sem um deny",
            projeto / ".claude/settings.json",
            '      "Bash(git push -f *)",\n',
            "",
        ),
        (
            "Decisão fora de ordem",
            roadmap,
            "## Decisões\n",
            "## Decisões\n\n- 2026-01-01 — antiga — porquê: teste.\n",
        ),
    ):
        original = alvo.read_text(encoding="utf-8")
        alvo.write_text(original.replace(velho, novo, 1), encoding="utf-8")
        mutado = rodar(
            python,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "tests/test_processo.py",
            cwd=projeto,
        )
        checar(mutado.returncode != 0, f"mutação '{descricao}' derruba o test_processo", falhas)
        alvo.write_text(original, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--python", default=sys.executable, help="interpretador com pytest e ruff")
    parser.add_argument("--manter", action="store_true", help="não apaga os projetos gerados")
    args = parser.parse_args()
    if rodar(args.python, "-c", "import pytest, ruff").returncode:
        print(f"erro: {args.python} não tem pytest e ruff", file=sys.stderr)
        return 2
    base = Path(tempfile.mkdtemp(prefix="autoteste-kit-"))
    falhas: list[str] = []
    try:
        entradas_ruins(base, falhas)
        for nome, respostas in VARIANTES.items():
            variante(nome, respostas, args.python, base, falhas)
    finally:
        if args.manter:
            print(f"\nprojetos mantidos em {base}")
        else:
            shutil.rmtree(base, ignore_errors=True)
    print(f"\n{len(falhas)} falha(s)")
    return int(bool(falhas))


if __name__ == "__main__":
    sys.exit(main())
