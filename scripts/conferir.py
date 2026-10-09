"""Confere o repo de skills antes de um commit e no CI.

- toda pasta de skills/ e projetos/<p>/ tem SKILL.md com frontmatter, name em kebab-case e
  description de até 1024 caracteres;
- nenhum name se repete no mesmo conjunto de instalação (skills/ + um projeto);
- toda skill de terceiros está listada no TERCEIROS.md, e o contrário;
- nenhum token comum (Databricks, GitHub, Anthropic/OpenAI) em arquivo versionado;
- o install.sh instala tudo num HOME vazio, é idempotente, não sobrescreve sem --forcar e, sem
  HOME com escrita, instala no repo da tarefa sem sujar o git status dele.

Uso: python3 scripts/conferir.py
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOKEN = re.compile(
    r"dapi[0-9a-f]{32}"
    r"|gh[pousr]_[A-Za-z0-9]{36}"
    r"|github_pat_[A-Za-z0-9_]{22,}"
    r"|sk-[A-Za-z0-9_-]{32,}"
)

erros: list[str] = []


def frontmatter(arquivo: Path) -> dict[str, str]:
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    if not linhas or linhas[0].strip() != "---":
        erros.append(f"{arquivo.relative_to(RAIZ)}: sem frontmatter")
        return {}
    campos: dict[str, str] = {}
    for linha in linhas[1:]:
        if linha.strip() == "---":
            return campos
        m = re.match(r"^([a-z-]+):\s*(.*)$", linha)
        if m:
            campos[m.group(1)] = m.group(2).strip().strip("\"'")
    erros.append(f"{arquivo.relative_to(RAIZ)}: frontmatter sem fechamento")
    return campos


def conferir_conjunto(pastas: list[Path], rotulo: str) -> None:
    vistos: dict[str, Path] = {}
    for pasta in pastas:
        skill = pasta / "SKILL.md"
        rel = pasta.relative_to(RAIZ)
        if not skill.is_file():
            erros.append(f"{rel}: sem SKILL.md")
            continue
        campos = frontmatter(skill)
        nome, descricao = campos.get("name", ""), campos.get("description", "")
        if not NOME.match(nome):
            erros.append(f"{rel}: name '{nome}' não é kebab-case")
        if not descricao or len(descricao) > 1024:
            erros.append(f"{rel}: description vazia ou com mais de 1024 caracteres ({len(descricao)})")
        if nome in vistos:
            erros.append(f"{rotulo}: name '{nome}' repetido em {vistos[nome].relative_to(RAIZ)} e {rel}")
        vistos[nome] = pasta


def pastas(dir_: Path) -> list[Path]:
    return sorted(p for p in dir_.iterdir() if p.is_dir())


def conferir_skills() -> None:
    gerais = pastas(RAIZ / "skills")
    conferir_conjunto(gerais, "skills/")
    for projeto in pastas(RAIZ / "projetos"):
        conferir_conjunto(gerais + pastas(projeto), f"skills/ + {projeto.relative_to(RAIZ)}")
        repetidas = {p.name for p in gerais} & {p.name for p in pastas(projeto)}
        if repetidas:
            erros.append(f"{projeto.relative_to(RAIZ)}: pasta com o mesmo nome de skills/: {sorted(repetidas)}")

    listadas = set(re.findall(r"^\| `([a-z0-9-]+)` \|", (RAIZ / "TERCEIROS.md").read_text(), re.M))
    for nome in listadas - {p.name for p in gerais}:
        erros.append(f"TERCEIROS.md: '{nome}' não existe em skills/")


def conferir_segredos() -> None:
    arquivos = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=RAIZ, capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    for nome in arquivos:
        caminho = RAIZ / nome
        if not caminho.is_file():
            continue
        try:
            texto = caminho.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if TOKEN.search(texto):
            erros.append(f"{nome}: parece conter um token")


def rodar(args: list[str], home: Path, cwd: Path | None = None) -> str:
    env = {**os.environ, "HOME": str(home)}
    r = subprocess.run(["bash", str(RAIZ / "install.sh"), *args], cwd=cwd or home, env=env,
                       capture_output=True, text=True)
    if r.returncode != 0:
        erros.append(f"install.sh {' '.join(args)} saiu com {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def conferir_install() -> None:
    gerais = {p.name for p in pastas(RAIZ / "skills")}
    projeto = next(iter(pastas(RAIZ / "projetos")), None)
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        home.mkdir()
        rodar([], home)
        for d in (".claude/skills", ".agents/skills"):
            instaladas = {p.name for p in (home / d).iterdir()}
            if instaladas != gerais:
                erros.append(f"install.sh: {d} ficou com {sorted(instaladas ^ gerais)} a mais ou a menos")
        if "0 instaladas" not in rodar([], home):
            erros.append("install.sh: a segunda rodada reinstalou algo")

        alvo = home / ".claude/skills" / sorted(gerais)[0] / "SKILL.md"
        alvo.write_text(alvo.read_text() + "\nedição local\n")
        rodar([], home)
        if "edição local" not in alvo.read_text():
            erros.append("install.sh: sobrescreveu uma skill editada sem --forcar")
        rodar(["--forcar"], home)
        if "edição local" in alvo.read_text():
            erros.append("install.sh: --forcar não substituiu a skill editada")

        if projeto:
            rodar(["--projeto", projeto.name], home)
            faltam = {p.name for p in pastas(projeto)} - {p.name for p in (home / ".claude/skills").iterdir()}
            if faltam:
                erros.append(f"install.sh --projeto {projeto.name}: faltaram {sorted(faltam)}")

        # HOME sem escrita: instala no repo da tarefa, fora do git status.
        ro_home = Path(tmp) / "ro-home"
        ro_home.mkdir()
        tarefa = Path(tmp) / "tarefa"
        tarefa.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=tarefa, check=True)
        ro_home.chmod(0o555)
        try:
            rodar([], ro_home, cwd=tarefa)
        finally:
            ro_home.chmod(0o755)
        instaladas = {p.name for p in (tarefa / ".agents/skills").iterdir()} if (tarefa / ".agents/skills").is_dir() else set()
        if instaladas != gerais:
            erros.append("install.sh: com HOME só de leitura, não instalou no repo da tarefa")
        sujo = subprocess.run(["git", "status", "--porcelain"], cwd=tarefa, capture_output=True, text=True).stdout
        if sujo.strip():
            erros.append(f"install.sh: sujou o git status do repo da tarefa:\n{sujo}")
        shutil.rmtree(tarefa)


def main() -> int:
    conferir_skills()
    conferir_segredos()
    conferir_install()
    if erros:
        print("\n".join(f"✗ {e}" for e in erros))
        return 1
    print("✓ skills, segredos e install.sh conferidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
