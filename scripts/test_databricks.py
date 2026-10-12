"""Pinned content and opt-in packaging only; never execute vendored scripts."""
from pathlib import Path
import hashlib
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "projetos/databricks/skills"


class DatabricksPackageTests(unittest.TestCase):
    def test_pinned_manifest_and_complete_notices(self):
        lines = (ROOT / "licencas/databricks-agent-skills-SHA256SUMS").read_text().splitlines()
        entries = [line for line in lines if line and not line.startswith("#")]
        self.assertEqual(len(entries), 423)
        self.assertEqual(len(list(PACKAGE.glob("*/SKILL.md"))), 34)
        covered = set()
        for line in entries:
            expected, relative = line.split("  ", 1)
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertFalse(path.is_symlink(), relative)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected, relative)
            covered.add(path)
        self.assertEqual({p for p in PACKAGE.rglob("*") if p.is_file()},
                         {p for p in covered if PACKAGE in p.parents})

    def test_both_agent_targets_keep_license_and_remain_opt_in(self):
        with tempfile.TemporaryDirectory(prefix="databricks fixture ") as temp:
            home = Path(temp) / "home"
            project = Path(temp) / "project with spaces"
            home.mkdir()
            project.mkdir()
            env = {**os.environ, "HOME": str(home)}
            result = subprocess.run(["bash", str(ROOT / "install.sh")], env=env,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for prefix in (".claude", ".agents"):
                self.assertFalse(any((home / prefix / "skills").glob("databricks-*")))
            result = subprocess.run(["bash", str(ROOT / "install.sh"), "--projeto", "databricks",
                                     "--em", str(project), "--agente", "ambos"],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for prefix in (".claude", ".agents"):
                installed = list((project / prefix / "skills").glob("databricks-*"))
                self.assertEqual(len(installed), 34)
                for folder in installed:
                    for notice in ("LICENSE", "NOTICE"):
                        central = ROOT / "licencas" / f"databricks-agent-skills-{notice}"
                        self.assertEqual((folder / notice).read_bytes(), central.read_bytes())
            self.assertFalse((project / ".claude/commands").exists())


if __name__ == "__main__":
    unittest.main()
