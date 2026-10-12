"""Regressões do instalador: apenas cópias e HOMEs temporários, nunca o HOME real."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import shlex
import stat
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from instalar import hash_item, manifest_path

ROOT = Path(__file__).resolve().parent.parent
BASH = shutil.which('bash')
GIT = shutil.which('git')


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='agent-skills-test-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / 'repo fonte com espaços'
        self.repo.mkdir()
        (self.repo / 'scripts').mkdir()
        shutil.copy2(ROOT / 'install.sh', self.repo / 'install.sh')
        shutil.copy2(ROOT / 'scripts/instalar.py', self.repo / 'scripts/instalar.py')
        self.source = self.repo / 'skills/exemplo'
        self.source.mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('---\nname: exemplo\ndescription: exemplo\n---\nversão 1\n')
        (self.source / 'rodar.sh').write_text('#!/bin/sh\nprintf oi\n')
        (self.source / 'rodar.sh').chmod(0o755)
        project = self.repo / 'projetos/demo'
        for kind, name in [('skills', 'projeto/SKILL.md'), ('commands', 'today.md'), ('agents', 'audit.md')]:
            target = project / kind / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('---\nname: projeto\ndescription: do projeto\n---\n')
        self.home = self.base / 'home'
        self.home.mkdir()
        self.target = self.home / '.claude/skills/exemplo'

    def run_install(self, *args, home=None, cwd=None, env=None, expected=0):
        variables = {**os.environ, 'HOME': str(home or self.home),
                     'AGENT_SKILLS_WORKSPACE': str(self.base / 'empty-workspace'),
                     'PYTHONDONTWRITEBYTECODE': '1', **(env or {})}
        result = subprocess.run([BASH, str(self.repo / 'install.sh'), *map(str, args)],
                                cwd=cwd or self.home, env=variables, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def git(self, *args, cwd=None):
        return subprocess.run([GIT, '-C', str(cwd or self.project), *args],
                              capture_output=True, text=True, check=True).stdout

    def make_project(self):
        self.project = self.base / 'projeto alvo [teste]'
        self.project.mkdir()
        self.git('init', '-q')
        return self.project

    def source_change(self):
        (self.source / 'SKILL.md').write_text('versão 2\n')

    def backups(self, target=None):
        target = target or self.target
        return list((manifest_path(target.parent).parent / 'backups').glob('*'))

    def snapshot(self, folder):
        return {str(path.relative_to(folder)): (path.lstat().st_mode, path.lstat().st_mtime_ns,
                                              os.readlink(path) if path.is_symlink() else
                                              path.read_bytes() if path.is_file() else None)
                for path in sorted(folder.rglob('*'))}

    def test_default_install_and_idempotence(self):
        self.run_install()
        for relative in ('.claude/skills/exemplo', '.agents/skills/exemplo'):
            target = self.home / relative
            self.assertEqual(hash_item(self.source), hash_item(target))
            self.assertEqual(stat.S_IMODE((target / 'rodar.sh').stat().st_mode), 0o755)
            self.assertEqual({p.name for p in target.parent.iterdir()}, {'exemplo'})
            data = json.loads(manifest_path(target.parent).read_text())
            self.assertEqual(data['items']['exemplo']['baseline'], hash_item(target))
        before = self.snapshot(self.home)
        self.assertIn('0 instaladas', self.run_install().stdout)
        self.assertEqual(before, self.snapshot(self.home))
        self.assertFalse(self.backups())

    def test_managed_update_and_removed_file(self):
        self.run_install()
        previous = hash_item(self.target)
        self.source_change()
        (self.source / 'rodar.sh').unlink()
        self.assertIn('update', self.run_install().stdout)
        self.assertEqual(hash_item(self.target), hash_item(self.source))
        self.assertEqual(hash_item(self.backups()[0]), previous)
        self.assertFalse((self.target / 'rodar.sh').exists())
        self.assertIn('0 instaladas', self.run_install().stdout)

    def test_local_edits_preserved_and_force_backed_up(self):
        self.run_install()
        (self.target / 'SKILL.md').write_text('edição local\n')
        (self.target / 'extra.txt').write_text('nota local\n')
        previous = hash_item(self.target)
        manifest_before = manifest_path(self.target.parent).read_bytes()
        self.source_change()
        self.assertIn('preservei', self.run_install().stdout)
        self.assertEqual(hash_item(self.target), previous)
        self.assertEqual(manifest_path(self.target.parent).read_bytes(), manifest_before)
        self.run_install('--forcar')
        self.assertEqual(hash_item(self.target), hash_item(self.source))
        self.assertEqual(hash_item(self.backups()[0]), previous)
        self.assertIn('0 instaladas', self.run_install('--forcar').stdout)

    def test_unmanaged_conflict_and_equal_legacy_adoption(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_text('do usuário\n')
        self.run_install('--agente', 'claude')
        self.assertEqual((self.target / 'SKILL.md').read_text(), 'do usuário\n')
        self.assertFalse(manifest_path(self.target.parent).exists())
        self.run_install('--agente', 'claude', '--forcar')
        self.assertEqual((self.backups()[0] / 'SKILL.md').read_text(), 'do usuário\n')
        manifest_path(self.target.parent).unlink()
        before = self.target.stat().st_mtime_ns
        self.run_install('--agente', 'claude')
        self.assertEqual(before, self.target.stat().st_mtime_ns)
        self.source_change()
        self.run_install('--agente', 'claude')
        self.assertEqual(hash_item(self.target), hash_item(self.source))

    def test_another_clone_cannot_claim_stale_baseline(self):
        self.run_install('--agente', 'claude')
        before = hash_item(self.target)
        another = self.base / 'outro clone'
        shutil.copytree(self.repo, another)
        self.repo = another
        self.source = another / 'skills/exemplo'
        self.source_change()
        self.run_install('--agente', 'claude')
        self.assertEqual(hash_item(self.target), before)
        self.assertFalse(self.backups())
        self.run_install('--agente', 'claude', '--forcar')
        self.assertEqual(hash_item(self.target), hash_item(self.source))
        self.assertEqual(hash_item(self.backups()[0]), before)

    def test_chmod_is_local_edit(self):
        self.run_install('--agente', 'claude')
        (self.target / 'rodar.sh').chmod(0o644)
        self.source_change()
        self.run_install('--agente', 'claude')
        self.assertIn('versão 1', (self.target / 'SKILL.md').read_text())
        self.assertEqual(stat.S_IMODE((self.target / 'rodar.sh').stat().st_mode), 0o644)

    def test_dry_run_no_mutation_new_or_force(self):
        before = self.snapshot(self.base)
        self.run_install('--dry-run')
        self.assertEqual(before, self.snapshot(self.base))
        self.run_install('--agente', 'claude')
        (self.target / 'SKILL.md').write_text('edição local\n')
        before = self.snapshot(self.base)
        result = self.run_install('--dry-run', '--forcar')
        self.assertIn('replace', result.stdout)
        self.assertEqual(before, self.snapshot(self.base))

    def test_link_mode_and_explicit_mode_change(self):
        self.run_install('--agente', 'claude', '--link')
        self.assertTrue(self.target.is_symlink())
        self.source_change()
        self.run_install('--agente', 'claude', '--link')
        self.assertIn('versão 2', (self.target / 'SKILL.md').read_text())
        self.run_install('--agente', 'claude')
        self.assertTrue(self.target.is_symlink())
        self.run_install('--agente', 'claude', '--forcar')
        self.assertFalse(self.target.is_symlink())
        self.assertTrue(self.backups()[0].is_symlink())
        self.assertEqual(hash_item(self.source), hash_item(self.target))
        self.run_install('--agente', 'claude', '--link')
        self.assertFalse(self.target.is_symlink())
        self.run_install('--agente', 'claude', '--link', '--forcar')
        self.assertTrue(self.target.is_symlink())
        self.assertEqual(len(self.backups()), 2)

    def test_foreign_and_broken_links_never_followed(self):
        foreign = self.base / 'estrangeira'
        foreign.mkdir()
        (foreign / 'segredo').write_text('intacto')
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(foreign)
        previous = hash_item(foreign)
        self.run_install('--agente', 'claude')
        self.assertTrue(self.target.is_symlink())
        self.run_install('--agente', 'claude', '--forcar')
        self.assertEqual(hash_item(foreign), previous)
        self.assertEqual(os.readlink(self.backups()[0]), str(foreign))
        shutil.rmtree(self.target)
        self.target.symlink_to(self.base / 'missing')
        self.run_install('--agente', 'claude')
        self.assertTrue(self.target.is_symlink())
        self.run_install('--agente', 'claude', '--forcar')
        self.assertFalse(self.target.is_symlink())
        self.assertFalse((self.base / 'missing').exists())

    def test_source_and_destination_links_rejected(self):
        foreign = self.base / 'fora'
        foreign.mkdir()
        (self.home / '.claude').symlink_to(foreign)
        self.assertIn('link simbólico', self.run_install('--agente', 'claude', expected=1).stderr)
        self.assertFalse(list(foreign.iterdir()))
        (self.home / '.claude').unlink()
        (self.source / 'escape').symlink_to(foreign)
        self.assertIn('link simbólico', self.run_install(expected=1).stderr)
        self.assertFalse(list(self.home.iterdir()))

    def test_manifest_symlink_and_corruption_rejected(self):
        state = manifest_path(self.target.parent)
        state.parent.mkdir(parents=True)
        external = self.base / 'external.json'
        external.write_text('{}')
        state.symlink_to(external)
        self.run_install('--agente', 'claude', expected=1)
        self.assertEqual(external.read_text(), '{}')
        self.assertFalse(self.target.exists())
        state.unlink()
        state.write_text('{invalid')
        self.run_install('--agente', 'claude', '--forcar', expected=1)
        self.assertEqual(state.read_text(), '{invalid')
        self.assertFalse(self.target.exists())

    def test_agent_targets_and_project_scopes(self):
        for agent, folders in [('codex', ['.agents']), ('claude', ['.claude']), ('ambos', ['.claude', '.agents'])]:
            home = self.base / ('home-' + agent)
            home.mkdir()
            project = self.base / ('project-' + agent)
            project.mkdir()
            self.run_install('--agente', agent, '--projeto', 'demo', '--em', project, home=home)
            self.assertEqual({p.name for p in home.iterdir()}, set(folders))
            self.assertEqual({p.name for p in project.iterdir()}, set(folders))
            for folder in folders:
                self.assertTrue((home / folder / 'skills/exemplo/SKILL.md').exists())
                self.assertTrue((project / folder / 'skills/projeto/SKILL.md').exists())
                self.assertFalse((project / folder / 'skills/exemplo').exists())
            self.assertEqual((project / '.claude/commands/today.md').exists(), agent != 'codex')
            self.assertEqual((project / '.claude/agents/audit.md').exists(), agent != 'codex')

    def test_global_project_and_explicit_destination_spaces(self):
        destination = self.base / 'meu destino com espaços'
        second = self.base / 'outro destino'
        self.run_install('--destino', destination, '--destino', second, '--agente', 'codex', '--projeto', 'demo')
        for path in (destination, second):
            self.assertEqual({p.name for p in path.iterdir()}, {'exemplo', 'projeto'})
        self.assertFalse(list(self.home.iterdir()))
        self.run_install('--projeto', 'demo')
        self.assertTrue((self.home / '.claude/commands/today.md').exists())
        self.assertTrue((self.home / '.agents/skills/projeto/SKILL.md').exists())

    def test_git_clean_tracked_skill_never_overwritten(self):
        project = self.make_project()
        target = project / '.agents/skills/exemplo'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('versionado\n')
        self.git('add', '.')
        before = self.git('status', '--porcelain')
        self.run_install('--destino', target.parent, '--forcar')
        self.assertEqual((target / 'SKILL.md').read_text(), 'versionado\n')
        self.assertEqual(before, self.git('status', '--porcelain'))
        self.assertFalse(manifest_path(target.parent).exists())
        self.run_install('--projeto', 'demo', '--em', project, '--link')
        self.assertEqual(before, self.git('status', '--porcelain'))
        self.assertTrue((project / '.agents/skills/projeto').is_symlink())
        self.assertIn('/.agents/skills/projeto', (project / '.git/info/exclude').read_text())

    def test_home_readonly_fallback_and_git_hygiene(self):
        project = self.make_project()
        self.home.chmod(0o555)
        try:
            before = self.snapshot(project)
            self.run_install('--dry-run', cwd=project)
            self.assertEqual(before, self.snapshot(project))
            self.run_install(cwd=project)
            for folder in ('.claude', '.agents'):
                self.assertTrue((project / folder / 'skills/exemplo/SKILL.md').exists())
            self.assertEqual(self.git('status', '--porcelain'), '')
            self.assertFalse(list(self.home.iterdir()))
            self.source_change()
            self.run_install(cwd=project)
            self.assertEqual(self.git('status', '--porcelain'), '')
        finally:
            self.home.chmod(0o755)

    def test_readonly_home_workspace_fallback_ambiguous_rejected(self):
        workspace = self.base / 'workspace'
        project = workspace / 'único'
        project.mkdir(parents=True)
        self.git('init', '-q', cwd=project)
        self.home.chmod(0o555)
        env = {'AGENT_SKILLS_WORKSPACE': str(workspace)}
        try:
            self.run_install('--agente', 'codex', env=env)
            self.assertTrue((project / '.agents/skills/exemplo/SKILL.md').exists())
            self.assertFalse((project / '.claude').exists())
            second = workspace / 'segundo'
            second.mkdir()
            self.git('init', '-q', cwd=second)
            self.assertIn('2 candidatos', self.run_install(env=env, expected=1).stderr)
            self.assertFalse((second / '.agents').exists())
        finally:
            self.home.chmod(0o755)

    def test_missing_dependencies_and_bad_arguments(self):
        empty_path = self.base / 'path'
        empty_path.mkdir()
        self.assertIn('python3', self.run_install(env={'PATH': str(empty_path)}, expected=1).stderr)
        (empty_path / 'python3').symlink_to(sys.executable)
        self.assertIn('git', self.run_install(env={'PATH': str(empty_path)}, expected=1).stderr)
        self.assertFalse(list(self.home.iterdir()))
        self.run_install('--destino', expected=2)
        self.run_install('--agente', 'outro', expected=2)
        self.run_install('--em', self.home, expected=2)
        self.run_install('--projeto', '../skills', expected=1)

    def test_git_dubious_ownership_fails_closed(self):
        self.make_project()
        target = self.project / '.agents/skills/exemplo'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('conteúdo versionado do usuário')
        self.git('add', '.')
        # Erro determinístico: o hook interno do Git não funciona em toda versão/CI.
        binaries = self.base / 'git ownership fixture'
        binaries.mkdir()
        (binaries / 'python3').symlink_to(sys.executable)
        git = binaries / 'git'
        git.write_text(
            '#!' + BASH + '\n'
            'if [ "$3" = rev-parse ] && [ "$4" = --show-toplevel ]; then\n'
            "  printf '%s\\n' \"fatal: detected dubious ownership in repository at '$2'\" >&2\n"
            '  exit 128\n'
            'fi\n'
            'exec ' + shlex.quote(GIT) + ' "$@"\n'
        )
        git.chmod(0o755)
        before = self.snapshot(self.project)
        result = self.run_install('--destino', target.parent, '--forcar',
                                  env={'PATH': str(binaries)}, expected=1)
        self.assertIn('dubious ownership', result.stderr)
        self.assertEqual(before, self.snapshot(self.project))

    def test_real_git_preserves_tracked_target_with_force(self):
        self.make_project()
        target = self.project / '.agents/skills/exemplo'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('conteúdo versionado do usuário')
        self.git('add', '.')
        before = self.snapshot(self.project)
        result = self.run_install('--destino', target.parent, '--forcar')
        self.assertIn('arquivo do projeto versionado; nunca substituído', result.stdout)
        self.assertEqual(before, self.snapshot(self.project))

    def test_inherited_git_paths_do_not_bypass_tracking(self):
        self.make_project()
        target = self.project / '.agents/skills/exemplo'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('conteúdo versionado do usuário')
        self.git('add', '.')
        other = self.base / 'outro repo'
        other.mkdir()
        self.git('init', '-q', cwd=other)
        before = self.snapshot(self.project)
        self.run_install('--destino', target.parent, '--forcar', env={
            'GIT_DIR': str(other / '.git'), 'GIT_WORK_TREE': str(other),
            'GIT_INDEX_FILE': str(self.base / 'outro-index'),
            'GIT_CEILING_DIRECTORIES': str(self.project),
        })
        self.assertEqual(before, self.snapshot(self.project))
        self.assertFalse((self.base / 'outro-index').exists())

    def test_unexpected_git_failure_is_not_treated_as_no_repo(self):
        binaries = self.base / 'git quebrado'
        binaries.mkdir()
        (binaries / 'python3').symlink_to(sys.executable)
        git = binaries / 'git'
        git.write_text('#!' + BASH + '\nprintf "fatal: falha simulada\\n" >&2\nexit 128\n')
        git.chmod(0o755)
        before = self.snapshot(self.home)
        self.assertIn('falha simulada', self.run_install(env={'PATH': str(binaries)}, expected=1).stderr)
        self.assertEqual(before, self.snapshot(self.home))

    def test_worktree_uses_common_git_exclude(self):
        self.make_project()
        self.git('-c', 'user.name=Teste', '-c', 'user.email=teste', 'commit', '--allow-empty', '-qm', 'fixture')
        worktree = self.base / 'worktree com espaço'
        self.git('worktree', 'add', '--detach', str(worktree), 'HEAD')
        self.run_install('--destino', worktree / '.agents/skills')
        self.assertTrue((worktree / '.agents/skills/exemplo/SKILL.md').exists())
        self.assertEqual(self.git('status', '--porcelain', cwd=worktree), '')
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.source_change()
        self.run_install('--destino', worktree / '.agents/skills')
        self.assertEqual(self.git('status', '--porcelain', cwd=worktree), '')

    def test_corrupt_exclude_link_preserves_destination(self):
        self.make_project()
        external = self.base / 'exclude externo'
        external.write_text('original')
        exclude = self.project / '.git/info/exclude'
        exclude.unlink()
        exclude.symlink_to(external)
        self.run_install('--destino', self.project / '.agents/skills', expected=1)
        self.assertEqual(external.read_text(), 'original')
        self.assertFalse((self.project / '.agents').exists())

    def test_source_parent_symlink_rejected(self):
        outside = self.base / 'projeto externo'
        shutil.move(self.repo / 'projetos/demo', outside)
        (self.repo / 'projetos/demo').symlink_to(outside)
        self.run_install('--projeto', 'demo', expected=1)
        self.assertFalse(list(self.home.iterdir()))

    def test_git_glob_names_are_literal(self):
        project = self.make_project()
        destination = project / 'skills [test] *'
        self.run_install('--destino', destination)
        self.assertEqual(self.git('status', '--porcelain'), '')
        other = project / 'skills t anything'
        other.mkdir()
        (other / 'exemplo').write_text('não pode ser ignorado')
        self.assertIn('skills t anything', self.git('status', '--porcelain'))

    def test_old_python_fails_before_loading_helper(self):
        binaries = self.base / 'python antigo'
        binaries.mkdir()
        python = binaries / 'python3'
        python.write_text('#!' + BASH + '\nif [ "$1" = -c ]; then exit 1; fi\nexit 99\n')
        python.chmod(0o755)
        before = self.snapshot(self.home)
        result = self.run_install(env={'PATH': str(binaries)}, expected=1)
        self.assertIn('requer Python 3.10', result.stderr)
        self.assertEqual(before, self.snapshot(self.home))

    def test_relative_launcher(self):
        result = subprocess.run([BASH, 'install.sh', '--agente', 'codex'], cwd=self.repo,
                                env={**os.environ, 'HOME': str(self.home)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / '.agents/skills/exemplo/SKILL.md').exists())


if __name__ == '__main__':
    unittest.main()
