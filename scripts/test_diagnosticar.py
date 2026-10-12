"""Read-only diagnostics tested against temporary installations, never the real HOME."""
from pathlib import Path
import json
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIAG = ROOT / "skills/diagnosticar-skills/scripts/diagnosticar.py"


def snapshot(root):
    return {str(p.relative_to(root)): (p.lstat().st_mode, p.read_bytes() if p.is_file() else None)
            for p in root.rglob("*")}


class DiagnosticTests(unittest.TestCase):
    def test_missing_and_equal_and_local_are_read_only(self):
        with tempfile.TemporaryDirectory(prefix="diagnostico com espaços ") as temp:
            home = Path(temp)
            target = home / "skills"
            command = ["python3", str(DIAG), "--repo", str(ROOT), "--destino", str(target), "--json"]
            env = {**os.environ, "HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1"}
            before = snapshot(home)
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(all(row["estado"] == "ausente" for row in json.loads(result.stdout)["itens"]))
            self.assertEqual(before, snapshot(home))
            install = subprocess.run(["bash", str(ROOT / "install.sh"), "--destino", str(target)],
                                     env=env, capture_output=True, text=True)
            self.assertEqual(install.returncode, 0, install.stderr)
            before = snapshot(home)
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(all(row["estado"] == "igual" for row in json.loads(result.stdout)["itens"]))
            self.assertEqual(before, snapshot(home))
            skill = target / "diagnosticar-skills/SKILL.md"
            skill.write_text(skill.read_text() + "\nLocal adjustment\n")
            before = snapshot(home)
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            rows = json.loads(result.stdout)["itens"]
            row = next(row for row in rows if row["skill"] == "diagnosticar-skills")
            self.assertEqual(row["estado"], "edicao-local")
            self.assertEqual(before, snapshot(home))

    def test_unknown_provenance_and_corrupt_manifest_are_not_silent(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            target = home / "skills"
            item = target / "diagnosticar-skills"
            item.mkdir(parents=True)
            (item / "SKILL.md").write_text("An unmanaged local skill")
            command = ["python3", str(DIAG), "--repo", str(ROOT), "--destino", str(target), "--json"]
            before = snapshot(home)
            result = subprocess.run(command, capture_output=True, text=True)
            row = next(row for row in json.loads(result.stdout)["itens"]
                       if row.get("skill") == "diagnosticar-skills")
            self.assertEqual(row["estado"], "divergente-sem-proveniencia")
            self.assertEqual(before, snapshot(home))
            manifest = home / ".agent-skills-skills/manifest.json"
            manifest.parent.mkdir()
            manifest.write_text("{invalid")
            before = snapshot(home)
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertTrue(any(row["estado"] == "erro-leitura" for row in json.loads(result.stdout)["itens"]))
            self.assertEqual(before, snapshot(home))

    def test_rejects_path_traversal(self):
        result = subprocess.run(["python3", str(DIAG), "--repo", str(ROOT), "--projeto", "../../skills"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
