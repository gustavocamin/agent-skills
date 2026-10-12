"""Structural regressions for first-party portable skills; not a runtime-agent claim."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NEW = [ROOT / "skills" / name for name in (
    "tutor-databricks", "mapa-projeto-tech-lead", "revisar-qualidade-dados", "diagnosticar-skills", "revisar-decisao-de-compra")]
NEW += [ROOT / "projetos/obsidian/skills" / name for name in ("study-loop", "comms-check", "exec-sim")]


class SkillStructureTests(unittest.TestCase):
    def test_frontmatter_and_local_references(self):
        for folder in NEW:
            with self.subTest(skill=folder.name):
                text = (folder / "SKILL.md").read_text()
                self.assertTrue(text.startswith("---\n"))
                front = text.split("---", 2)[1]
                name = re.search(r"^name:\s*(.+)$", front, re.M)
                self.assertIsNotNone(name)
                self.assertEqual(name[1].strip("\"'"), folder.name)
                desc = re.search(r"^description:\s*(.+)$", front, re.M)
                self.assertIsNotNone(desc)
                self.assertLessEqual(len(desc[1]), 1024)
                self.assertLess(len(text.splitlines()), 150)
                for file in folder.rglob("*.md"):
                    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", file.read_text()):
                        if "://" in target or target.startswith("#"):
                            continue
                        self.assertTrue((file.parent / target.split("#")[0]).exists(),
                                        f"broken reference {file}: {target}")

    def test_claude_commands_are_thin_adapters(self):
        for name in ("study-loop", "comms-check", "exec-sim"):
            text = (ROOT / "projetos/obsidian/commands" / f"{name}.md").read_text()
            self.assertLess(len(text.splitlines()), 35)
            self.assertIn(name, text)
            self.assertNotRegex(text, r"2026|2027|20[–-]24|30/10|02/11")

    def test_no_fixed_personal_calendar_in_portable_workflows(self):
        for folder in NEW:
            for file in folder.rglob("*.md"):
                self.assertNotRegex(file.read_text(), r"Gustavo|PDI do|22[–-]28/09/2026|2026-11-02")

    def test_conversation_mode_keeps_one_canonical_skill(self):
        skill = ROOT / "projetos/obsidian/skills/exec-sim/SKILL.md"
        wrapper = ROOT / "projetos/obsidian/commands/exec-sim.md"
        skill_description = re.search(r"^description: (.+)$", skill.read_text(), re.M)[1]
        wrapper_description = re.search(r"^description: (.+)$", wrapper.read_text(), re.M)[1]
        self.assertEqual(skill_description, wrapper_description)
        self.assertTrue((skill.parent / "references/conversa-dificil.md").is_file())
        self.assertFalse((ROOT / "skills/ensaiar-conversa-dificil").exists())
        self.assertFalse((skill.parent.parent / "ensaiar-conversa-dificil").exists())

    def test_mac_measurement_refuses_other_platforms(self):
        import platform
        import subprocess
        if platform.system() == "Darwin":
            self.skipTest("non-macOS negative case")
        result = subprocess.run(["bash", str(ROOT / "skills/liberar-disco/scripts/medir.sh")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("macOS", result.stderr)


if __name__ == "__main__":
    unittest.main()
