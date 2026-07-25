import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "productivity" / "say-hello"
GREETING = "नमस्ते! तपाईंलाई हार्दिक अभिवादन।"

RESOLVER = (
    ROOT
    / "skills"
    / "sdlc"
    / "persistent-memory"
    / "scripts"
    / "resolve-memory-root.sh"
)

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
    "commit-pr",
    "persistent-memory",
    "ssh-readonly-investigation",
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
    "./skills/sdlc/commit-pr",
    "./skills/sdlc/persistent-memory",
    "./skills/sdlc/ssh-readonly-investigation",
]

SHARED = ROOT / "skills" / "sdlc" / "_shared"

TEMPLATES = [
    "manifest.yaml",
    "gap-analysis.md",
    "tech-design.md",
    "dev-plan.md",
    "slice-log.md",
    "validation.md",
    "retro.md",
    "team-handoff.md",
    "technical-doc.md",
]

SHARED_DOCS = [
    "handoff-format.md",
    "branch-commit-conventions.md",
    "repo-map.template.md",
    "workspace-setup.md",
]

# Skills that call tools/sdlc or read docs/templates cannot work in a project
# that hasn't been bootstrapped, so each must point the reader at the setup
# doc — directly, or via handoff-format.md which carries it in §0.
BOOTSTRAP_POINTERS = ("workspace-setup", "handoff-format")

FORBIDDEN_TERMS = ("Sensor", "PHI", "HIPAA")

