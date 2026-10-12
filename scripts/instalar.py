#!/usr/bin/env python3
"""Instalador conservador, sem dependências externas além de git.

API somente leitura para diagnósticos: hash_item, manifest_path, load_manifest,
plan_item. Um baseline autoriza atualizar apenas a cópia ainda idêntica à última
instalação, da mesma origem absoluta. Hash inclui tipos, permissões e links (não
os segue), mas não timestamps. Estado e backups ficam fora da pasta de skills.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
import uuid

ROOT = Path(__file__).resolve().parent.parent
VERSION = 1


class InstallError(Exception):
    """Erro seguro e legível, antes de substituir um item incerto."""


def absolute(path: Path | str) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def exists(path: Path) -> bool:
    return os.path.lexists(path)


def hash_item(path: Path) -> str:
    """SHA-256 de JSON-lines [caminho, tipo, modo, payload], UTF-8, ordenado.

    modo = stat.S_IMODE (links usam 0); payload = SHA-256 dos bytes para
    arquivos, destino textual para links, '' para diretórios. Inclui a raiz '.'.
    json.dumps usa ensure_ascii=True, separators=(',', ':'); cada registro termina
    em '\\n'. Caminhos relativos usam '/'. Não ignora arquivos locais adicionais.
    """
    digest = hashlib.sha256()

    def visit(item: Path, relative: str) -> None:
        info = item.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if stat.S_ISLNK(info.st_mode):
            kind, mode, payload = 'link', 0, os.readlink(item)
        elif stat.S_ISREG(info.st_mode):
            content = hashlib.sha256()
            with item.open('rb') as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b''):
                    content.update(chunk)
            kind, payload = 'file', content.hexdigest()
        elif stat.S_ISDIR(info.st_mode):
            kind, payload = 'dir', ''
        else:
            raise InstallError(f'tipo de arquivo não suportado: {item}')
        record = json.dumps([relative, kind, mode, payload], separators=(',', ':'))
        digest.update((record + '\n').encode('utf-8'))
        if kind == 'dir':
            for child in sorted(item.iterdir(), key=lambda p: p.name):
                visit(child, child.name if relative == '.' else relative + '/' + child.name)

    visit(path, '.')
    return digest.hexdigest()


def manifest_path(destination: Path) -> Path:
    destination = absolute(destination)
    return destination.parent / ('.agent-skills-' + destination.name) / 'manifest.json'


def safe_ancestors(path: Path) -> None:
    """Não atravessa links em destinos, estado, backups ou exclusões do git."""
    for part in reversed([path, *path.parents]):
        if part.is_symlink():
            raise InstallError(f'caminho contém link simbólico; preservado: {part}')
        if exists(part) and not part.is_dir():
            raise InstallError(f'caminho não é diretório: {part}')


def load_manifest(path: Path) -> dict:
    safe_ancestors(path.parent)
    if path.is_symlink():
        raise InstallError(f'manifesto é link simbólico; preservado: {path}')
    if not exists(path):
        return {'version': VERSION, 'items': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or data.get('version') != VERSION or not isinstance(data.get('items'), dict):
            raise ValueError('formato ou versão desconhecida')
        for name, record in data['items'].items():
            if not name or Path(name).name != name or name in ('.', '..'):
                raise ValueError('nome inválido')
            if not isinstance(record, dict) or record.get('mode') not in ('copy', 'link'):
                raise ValueError('registro inválido')
            if not isinstance(record.get('source'), str) or not Path(record['source']).is_absolute():
                raise ValueError('origem inválida')
            for key in ('baseline', 'source_hash'):
                if not re.fullmatch(r'[a-f0-9]{64}', str(record.get(key, ''))):
                    raise ValueError('hash inválido')
        return data
    except (ValueError, OSError) as error:
        raise InstallError(f'manifesto inválido, não foi alterado: {path}: {error}') from error


def plan_item(source: Path, target: Path, record: dict | None, mode: str, force: bool = False) -> dict:
    """Retorna action/reason/source_hash/target_hash; nunca grava nem segue alvo-link.

    A política de git e a segurança dos diretórios são verificadas pelo chamador.
    Actions: install, update, replace, adopt, current, conflict.
    """
    source = absolute(source)
    source_hash = hash_item(source)
    current = hash_item(target) if exists(target) else None
    result = {'source_hash': source_hash, 'target_hash': current}
    same_source = bool(record and record.get('source') == str(source))
    actual_mode = 'link' if target.is_symlink() else 'copy'
    if current is None:
        action, reason = 'install', 'novo item'
    elif source == absolute(target):
        action, reason = 'conflict', 'alvo é a própria origem'
    elif actual_mode != mode:
        action, reason = 'conflict', 'mudança de modo copy/link exige --forcar'
    elif mode == 'link' and target.resolve() == source.resolve():
        action, reason = 'current' if same_source else 'adopt', 'link para a origem'
    elif mode == 'copy' and current == source_hash:
        action, reason = 'current' if same_source else 'adopt', 'conteúdo idêntico à origem'
    elif same_source and record.get('mode') == mode and current == record.get('baseline'):
        action, reason = 'update', 'instalação gerenciada intacta; origem mudou'
    else:
        action, reason = 'conflict', 'edição local ou item sem baseline desta origem'
    if force and action == 'conflict' and source != absolute(target):
        action, reason = 'replace', reason + '; substituir com backup'
    return {**result, 'action': action, 'reason': reason}


def writable(path: Path) -> bool:
    safe_ancestors(path)
    probe = path
    while not exists(probe):
        probe = probe.parent
    # Bits também funcionam nos testes executados como root (os.access sozinho não).
    return bool(probe.stat().st_mode & 0o222) and os.access(probe, os.W_OK | os.X_OK)


def git_run(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    # O repo é sempre o descoberto a partir de -C, nunca um índice/worktree herdado.
    env = dict(os.environ)
    for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE',
                 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
                 'GIT_PREFIX', 'GIT_CEILING_DIRECTORIES', 'GIT_DISCOVERY_ACROSS_FILESYSTEM'):
        env.pop(name, None)
    env['LC_ALL'] = 'C'
    return subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True, env=env)


def git_root(path: Path) -> Path | None:
    probe = path
    while not probe.is_dir():
        if probe == probe.parent:
            return None
        probe = probe.parent
    result = git_run(probe, 'rev-parse', '--show-toplevel')
    if result.returncode:
        message = result.stderr.strip()
        not_repo = message == 'fatal: not a git repository (or any of the parent directories): .git'
        not_repo = not_repo or message.startswith('fatal: not a git repository (or any parent up to mount point ')
        # Um .git vazio não é repo (alguns sandboxes montam essa sentinela em /tmp).
        # Metadados presentes mas ilegíveis/inválidos continuam bloqueando a escrita.
        marker = False
        for parent in [probe, *probe.parents]:
            candidate = parent / '.git'
            if exists(candidate) and (not candidate.is_dir() or candidate.is_symlink()
                                      or any(candidate.iterdir())):
                marker = True
                break
        if not_repo and not marker:
            return None
        raise InstallError(f'git não pôde verificar o repositório em {probe}; nada autorizado: {message}')
    if not result.stdout.strip():
        raise InstallError(f'git retornou raiz vazia em {probe}; nada autorizado')
    root = Path(result.stdout.strip()).resolve()
    real_probe = probe.resolve()
    if root != real_probe and root not in real_probe.parents:
        raise InstallError(f'git retornou raiz fora do destino: {root} / {probe}')
    return root


def is_tracked(path: Path) -> bool:
    root = git_root(path.parent)
    if root is None:
        return False
    relative = absolute(path).relative_to(root).as_posix()
    result = git_run(root, 'ls-files', '-z', '--', ':(literal)' + relative)
    if result.returncode:
        raise InstallError(f'não consegui verificar arquivos versionados em {path}')
    return bool(result.stdout)


def ignore_git(path: Path) -> None:
    root = git_root(path.parent)
    if root is None:
        return
    relative = absolute(path).relative_to(root).as_posix()
    # Escapa metacaracteres gitignore, inclusive espaços finais e barras invertidas.
    escaped = ''.join('\\' + char if char in '\\*?[]#! ' else char for char in relative)
    entry = '/' + escaped
    common = git_run(root, 'rev-parse', '--git-common-dir')
    if common.returncode:
        raise InstallError(f'não consegui localizar exclusões locais do git em {root}')
    gitdir = Path(common.stdout.strip())
    if not gitdir.is_absolute():
        gitdir = root / gitdir
    exclude = absolute(gitdir) / 'info' / 'exclude'
    safe_ancestors(exclude.parent)
    if exclude.is_symlink() or (exists(exclude) and not exclude.is_file()):
        raise InstallError(f'exclusão git insegura; preservada: {exclude}')
    content = exclude.read_text(encoding='utf-8') if exists(exclude) else ''
    if entry not in content.splitlines():
        exclude.parent.mkdir(parents=True, exist_ok=True)
        with exclude.open('a', encoding='utf-8') as file:
            if content and not content.endswith('\n'):
                file.write('\n')
            file.write(entry + '\n')


def save_manifest(path: Path, manifest: dict) -> None:
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if exists(path) and path.read_text(encoding='utf-8') == rendered:
        return
    safe_ancestors(path.parent)
    if path.is_symlink():
        raise InstallError(f'manifesto é link simbólico: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.manifest-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as file:
            file.write(rendered)
            file.flush()
            os.fsync(file.fileno())
        os.replace(name, path)
    finally:
        if os.path.lexists(name):
            os.unlink(name)


def validate_source(source: Path) -> None:
    if source.is_symlink():
        raise InstallError(f'origem contém link simbólico; não importei: {source}')
    if source.is_dir():
        for child in source.iterdir():
            validate_source(child)
    elif not source.is_file():
        raise InstallError(f'origem não é arquivo comum ou diretório: {source}')


def install_item(source: Path, target: Path, state: Path, plan: dict, mode: str) -> Path | None:
    """Prepara cópia íntegra antes da troca; toda substituição conserva backup."""
    target.parent.mkdir(parents=True, exist_ok=True)
    state.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.stage-', dir=state.parent) as temporary:
        staged = Path(temporary) / 'item'
        if mode == 'link':
            staged.symlink_to(source, target_is_directory=source.is_dir())
        elif source.is_dir():
            shutil.copytree(source, staged, symlinks=True)
        else:
            shutil.copy2(source, staged)
        if hash_item(source) != plan['source_hash']:
            raise InstallError(f'origem mudou durante a instalação; tente novamente: {source}')
        if mode == 'copy' and hash_item(staged) != plan['source_hash']:
            raise InstallError(f'cópia divergiu da origem; alvo preservado: {target}')
        current = hash_item(target) if exists(target) else None
        if current != plan['target_hash']:
            raise InstallError(f'alvo mudou durante a instalação; preservado: {target}')
        backup = None
        if current is not None:
            folder = state.parent / 'backups'
            safe_ancestors(folder)
            folder.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = folder / (target.name + '--' + stamp + '--' + uuid.uuid4().hex[:8])
            os.replace(target, backup)
        try:
            os.replace(staged, target)
        except OSError:
            if backup is not None:
                os.replace(backup, target)
            raise
        return backup


def fallback_repo(repo: Path, cwd: Path, workspace: Path) -> Path:
    root = git_root(cwd)
    if root and root != repo.resolve():
        return root
    candidates = []
    if workspace.is_dir():
        for candidate in workspace.iterdir():
            if candidate.is_dir() and (candidate / '.git').exists():
                root = git_root(candidate)
                if root and root != repo.resolve():
                    candidates.append(root)
    candidates = sorted(set(candidates))
    if len(candidates) != 1:
        raise InstallError('nenhuma pasta pessoal com escrita e não há repo de tarefa único '
                           f'no diretório atual ou em {workspace} ({len(candidates)} candidatos)')
    return candidates[0]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Instala e atualiza skills intactas; preserva edições locais.')
    parser.add_argument('--agente', choices=('claude', 'codex', 'ambos'), default='ambos',
                        help='destinos pessoais/de projeto (padrão: ambos)')
    parser.add_argument('--destino', action='append', default=[], metavar='PASTA',
                        help='destino explícito para skills; pode repetir')
    parser.add_argument('--projeto', action='append', default=[], metavar='NOME',
                        help='adiciona projetos/NOME; pode repetir')
    parser.add_argument('--em', metavar='PASTA', help='instala itens do projeto nesta pasta existente')
    parser.add_argument('--link', action='store_true', help='links para este clone, em vez de cópias')
    parser.add_argument('--forcar', action='store_true', help='substitui conflitos com backup; nunca itens versionados')
    parser.add_argument('--dry-run', action='store_true', help='mostra o plano sem gravar nada')
    args = parser.parse_args(argv)
    if args.em and not args.projeto:
        parser.error('--em requer --projeto')
    return args


def run(args: argparse.Namespace, repo: Path = ROOT) -> int:
    if shutil.which('git') is None:
        raise InstallError('dependência ausente: git (necessário para proteger arquivos versionados)')
    home = absolute(os.environ.get('HOME', str(Path.home())))
    agents = ('claude', 'codex') if args.agente == 'ambos' else (args.agente,)
    folders = {'claude': '.claude', 'codex': '.agents'}
    projects = []
    for name in dict.fromkeys(args.projeto):
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or not (repo / 'projetos' / name).is_dir():
            raise InstallError(f'projeto inválido ou inexistente: {name}')
        projects.append(repo / 'projetos' / name)
    project_root = absolute(args.em) if args.em else None
    if project_root is not None and not project_root.is_dir():
        raise InstallError(f'--em não é uma pasta existente: {project_root}')
    if args.destino:
        destinations = list(dict.fromkeys(absolute(p) for p in args.destino))
    else:
        destinations = []
        for agent in agents:
            destination = home / folders[agent] / 'skills'
            if writable(destination) and writable(manifest_path(destination).parent):
                destinations.append(destination)
            else:
                print(f'install: sem escrita em {destination}; pulei')
        if not destinations:
            root = fallback_repo(repo, Path.cwd(), absolute(os.environ.get('AGENT_SKILLS_WORKSPACE', '/workspace')))
            destinations = [root / folders[a] / 'skills' for a in agents]
            print(f'install: usando o repo da tarefa: {root}')
    items: dict[Path, Path] = {}

    def add(source: Path, destination: Path) -> None:
        target = destination / source.name
        if target in items and items[target] != source:
            raise InstallError(f'duas origens disputam o mesmo alvo: {target}')
        items[target] = source

    for destination in destinations:
        for source in sorted((repo / 'skills').iterdir()):
            if source.is_dir() or source.is_symlink():
                add(source, destination)
    for project in projects:
        selected = [project_root / folders[a] / 'skills' for a in agents] if project_root else destinations
        for destination in selected:
            for source in sorted((project / 'skills').glob('*')):
                if source.is_dir() or source.is_symlink():
                    add(source, destination)
        if 'claude' in agents:
            for kind in ('commands', 'agents'):
                destination = (project_root or home) / '.claude' / kind
                for source in sorted((project / kind).glob('*.md')):
                    add(source, destination)
    manifests: dict[Path, dict] = {}
    plans = []
    mode = 'link' if args.link else 'copy'
    # Valida todo o plano antes de criar pastas/estado. --dry-run usa o mesmo plano.
    for target, source in items.items():
        safe_ancestors(source.parent)
        validate_source(source)
        safe_ancestors(target.parent)
        if source == target or source in target.parents or target in source.parents:
            raise InstallError(f'origem e destino se sobrepõem: {source} / {target}')
        state = manifest_path(target.parent)
        if state not in manifests:
            manifests[state] = load_manifest(state)
        if is_tracked(target) or is_tracked(state.parent):
            plan = {'action': 'protected', 'reason': 'arquivo do projeto versionado; nunca substituído'}
        elif not writable(target.parent) or not writable(state.parent):
            plan = {'action': 'protected', 'reason': 'destino/estado sem escrita'}
        else:
            plan = plan_item(source, target, manifests[state]['items'].get(target.name), mode, args.forcar)
        plans.append((source, target, state, plan))
    installed = same = skipped = 0
    for source, target, state, plan in plans:
        action = plan['action']
        prefix = 'install (dry-run)' if args.dry_run else 'install'
        if action in ('conflict', 'protected'):
            print(f'{prefix}: preservei {target}: {plan["reason"]}')
            skipped += 1
            continue
        if action in ('install', 'update', 'replace'):
            installed += 1
        else:
            same += 1
        if args.dry_run:
            print(f'{prefix}: {action} {target}: {plan["reason"]}')
            continue
        # A exclusão vem antes da escrita; nenhum backup ou manifesto fica no status.
        ignore_git(target)
        ignore_git(state.parent)
        if action in ('install', 'update', 'replace'):
            backup = install_item(source, target, state, plan, mode)
            print(f'install: {action} {target}' + (f' (backup: {backup})' if backup else ''))
        record = {'source': str(source), 'source_hash': plan['source_hash'],
                  'baseline': hash_item(target), 'mode': mode}
        manifests[state]['items'][target.name] = record
        save_manifest(state, manifests[state])
    print(f'install: {installed} instaladas, {same} já atualizadas, {skipped} puladas (de {len(plans)})'
          + ('; simulação, nada gravado' if args.dry_run else ''))
    return 0


def main() -> int:
    if sys.version_info < (3, 10):
        print("install: requer Python 3.10 ou mais recente", file=sys.stderr)
        return 1
    try:
        return run(parse_args())
    except (InstallError, OSError) as error:
        print(f'install: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
