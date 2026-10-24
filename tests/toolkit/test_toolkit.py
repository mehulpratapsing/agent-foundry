from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_adapters
import verify_toolkit


class ToolkitTests(unittest.TestCase):
    def test_complete_protocol_has_required_sections_and_fits_codex_budget(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertLess((ROOT / "AGENTS.md").stat().st_size, 32 * 1024)
        for heading in (
            "# 1. THE PRIMARY DIRECTIVE",
            "# 2. INTERPRET THE REQUEST",
            "# 3. PREFLIGHT: UNDERSTAND THE ENVIRONMENT",
            "# 4. SELECT TOOLS INTELLIGENTLY",
            "# 5. RESEARCH BEFORE IMPLEMENTATION",
            "# 6. CHOOSE THE RIGHT EXECUTION MODE",
            "# 7. ARCHITECTURE AND PLANNING",
            "# 8. IMPLEMENT THE REAL SOLUTION",
            "# 9. GIT, FILES, AND CHANGE MANAGEMENT",
            "# 10. TEST-DRIVEN VERIFICATION",
            "# 11. SECURITY AND TRUST BOUNDARIES",
            "# 12. PERFORMANCE, COST, AND CONTEXT EFFICIENCY",
            "# 13. ITERATE UNTIL THE ACCEPTANCE CRITERIA ARE MET",
            "# 14. DOCUMENTATION AND REPRODUCIBILITY",
            "# 15. FINAL ACCEPTANCE GATE",
            "# 16. REQUIRED FINAL RESPONSE",
            "# 17. NON-NEGOTIABLE BEHAVIOR",
        ):
            self.assertIn(heading, agents)
        self.assertIn("# 17. NON-NEGOTIABLE BEHAVIOR", agents)
        self.assertIn("# START EXECUTION", agents)

    def test_profiles_remain_selective_and_base_enables_context7_only(self) -> None:
        manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["sources"]), 11)
        base = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertEqual(set(base["mcp"]), {"context7"})
        self.assertNotIn("skills", base)
        profiles = {path.stem for path in (ROOT / "profiles").glob("*.json")}
        self.assertEqual(profiles, {"ecc", "gstack", "memory", "research", "security", "superpowers"})

    def test_generated_adapters_are_current_and_full_copies_match(self) -> None:
        rendered = generate_adapters.expected_files()
        generate_adapters.validate_rendered(rendered)
        for path, expected in rendered.items():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())
                self.assertEqual(path.read_text(encoding="utf-8"), expected)
        canonical = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual((ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8"), canonical)
        self.assertEqual((ROOT / ".amazonq" / "rules" / "00-toolkit.md").read_text(encoding="utf-8"), canonical)

    def test_context7_native_templates_are_secret_free_and_secure(self) -> None:
        logical = json.loads((ROOT / "adapters" / "mcp" / "context7.json").read_text(encoding="utf-8"))
        self.assertEqual(logical["transport"], "streamable-http")
        self.assertEqual(logical["url"], "https://mcp.context7.com/mcp")
        self.assertEqual(logical["required_environment_variables"], [])
        templates = ROOT / "adapters" / "mcp" / "templates"
        json_files = list(templates.glob("*.json"))
        self.assertGreaterEqual(len(json_files), 6)
        for path in json_files:
            with self.subTest(path=path.name):
                parsed = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(parsed)
                self.assertNotRegex(path.read_text(encoding="utf-8"), verify_toolkit.SECRET_SHAPE_RE)

    def test_shared_agent_skills_are_valid_and_unique(self) -> None:
        skills = ROOT / ".agents" / "skills"
        names = []
        for folder in sorted(path for path in skills.iterdir() if path.is_dir()):
            body = (folder / "SKILL.md").read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", body.split("\n---\n", 1)[0])
            self.assertIsNotNone(match)
            self.assertEqual(match.group(1), folder.name)
            self.assertRegex(body.split("\n---\n", 1)[0], r"(?m)^description:\s*\S")
            names.append(match.group(1))
        self.assertEqual(len(names), 6)
        self.assertEqual(len(set(names)), len(names))
        for folder in skills.iterdir():
            with self.subTest(skill=folder.name):
                body = (folder / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("## Expected output", body)
                self.assertIn("## Completion check", body)

    def test_tool_discovery_is_separate_from_versioned_library_research(self) -> None:
        research = (ROOT / ".agents/skills/current-library-research/SKILL.md").read_text(
            encoding="utf-8"
        )
        discovery = (ROOT / ".agents/skills/tool-discovery/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("use `tool-discovery` instead", research)
        self.assertIn("current-library-research", discovery)
        self.assertIn("GitHub Trending", discovery)


if __name__ == "__main__":
    unittest.main()
