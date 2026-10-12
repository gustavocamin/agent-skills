"""A sincronização não pode transformar cópias locais em atualizações upstream."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BASH = shutil.which('bash')


class SynchronizationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='agent-skills-sync-test-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / 'repo'
        (self.repo / 'scripts').mkdir(parents=True)
        shutil.copy2(ROOT / 'scripts/sincronizar.sh', self.repo / 'scripts/sincronizar.sh')
        (self.repo / 'TERCEIROS.md').write_text('| `upstream-skill` | origem fixada |\n')
        self.original = self.repo / 'projetos/databricks/skills/upstream-skill/SKILL.md'
        self.original.parent.mkdir(parents=True)
        self.original.write_text('original upstream')
        (self.repo / 'projetos/databricks/ORIGEM.json').write_text('{"commit": "fixado"}')
        self.home = self.base / 'home'
        self.home.mkdir()
        self.source = self.base / 'fonte'
        (self.source / '.claude/skills/upstream-skill').mkdir(parents=True)
        (self.source / '.claude/skills/upstream-skill/SKILL.md').write_text('edição local')
        # PATH realista mínimo sem rsync: a proteção deve ocorrer antes de usá-lo.
        self.binaries = self.base / 'bin'
        self.binaries.mkdir()
        for name in ('dirname', 'sed', 'grep', 'basename', 'mkdir', 'python3'):
            (self.binaries / name).symlink_to(shutil.which(name))

    def snapshot(self):
        return {str(path.relative_to(self.repo)): path.read_bytes() if path.is_file() else None
                for path in self.repo.rglob('*')}

    def reject(self, *args):
        before = self.snapshot()
        result = subprocess.run([BASH, str(self.repo / 'scripts/sincronizar.sh'), *map(str, args)],
                                env={**os.environ, 'HOME': str(self.home), 'PATH': str(self.binaries)},
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('rsync', result.stderr)
        self.assertEqual(before, self.snapshot())
        return result.stderr

    def test_whole_databricks_project_is_protected(self):
        self.assertIn('terceiros', self.reject('--projeto', 'databricks', self.source))

    def test_new_skill_cannot_replace_third_party(self):
        origin = self.source / '.claude/skills/upstream-skill'
        self.assertIn('terceiros', self.reject('--nova', origin))
        self.assertIn('terceiros', self.reject('--nova', origin, '--projeto', 'databricks'))

    def test_copy_guard_protects_upstream_in_any_project(self):
        target = self.repo / 'projetos/outro/skills/upstream-skill'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('também upstream')
        self.assertIn('terceiros', self.reject('--projeto', 'outro', self.source))

    def own_skill(self):
        source = self.base / 'minha-skill'
        source.mkdir()
        (source / 'SKILL.md').write_text('minha skill')
        return source

    def test_new_skill_source_symlink_rejected(self):
        source = self.own_skill()
        link = self.base / 'skill-link'
        link.symlink_to(source)
        self.assertIn('link simbólico', self.reject('--nova', link))
        self.assertEqual((source / 'SKILL.md').read_text(), 'minha skill')

    def test_new_skill_target_symlink_rejected(self):
        source = self.own_skill()
        external = self.base / 'fora'
        external.mkdir()
        (external / 'SKILL.md').write_text('intacto')
        (self.repo / 'skills').mkdir()
        (self.repo / 'skills/minha-skill').symlink_to(external)
        self.assertIn('link simbólico', self.reject('--nova', source))
        self.assertEqual((external / 'SKILL.md').read_text(), 'intacto')

    def test_source_and_target_ancestor_symlinks_rejected(self):
        source = self.own_skill()
        source_parent = self.base / 'fonte-link'
        source_parent.symlink_to(self.base)
        self.assertIn('link simbólico', self.reject('--nova', source_parent / source.name))
        outside = self.base / 'destino-externo'
        outside.mkdir()
        (self.repo / 'skills').symlink_to(outside)
        self.assertIn('link simbólico', self.reject('--nova', source))
        self.assertFalse(list(outside.iterdir()))

    def test_nested_symlinks_do_not_import_or_overwrite_external_data(self):
        source = self.own_skill()
        external = self.base / 'segredo'
        external.write_text('intacto')
        (source / 'escape').symlink_to(external)
        self.assertIn('link simbólico', self.reject('--nova', source))
        (source / 'escape').unlink()
        target = self.repo / 'skills/minha-skill'
        target.mkdir(parents=True)
        (target / 'escape').symlink_to(external)
        self.assertIn('link simbólico', self.reject('--nova', source))
        self.assertEqual(external.read_text(), 'intacto')

    def test_project_traversal_and_databricks_new_are_rejected(self):
        self.assertIn('inválido', self.reject('--projeto', '../fora', self.source))
        own = self.base / 'minha-skill'
        own.mkdir()
        (own / 'SKILL.md').write_text('minha')
        self.assertIn('inválido', self.reject('--nova', own, '--projeto', '../fora'))
        self.assertIn('terceiros', self.reject('--nova', own, '--projeto', 'databricks'))


if __name__ == '__main__':
    unittest.main()
