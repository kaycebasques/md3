from pathlib import Path
import re
import unittest

from harness import (
    REF_TOKENS,
    SYS_TOKENS,
    DocsServer,
    build_docs,
    run_playwright,
)
import md3

DOCS_URL = "md3.html#tokens"
DOCS_COMPLIANCE_URL = "dev/test.html#md3-compliance"
MD3_TOKENS_URL = "https://m3.material.io/foundations/design-tokens/overview"


class TokensTest(unittest.TestCase):
    def test_md3(self):
        files = {
            "conf.py": """
                project = "test_md3"
                extensions = ["md3"]
                html_theme = "md3"
            """,
            "index.rst": """
                ========
                test_md3
                ========
            """,
        }
        token_names = list(REF_TOKENS.keys()) + list(SYS_TOKENS.keys())
        spec_ref = f"See {DOCS_URL} and {MD3_TOKENS_URL}"
        with build_docs(files) as outdir:
            html = (outdir / "index.html").read_text()
            self.assertIn("_static/ref.css", html, spec_ref)
            self.assertIn("_static/sys.css", html, spec_ref)

            with DocsServer(outdir) as server:
                with run_playwright() as page:
                    page.goto(server.url_for("index.html"))
                    resolved = page.evaluate(
                        """(names) => {
                            const cs = window.getComputedStyle(document.documentElement);
                            const out = {};
                            for (const name of names) {
                                out[name] = cs.getPropertyValue(name).trim();
                            }
                            return out;
                        }""",
                        token_names,
                    )
                    for name, expected in REF_TOKENS.items():
                        self.assertEqual(resolved[name], expected, f"{name}: {spec_ref}")
                    for name, expected in SYS_TOKENS.items():
                        self.assertEqual(resolved[name], expected, f"{name}: {spec_ref}")

    def test_unused(self):
        package_dir = Path(md3.__file__).resolve().parent
        ref_css = (package_dir / "tokens" / "ref.css").read_text()
        sys_css = (package_dir / "tokens" / "sys.css").read_text()
        comp_css = "\n".join(
            path.read_text()
            for path in sorted((package_dir / "components").glob("**/*.css"))
        )

        ref_declared = re.findall(r"(--[a-z0-9-]+)\s*:", ref_css)
        sys_declared = re.findall(r"(--[a-z0-9-]+)\s*:", sys_css)
        spec_ref = f"See {DOCS_URL} and {MD3_TOKENS_URL}"

        self.assertEqual(set(ref_declared), set(REF_TOKENS.keys()), spec_ref)
        self.assertEqual(set(sys_declared), set(SYS_TOKENS.keys()), spec_ref)

        for token in ref_declared:
            self.assertTrue(
                token.startswith("--md-ref-"),
                f"{token} must start with --md-ref-. {spec_ref}",
            )
            self.assertIn(
                f"var({token})",
                sys_css,
                f"Unused reference token {token} in ref.css. {spec_ref}",
            )

        for token in sys_declared:
            self.assertTrue(
                token.startswith("--md-sys-"),
                f"{token} must start with --md-sys-. {spec_ref}",
            )
            self.assertIn(
                f"var({token})",
                comp_css,
                f"Unused system token {token} in sys.css. {spec_ref}",
            )

    def test_component_css(self):
        package_dir = Path(md3.__file__).resolve().parent
        spec_ref = f"See {DOCS_URL} and {MD3_TOKENS_URL}"
        comp_files = sorted((package_dir / "components").glob("**/*.css"))
        self.assertTrue(comp_files, spec_ref)

        for css_path in comp_files:
            rel_path = css_path.relative_to(package_dir)
            content = css_path.read_text()
            self.assertNotIn(
                ":root",
                content,
                f"{rel_path} must not declare :root tokens. {spec_ref}",
            )
            custom_props = re.findall(r"(--[a-zA-Z0-9-]+)\s*:", content)
            self.assertEqual(
                custom_props,
                [],
                f"{rel_path} must not define custom properties {custom_props}. {spec_ref}",
            )
            used_vars = set(re.findall(r"var\((--[a-zA-Z0-9-]+)\)", content))
            unknown_vars = used_vars - set(SYS_TOKENS.keys()) - {"--md3-density"}
            self.assertEqual(
                unknown_vars,
                set(),
                f"{rel_path} references unknown CSS variables {sorted(unknown_vars)}. {spec_ref}",
            )
            raw_colors = re.findall(
                r"#[0-9a-fA-F]{3,8}\b|\b(?:rgb|rgba|hsl|hsla)\(",
                content,
            )
            self.assertEqual(
                raw_colors,
                [],
                f"{rel_path} must use --md-sys-color-* tokens instead of {raw_colors}. {spec_ref}",
            )

    def test_doc_links(self):
        tests_dir = Path(__file__).parent
        docs_html_dir = Path.cwd() / "docs" / "docs" / "_build" / "html"
        self.assertTrue(docs_html_dir.is_dir(), f"See {DOCS_COMPLIANCE_URL}")

        url_assignments = []
        for test_file in sorted(tests_dir.glob("*_test.py")):
            matches = re.findall(
                r'^(DOCS[A-Z0-9_]*_URL)\s*=\s*"([^"]+)"',
                test_file.read_text(),
                 flags=re.MULTILINE,
            )
            for name, url in matches:
                url_assignments.append((test_file.name, name, url))

        self.assertTrue(url_assignments, f"See {DOCS_COMPLIANCE_URL}")
        for filename, const_name, url in url_assignments:
            path_part, _, fragment = url.partition("#")
            target_file = docs_html_dir / path_part
            self.assertTrue(
                target_file.is_file(),
                f"{filename}:{const_name} references missing doc page {path_part!r}. See {DOCS_COMPLIANCE_URL}",
            )
            if fragment:
                html = target_file.read_text()
                self.assertIn(
                    f'id="{fragment}"',
                    html,
                    f"{filename}:{const_name} references missing anchor #{fragment} in {path_part!r}. See {DOCS_COMPLIANCE_URL}",
                )


if __name__ == "__main__":
    unittest.main()
