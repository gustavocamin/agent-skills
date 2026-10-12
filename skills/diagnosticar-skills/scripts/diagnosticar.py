#!/usr/bin/env python3
"""Read-only installation diagnostics. No network, fixes, or runtime CLI probes."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True


def git(repo: Path, *args: str) -> str | None:
    if not shutil.which("git"):
        return None
    result = subprocess.run(["git", "--no-optional-locks", "-C", str(repo), *args],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--destino", action="append", type=Path, default=[])
    parser.add_argument("--projeto", action="append", default=[])
    parser.add_argument("--agente", choices=["claude", "codex", "ambos"], default="ambos")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    repo = args.repo.expanduser().resolve()
    helper = repo / "scripts/instalar.py"
    if not helper.is_file():
        parser.error("clone sem scripts/instalar.py; diagnóstico desta versão requer o helper de hash")
    spec = importlib.util.spec_from_file_location("agent_skills_installer", helper)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    sources = list(sorted((repo / "skills").glob("*/SKILL.md")))
    for project in args.projeto:
        if Path(project).name != project or project in (".", ".."):
            parser.error("nome de projeto inválido")
        root = repo / "projetos" / project / "skills"
        if not root.is_dir():
            parser.error(f"projeto não encontrado: {project}")
        sources.extend(sorted(root.glob("*/SKILL.md")))
    destinations = args.destino or [Path.home() / folder / "skills" for agent, folder in
                                  (("claude", ".claude"), ("codex", ".agents"))
                                  if args.agente in (agent, "ambos")]
    rows = []
    for destination in destinations:
        destination = destination.expanduser().absolute()
        manifest_file = module.manifest_path(destination)
        try:
            manifest = module.load_manifest(manifest_file)
            records = manifest.get("items", {})
        except (OSError, ValueError, TypeError, module.InstallError) as exc:
            rows.append({"destino": str(destination), "estado": "erro-leitura",
                         "evidencia": f"manifesto: {exc}"})
            records = {}
        for entry in sources:
            source = entry.parent
            target = destination / source.name
            record = records.get(source.name, {})
            row = {"skill": source.name, "origem": str(source), "destino": str(target),
                   "hash_fonte": None, "hash_instalado": None,
                   "baseline": record.get("baseline") if isinstance(record, dict) else None}
            try:
                name_match = re.search(r"^name:\s*(.+)$", entry.read_text(encoding="utf-8"), re.M)
                declared_name = name_match[1].strip("\"'") if name_match else None
                row["nome_declarado"] = declared_name
                if declared_name != source.name:
                    row["aviso_compatibilidade"] = "name difere da pasta; carregamento não verificado"
                source_hash = row["hash_fonte"] = module.hash_item(source)
                if not target.exists() and not target.is_symlink():
                    state = "ausente"
                elif target.is_symlink() and target.resolve() == source.resolve():
                    row["hash_instalado"] = module.hash_item(target)
                    state = "link-fonte"
                else:
                    installed = row["hash_instalado"] = module.hash_item(target)
                    if installed == source_hash:
                        state = "igual"
                    elif record and record.get("source") != str(source.resolve()):
                        state = "origem-diferente"
                    elif row["baseline"]:
                        state = "atualizacao-gerenciada" if installed == row["baseline"] else "edicao-local"
                    else:
                        state = "divergente-sem-proveniencia"
                row["estado"] = state
            except (OSError, ValueError, TypeError, AttributeError, module.InstallError) as exc:
                row.update(estado="erro-leitura", evidencia=str(exc))
            rows.append(row)
    result = {"repo": str(repo), "commit": git(repo, "rev-parse", "HEAD"),
              "fonte_modificada": git(repo, "status", "--porcelain"),
              "plataforma": platform.system(), "agente": args.agente,
              "runtime": "não verificado; não executamos agentes, CLIs ou autenticação",
              "pre_requisitos": {command: shutil.which(command) for command in
                                   ("python3", "bash", "git", "claude", "codex", "obsidian", "defuddle", "mlflow")},
              "limites": ["Obsidian CLI: app desktop aberto não verificado",
                          "liberar-disco: requer macOS; alvo remoto não inspecionado",
                          "Claude commands/agents não são entrypoints Codex",
                          "Binário encontrado não comprova versão, login nem funcionamento"],
              "itens": rows}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Fonte: {repo} | commit: {result['commit'] or 'não verificado'}")
        print(result["runtime"])
        for row in rows:
            print(f"{row.get('skill', 'manifesto')}: {row['estado']} | {row['destino']}")
            if row.get("aviso_compatibilidade"):
                print(f"  Aviso: {row['aviso_compatibilidade']} ({row.get('nome_declarado')})")
            if row.get("evidencia"):
                print(f"  Evidência: {row['evidencia']}")
        print("Use --json para hashes completos, baseline e caminhos dos pré-requisitos.")
        for limit in result["limites"]:
            print(f"Limite: {limit}")
    return 1 if any(row["estado"] == "erro-leitura" for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
