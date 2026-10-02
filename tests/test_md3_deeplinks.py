from pathlib import Path
import re
import unittest
from harness import SphinxTestBase, MD3_SPECS, md3_conformance


class TestMd3Deeplinks(SphinxTestBase):
    """Verifies that all MD3 spec catalog entries deeplink to both:
    1. A specific section within our own component documentation (`components/<slug>.html#<section-id>`),
       and that the built HTML section exists and links out to the official MD3 spec deeplink.
    2. A canonical https://m3.material.io/ URL with a real #<pageContentBlockCanonId> section anchor.
    """

    @md3_conformance(spec_key="COMPONENTS_CUSTOM_ELEMENTS")
    def test_all_catalog_entries_contain_valid_m3_urls_and_component_doc_deeplinks(self):
        """Verifies that every spec in MD3_SPECS has valid m3.material.io and component doc deeplinks."""
        self.assertGreaterEqual(len(MD3_SPECS), 54, "Expected at least 54 canonical MD3 spec entries")
        uuid_anchor_re = re.compile(
            r"^https://m3\.material\.io/[a-z0-9/-]+#[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        )
        doc_url_re = re.compile(r"^components/[a-z0-9-]+\.html#[a-z0-9-]+$")

        for key, entry in MD3_SPECS.items():
            url = entry.get("url", "")
            section = entry.get("section", "")
            req = entry.get("requirement", "")
            doc_url = entry.get("doc_url", "")
            doc_section = entry.get("doc_section", "")

            self.assertRegex(
                url,
                uuid_anchor_re,
                f"Spec key {key} must have a canonical https://m3.material.io/<route>#<uuid> deeplink, got: {url}",
            )
            self.assertRegex(
                doc_url,
                doc_url_re,
                f"Spec key {key} must have a component doc deeplink components/<slug>.html#<section-id>, got: {doc_url}",
            )
            self.assertTrue(bool(section.strip()), f"Spec key {key} must have a non-empty section name")
            self.assertTrue(bool(doc_section.strip()), f"Spec key {key} must have a non-empty doc_section name")
            self.assertTrue(bool(req.strip()), f"Spec key {key} must have a non-empty requirement explanation")

    def test_built_component_docs_contain_all_target_sections_and_m3_deeplinks(self):
        """Verifies that every component doc deeplink in MD3_SPECS resolves to an actual
        <section id="..."> in the built //docs HTML and that the section contains the
        corresponding https://m3.material.io/ deeplink.
        """
        docs_html_root = Path(__file__).parent.parent / "docs" / "docs" / "_build" / "html"
        self.assertTrue(
            docs_html_root.is_dir(),
            f"Expected built docs directory at {docs_html_root}",
        )

        for key, entry in MD3_SPECS.items():
            doc_url = entry["doc_url"]
            m3_url = entry["url"]
            rel_path, section_id = doc_url.split("#", 1)
            html_file = docs_html_root / rel_path

            self.assertTrue(
                html_file.is_file(),
                f"Component doc file for {key} ({rel_path}) does not exist at {html_file}",
            )
            html_text = html_file.read_text(encoding="utf-8")

            section_pattern = re.compile(
                rf'<section\s+[^>]*id="{re.escape(section_id)}"[^>]*>(.*?)</section>',
                re.DOTALL,
            )
            match = section_pattern.search(html_text)
            self.assertIsNotNone(
                match,
                f"Component doc {rel_path} is missing <section id=\"{section_id}\"> required by {key}",
            )

            section_html = match.group(1)
            self.assertIn(
                f'href="{m3_url}"',
                section_html,
                f"Section #{section_id} in {rel_path} (for {key}) must contain a deeplink to {m3_url}",
            )

    def test_assertion_failure_enriches_error_with_spec_and_component_doc_details(self):
        """Verifies that when an assertion fails inside md3_conformance or spec_context,
        the raised AssertionError contains both the component doc deeplink and the MD3 spec deeplink.
        """
        spec_url = "https://m3.material.io/components/buttons/specs#73044a63-dc51-4401-bd4d-318920738ab3"
        spec_sec = "Components > Buttons > Specs > Measurements & Corner sizes"
        spec_req = "Buttons must be 32px height in compact layouts."
        doc_url = "components/buttons.html#compact-button-sizing"
        doc_sec = "Components > Buttons > Compact Button Sizing"

        @md3_conformance(
            url=spec_url,
            section=spec_sec,
            requirement=spec_req,
            doc_url=doc_url,
            doc_section=doc_sec,
        )
        def failing_test_fn():
            self.assertEqual(48, 32, "Height did not match compact spec")

        with self.assertRaises(AssertionError) as ctx:
            failing_test_fn()

        err_text = str(ctx.exception)
        self.assertIn("Height did not match compact spec", err_text)
        self.assertIn("MATERIAL DESIGN 3 (MD3) SPECIFICATION CONFORMANCE FAILURE", err_text)
        self.assertIn(doc_url, err_text)
        self.assertIn(doc_sec, err_text)
        self.assertIn(spec_url, err_text)
        self.assertIn(spec_sec, err_text)
        self.assertIn(spec_req, err_text)

    def test_spec_context_block_failure_enriches_error_with_component_doc_link(self):
        """Verifies that with self.spec_context(...) attaches both the component doc deeplink and MD3 spec deeplink."""
        with self.assertRaises(AssertionError) as ctx:
            with self.spec_context(spec_key="COLOR_SURFACE_CONTAINERS"):
                self.assertEqual("active", "inactive", "State mismatch")

        err_text = str(ctx.exception)
        self.assertIn("State mismatch", err_text)
        self.assertIn("components/color.html#surface-container-roles", err_text)
        self.assertIn("Components > Color System & Tokens > Surface Container Roles", err_text)
        self.assertIn(
            "https://m3.material.io/styles/color/roles#1950f337-a1cb-4ebf-9d84-e0643d99c578",
            err_text,
        )
        self.assertIn("Surface container roles", err_text)

    def test_unknown_spec_key_raises_key_error(self):
        """Verifies that an invalid spec_key raises KeyError immediately rather than silently dropping the deeplink."""
        with self.assertRaises(KeyError):
            with self.spec_context(spec_key="NON_EXISTENT_SPEC_KEY"):
                pass


if __name__ == "__main__":
    unittest.main()
