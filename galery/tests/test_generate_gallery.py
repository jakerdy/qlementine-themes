from __future__ import annotations

import sys
import unittest
from pathlib import Path

from jakerdy.qlementine_themes import ThemeId, available_themes

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generate_gallery import DEFAULT_IMAGE_DIR, REPO_ROOT, resolve_themes, screenshot_jobs


class GenerateGalleryTests(unittest.TestCase):
    def test_screenshot_jobs_cover_every_available_theme(self) -> None:
        jobs = screenshot_jobs()

        self.assertEqual(tuple(job.theme_id for job in jobs), available_themes())
        self.assertTrue(all(job.output_path.parent == DEFAULT_IMAGE_DIR for job in jobs))

    def test_screenshot_jobs_use_expected_relative_paths(self) -> None:
        jobs = screenshot_jobs()

        self.assertEqual(jobs[0].relative_path, Path("galery") / "img" / f"{jobs[0].theme_id.value}.png")
        self.assertEqual(jobs[-1].relative_path, Path("galery") / "img" / f"{jobs[-1].theme_id.value}.png")

    def test_resolve_themes_validates_theme_names(self) -> None:
        self.assertEqual(resolve_themes(["dark", "light"]), (ThemeId.DARK, ThemeId.LIGHT))

        with self.assertRaises(ValueError):
            resolve_themes(["missing"])

    def test_repository_root_points_at_checkout(self) -> None:
        self.assertTrue((REPO_ROOT / "README.md").is_file())
        self.assertEqual(REPO_ROOT.name, "qlementine-themes")

    def test_readme_contains_embedded_gallery_images(self) -> None:
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("| Theme | Style | Description | `<img>` |", readme_text)
        for job in screenshot_jobs():
            self.assertIn(f'<img src="{job.relative_path.as_posix()}"', readme_text)


if __name__ == "__main__":
    unittest.main()
