import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "productivity" / "say-hello"
GREETING = "नमस्ते! तपाईंलाई हार्दिक अभिवादन।"


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
        self.assertEqual(manifest["version"], "0.1.0")
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
        self.assertEqual(
            manifest["skills"], ["./skills/productivity/say-hello"]
        )
        self.assertEqual(marketplace["plugins"][0]["source"], "./")

    def test_readme_documents_all_installers(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills@latest add abhiyanhaze/hazeship", content)
        self.assertIn("claude plugin marketplace add abhiyanhaze/hazeship", content)
        self.assertIn("claude plugin install hazeship@abhiyanhaze", content)
        self.assertIn("codex plugin marketplace add abhiyanhaze/hazeship", content)
        self.assertIn("codex plugin add hazeship@hazeship", content)


if __name__ == "__main__":
    unittest.main()
