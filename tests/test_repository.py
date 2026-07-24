import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "productivity" / "say-hello"
GREETING = "नमस्ते! तपाईंलाई हार्दिक अभिवादन।"

SDLC_SKILLS = [
    "feature-intake",
    "tech-design",
    "dev-plan",
    "implement-slice",
    "validate-feature",
    "raise-pr",
    "review",
    "retro",
    "team-handoff",
    "teach",
    "to-technical-doc",
    "checkpoint",
    "qa-playwright",
    "seed-data",
]

FULL_SKILLS_ARRAY = [
    "./skills/productivity/say-hello",
    "./skills/sdlc/feature-intake",
    "./skills/sdlc/tech-design",
    "./skills/sdlc/dev-plan",
    "./skills/sdlc/implement-slice",
    "./skills/sdlc/validate-feature",
    "./skills/sdlc/raise-pr",
    "./skills/sdlc/review",
    "./skills/sdlc/retro",
    "./skills/sdlc/team-handoff",
    "./skills/sdlc/teach",
    "./skills/sdlc/to-technical-doc",
    "./skills/sdlc/checkpoint",
    "./skills/sdlc/qa-playwright",
    "./skills/sdlc/seed-data",
]

FORBIDDEN_TERMS = ("Sensor", "PHI", "HIPAA")


class HazeshipRepositoryTests(unittest.TestCase):
    def test_skill_contract(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: say-hello", content)
        self.assertIn(
            "description: Use when the user explicitly invokes /say-hello or "
            "$say-hello, or asks for the Hazeship sample Nepali greeting.",
            content,
        )
        self.assertIn(GREETING, content)
        self.assertIn("Respond with exactly this single line", content)

    def test_openai_metadata(self):
        content = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Say Hello"', content)
        self.assertIn('$say-hello', content)
        self.assertIn("allow_implicit_invocation: false", content)

    def test_codex_plugin(self):
        manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["name"], "hazeship")
        self.assertEqual(manifest["version"], "0.2.0")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_codex_marketplace(self):
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        plugin = marketplace["plugins"][0]
        self.assertEqual(marketplace["name"], "hazeship")
        self.assertEqual(plugin["name"], "hazeship")
        self.assertEqual(plugin["source"]["source"], "url")
        self.assertEqual(
            plugin["source"]["url"],
            "https://github.com/abhiyanhaze/hazeship.git",
        )

    def test_claude_plugin(self):
        manifest = json.loads(
            (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(manifest["name"], "hazeship")
        self.assertEqual(manifest["version"], "0.2.0")
        self.assertEqual(manifest["skills"], FULL_SKILLS_ARRAY)
        self.assertEqual(marketplace["plugins"][0]["source"], "./")

    def test_sdlc_skill_contracts(self):
        for name in SDLC_SKILLS:
            skill_dir = ROOT / "skills" / "sdlc" / name
            skill_md = skill_dir / "SKILL.md"
            with self.subTest(skill=name):
                self.assertTrue(
                    skill_md.exists(), f"{skill_md} does not exist"
                )
                content = skill_md.read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", content)

                match = re.search(
                    r"^description:\s*(.*)$", content, re.MULTILINE
                )
                self.assertIsNotNone(
                    match, f"{skill_md} missing description field"
                )
                description_value = match.group(1).strip()
                if description_value in ("|", ">", "|-", ">-"):
                    # Block scalar: description continues on following
                    # indented lines.
                    frontmatter_end = content.index("\n---", content.index("---") + 3)
                    frontmatter = content[: frontmatter_end]
                    desc_start = frontmatter.index("description:")
                    block = frontmatter[desc_start:]
                    lines = block.splitlines()[1:]
                    body_lines = [
                        line for line in lines if line.strip()
                    ]
                    self.assertTrue(
                        body_lines,
                        f"{skill_md} has empty description block",
                    )
                else:
                    self.assertTrue(
                        description_value,
                        f"{skill_md} has empty description field",
                    )

                openai_yaml = skill_dir / "agents" / "openai.yaml"
                self.assertTrue(
                    openai_yaml.exists(), f"{openai_yaml} does not exist"
                )

    def test_sdlc_skills_have_no_forbidden_terms(self):
        sdlc_dir = ROOT / "skills" / "sdlc"
        files = list(sdlc_dir.rglob("*.md")) + list(sdlc_dir.rglob("*.yaml"))
        self.assertTrue(files, "expected markdown/yaml files under skills/sdlc")
        offenders = []
        for path in files:
            content = path.read_text(encoding="utf-8")
            for term in FORBIDDEN_TERMS:
                if term in content:
                    offenders.append((str(path.relative_to(ROOT)), term))
        self.assertEqual(
            offenders,
            [],
            f"forbidden terms found: {offenders}",
        )

    def test_readme_documents_all_installers(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills@latest add abhiyanhaze/hazeship", content)
        self.assertIn("claude plugin marketplace add abhiyanhaze/hazeship", content)
        self.assertIn("claude plugin install hazeship@abhiyanhaze", content)
        self.assertIn("codex plugin marketplace add abhiyanhaze/hazeship", content)
        self.assertIn("codex plugin add hazeship@hazeship", content)


if __name__ == "__main__":
    unittest.main()