# Vocabulary from the regulated project this kit was ported out of. The kit
# is stack- and domain-agnostic: data-handling rules come from the project's
# own repo-map, not from a compliance checklist baked into the skills.
FORBIDDEN_PHRASES = (
    "compliance",
    "project's own compliance",
    "Mock/README.md",
    "factory_boy",
)


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
        self.assertEqual(manifest["version"], "0.3.0")
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
            "https://github.com/abhiyan52/hazeship.git",
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
        self.assertEqual(manifest["version"], "0.3.0")
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

    def test_sdlc_skills_have_no_forbidden_phrases(self):
        sdlc_dir = ROOT / "skills" / "sdlc"
        files = list(sdlc_dir.rglob("*.md")) + list(sdlc_dir.rglob("*.yaml"))
        offenders = []
        for path in files:
            content = path.read_text(encoding="utf-8").lower()
            for phrase in FORBIDDEN_PHRASES:
                if phrase.lower() in content:
                    offenders.append((str(path.relative_to(ROOT)), phrase))
        self.assertEqual(
            offenders,
            [],
            f"project-specific phrasing found: {offenders}",
        )

    def test_shared_docs_exist(self):
        for name in SHARED_DOCS:
            with self.subTest(doc=name):
                self.assertTrue(
                    (SHARED / name).is_file(), f"{SHARED / name} does not exist"
                )

    def test_templates_ship(self):
        for name in TEMPLATES:
            path = SHARED / "templates" / name
            with self.subTest(template=name):
                self.assertTrue(path.is_file(), f"{path} does not exist")
                self.assertTrue(
                    path.read_text(encoding="utf-8").strip(),
                    f"{path} is empty",
                )

    def test_manifest_template_is_valid_yaml_in_the_starting_state(self):
        try:
            import yaml
        except ModuleNotFoundError:
            self.skipTest("PyYAML not installed")
        data = yaml.safe_load(
            (SHARED / "templates" / "manifest.yaml").read_text(encoding="utf-8")
        )
        # tools/sdlc refuses to touch a manifest it can't validate, so the
        # template has to start in a state the state machine accepts.
        self.assertEqual(data["stage"], "intake")
        self.assertEqual(data["gate"], "in-progress")
        self.assertEqual(data["revision"], 1)
        for key in ("feature", "title", "slices", "approvals", "handoffs"):
            self.assertIn(key, data)

    def test_shipped_tools_are_executable(self):
        for name in ("sdlc", "build-docx.sh"):
            path = SHARED / "tools" / name
            with self.subTest(tool=name):
                self.assertTrue(path.is_file(), f"{path} does not exist")
                self.assertTrue(
                    path.stat().st_mode & 0o111, f"{path} is not executable"
                )

    def test_sdlc_cli_runs_and_exposes_its_commands(self):
        result = subprocess.run(
            [sys.executable, str(SHARED / "tools" / "sdlc"), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("show", "validate", "transition", "gate", "approve", "slice"):
            with self.subTest(command=command):
                self.assertIn(command, result.stdout)

    def test_sdlc_cli_drives_a_feature_through_the_whole_loop(self):
        """The shipped CLI and the shipped manifest template, end to end.

        Covers the gates that make the loop trustworthy: a stage cannot
        advance without a recorded approval, `approved` cannot be set by
        hand, and validation cannot start with an unmerged slice.
        """
        try:
            import yaml
        except ModuleNotFoundError:
            self.skipTest("PyYAML not installed")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature = root / "docs" / "features" / "demo"
            feature.mkdir(parents=True)
            (root / "tools").mkdir()
            shutil.copy(SHARED / "tools" / "sdlc", root / "tools" / "sdlc")

            template = (SHARED / "templates" / "manifest.yaml").read_text(
                encoding="utf-8"
            )
            (feature / "manifest.yaml").write_text(
                template.replace("<feature-slug>", "demo").replace(
                    "<human-readable title>", "Demo feature"
                ),
                encoding="utf-8",
            )
            for name in (
                "01-gap-analysis.md",
                "02-tech-design.md",
                "03-dev-plan.md",
                "04-validation.md",
                "05-retro.md",
            ):
                (feature / name).write_text("placeholder\n", encoding="utf-8")

            for args in (
                ["init", "-q"],
                ["config", "user.email", "dev@example.com"],
                ["config", "user.name", "Dev"],
                ["add", "-A"],
                ["commit", "-qm", "init"],
            ):
                subprocess.run(["git", *args], cwd=root, check=True)

            def sdlc(*args):
                return subprocess.run(
                    [sys.executable, "tools/sdlc", *args],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )

            def ok(*args):
                result = sdlc(*args)
                self.assertEqual(result.returncode, 0, f"{args}: {result.stderr}")

            def refused(*args):
                result = sdlc(*args)
                self.assertNotEqual(result.returncode, 0, f"{args} should have failed")

            ok("validate", "demo")
            # No approval recorded yet, so the stage cannot advance.
            refused("transition", "demo", "tech-design")
            refused("gate", "demo", "approved")

            def approve_stage(*extra):
                ok("gate", "demo", "awaiting-approval")
                ok("approve", "demo", *extra)

            approve_stage()
            ok("transition", "demo", "tech-design")
            approve_stage()
            ok("transition", "demo", "dev-plan")
            approve_stage()
            ok("transition", "demo", "implement")

            ok("slice", "demo", "01", "in-progress")
            # Slice 01 is still open, so 02 cannot start.
            refused("slice", "demo", "02", "in-progress")
            # An unmerged slice blocks validation.
            refused("transition", "demo", "validate")
            ok("slice", "demo", "01", "awaiting-user-test")
            ok("slice", "demo", "01", "user-approved")
            refused("slice", "demo", "01", "pr-raised")  # needs --pr
            ok("slice", "demo", "01", "pr-raised", "--pr", "https://example.com/pr/1")
            ok("slice", "demo", "01", "merged")

            ok("transition", "demo", "validate")
            approve_stage()
            ok("transition", "demo", "final-pr")
            approve_stage("--artifact", "04-validation.md")
            ok("transition", "demo", "retro")
            approve_stage()
            ok("transition", "demo", "done")
            refused("transition", "demo", "done")  # terminal
            ok("validate", "demo")

            final = yaml.safe_load(
                (feature / "manifest.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(final["stage"], "done")
            self.assertEqual(final["slices"]["01"]["state"], "merged")
            # Approvals are an append-only chronological record.
            self.assertEqual(
                [entry["stage"] for entry in final["approvals"]],
                ["intake", "tech-design", "dev-plan", "validate", "final-pr", "retro"],
            )
            for entry in final["approvals"]:
                self.assertEqual(entry["actor"], "dev@example.com")
                self.assertNotEqual(entry["commit"], "unknown")

    def test_skills_needing_bootstrap_point_at_it(self):
        sdlc_dir = ROOT / "skills" / "sdlc"
        for name in SDLC_SKILLS:
            content = (sdlc_dir / name / "SKILL.md").read_text(encoding="utf-8")
            if "tools/sdlc" not in content and "docs/templates" not in content:
                continue
            with self.subTest(skill=name):
                self.assertTrue(
                    any(pointer in content for pointer in BOOTSTRAP_POINTERS),
                    f"{name} uses tools/sdlc or docs/templates but never "
                    f"points the reader at the workspace bootstrap",
                )

    def test_new_skills_carry_no_source_project_details(self):
        markers = ("proptech", "doppler", "/Users/", "TTS brain")
        for name in ("persistent-memory", "ssh-readonly-investigation", "commit-pr"):
            skill_dir = ROOT / "skills" / "sdlc" / name
            for path in sorted(skill_dir.rglob("*")):
                if not path.is_file():
                    continue
                content = path.read_text(encoding="utf-8")
                for marker in markers:
                    with self.subTest(skill=name, file=path.name, marker=marker):
                        self.assertNotIn(marker.lower(), content.lower())

    def test_repo_map_template_covers_new_skills(self):
        content = (
            ROOT / "skills" / "sdlc" / "_shared" / "repo-map.template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("## Remote hosts & read-only investigation", content)
        self.assertIn("## Persistent memory store", content)
        self.assertIn("HAZESHIP_MEMORY_DIR", content)

    def test_persistent_memory_bundles_templates(self):
        templates = ROOT / "skills" / "sdlc" / "persistent-memory" / "templates"
        for filename in ("README.md", "config.yaml", "logs.md", "blueprint.md"):
            with self.subTest(template=filename):
                self.assertTrue((templates / filename).exists())
        self.assertTrue(os.access(RESOLVER, os.X_OK), f"{RESOLVER} is not executable")

    def test_commit_pr_delegates_instead_of_duplicating(self):
        content = (
            ROOT / "skills" / "sdlc" / "commit-pr" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("checkpoint", content)
        self.assertIn("raise-pr", content)
        self.assertNotIn("gh pr create --", content)


class ResolveMemoryRootTests(unittest.TestCase):
    """The store root must resolve the same way every run, not by improvisation."""

    def run_resolver(self, start, *args, env_dir=None):
        env = dict(os.environ)
        env.pop("HAZESHIP_MEMORY_DIR", None)
        if env_dir is not None:
            env["HAZESHIP_MEMORY_DIR"] = env_dir
        result = subprocess.run(
            [str(RESOLVER), "--start", str(start), "--why", *args],
            capture_output=True,
            text=True,
            env=env,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def test_env_var_wins_over_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            (tmp / ".hazeship").mkdir()
            code, out, err = self.run_resolver(tmp, env_dir=str(tmp / "elsewhere"))
            self.assertEqual(code, 0)
            self.assertEqual(out, str(tmp / "elsewhere"))
            self.assertIn("source=env", err)

    def test_nearest_marker_wins_when_walking_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            (tmp / ".hazeship").mkdir()
            nested = tmp / "packages" / "api"
            nested.mkdir(parents=True)
            (nested / ".hazeship").mkdir()
            deep = nested / "src" / "handlers"
            deep.mkdir(parents=True)

            code, out, err = self.run_resolver(deep)
            self.assertEqual(code, 0)
            self.assertEqual(out, str(nested / ".hazeship" / "memory"))
            self.assertIn("source=marker", err)

    def test_walks_up_to_the_only_marker_above(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            (tmp / ".hazeship").mkdir()
            deep = tmp / "a" / "b" / "c"
            deep.mkdir(parents=True)
            code, out, _ = self.run_resolver(deep)
            self.assertEqual(code, 0)
            self.assertEqual(out, str(tmp / ".hazeship" / "memory"))

    def test_config_env_overrides_marker_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            marker = tmp / ".hazeship"
            marker.mkdir()
            (marker / "config.env").write_text(
                "# a comment\nHAZESHIP_MEMORY_DIR = \"/shared/store\"  # inline\n",
                encoding="utf-8",
            )
            code, out, _ = self.run_resolver(tmp)
            self.assertEqual(code, 0)
            self.assertEqual(out, "/shared/store")

    def test_config_env_relative_path_resolves_against_marker_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            marker = tmp / ".hazeship"
            marker.mkdir()
            (marker / "config.env").write_text(
                "HAZESHIP_MEMORY_DIR=notes/memory\n", encoding="utf-8"
            )
            code, out, _ = self.run_resolver(tmp)
            self.assertEqual(code, 0)
            self.assertEqual(out, f"{tmp}/notes/memory")

    def test_uninitialized_proposes_repo_root_and_exits_three(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            subprocess.run(
                ["git", "init", "--quiet", str(tmp)], check=True, capture_output=True
            )
            deep = tmp / "src" / "deep"
            deep.mkdir(parents=True)

            code, out, err = self.run_resolver(deep)
            self.assertEqual(code, 3, f"expected not-initialized exit code; {err}")
            self.assertEqual(out, str(tmp / ".hazeship" / "memory"))
            self.assertIn("source=default", err)
            self.assertFalse(
                (tmp / ".hazeship").exists(), "resolving must not create the store"
            )

    def test_init_creates_marker_config_and_buckets(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            subprocess.run(
                ["git", "init", "--quiet", str(tmp)], check=True, capture_output=True
            )
            code, out, err = self.run_resolver(tmp, "--init")
            self.assertEqual(code, 0, err)
            self.assertEqual(out, str(tmp / ".hazeship" / "memory"))
            self.assertTrue((tmp / ".hazeship" / "memory" / "buckets").is_dir())
            self.assertIn(
                "HAZESHIP_MEMORY_DIR",
                (tmp / ".hazeship" / "config.env").read_text(encoding="utf-8"),
            )

            # Idempotent: a second resolve now finds the marker.
            code, out2, err2 = self.run_resolver(tmp)
            self.assertEqual(code, 0)
            self.assertEqual(out2, out)
            self.assertIn("source=marker", err2)

    def test_worktree_resolves_to_main_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp).resolve()
            main = tmp / "main"
            main.mkdir()
            git = ["git", "-C", str(main)]
            subprocess.run([*git, "init", "--quiet"], check=True, capture_output=True)
            subprocess.run(
                [*git, "config", "user.email", "test@example.com"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [*git, "config", "user.name", "Test"], check=True, capture_output=True
            )
            (main / "file.txt").write_text("hi\n", encoding="utf-8")
            subprocess.run([*git, "add", "."], check=True, capture_output=True)
            subprocess.run(
                [*git, "commit", "--quiet", "-m", "init"],
                check=True,
                capture_output=True,
            )
            wt = tmp / "wt"
            subprocess.run(
                [*git, "worktree", "add", "--quiet", str(wt), "-b", "side"],
                check=True,
                capture_output=True,
            )

            code, out, err = self.run_resolver(wt)
            self.assertEqual(code, 3, err)
            self.assertEqual(out, str(main / ".hazeship" / "memory"))

    def test_rejects_unknown_argument(self):
        code, _, err = self.run_resolver(ROOT, "--nope")
        self.assertEqual(code, 2)
        self.assertIn("unknown argument", err)


class ReadmeTests(unittest.TestCase):
    def test_readme_documents_all_installers(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills@latest add abhiyan52/hazeship", content)
        self.assertIn("claude plugin marketplace add abhiyan52/hazeship", content)
        self.assertIn("claude plugin install hazeship@abhiyan52", content)
        self.assertIn("codex plugin marketplace add abhiyan52/hazeship", content)
        self.assertIn("codex plugin add hazeship@hazeship", content)

    def test_readme_documents_memory_store_setup(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("HAZESHIP_MEMORY_DIR", content)
        self.assertIn("resolve-memory-root.sh --init", content)


if __name__ == "__main__":
    unittest.main()
