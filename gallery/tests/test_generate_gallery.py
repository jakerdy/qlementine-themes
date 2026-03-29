from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TEST_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(TEST_REPO_ROOT / "python-qt" / "src"))
sys.path.append(str(TEST_REPO_ROOT / "gallery" / "src"))

from jakerdy.qlementine_themes import ThemeId, available_themes

from generate_gallery import DEFAULT_IMAGE_DIR, REPO_ROOT, jobs_to_render, parse_args, resolve_themes, screenshot_jobs

README_IMAGE_HEADER = "| Theme | Style | Description | `<img>` |"


class GenerateGalleryTests(unittest.TestCase):
    def test_screenshot_jobs_cover_every_available_theme(self) -> None:
        jobs = screenshot_jobs()

        self.assertEqual(tuple(job.theme_id for job in jobs), available_themes())
        self.assertTrue(all(job.output_path.parent == DEFAULT_IMAGE_DIR for job in jobs))

    def test_screenshot_jobs_use_expected_relative_paths(self) -> None:
        jobs = screenshot_jobs()

        self.assertEqual(jobs[0].relative_path, Path("gallery") / "img" / f"{jobs[0].theme_id.value}.png")
        self.assertEqual(jobs[-1].relative_path, Path("gallery") / "img" / f"{jobs[-1].theme_id.value}.png")

    def test_jobs_to_render_skip_existing_files_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            existing_file = output_dir / "dark.png"
            existing_file.touch()

            jobs = jobs_to_render(output_dir=output_dir, themes=(ThemeId.DARK, ThemeId.LIGHT))

        self.assertEqual(tuple(job.theme_id for job in jobs), (ThemeId.LIGHT,))

    def test_jobs_to_render_force_includes_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            existing_file = output_dir / "dark.png"
            existing_file.touch()

            jobs = jobs_to_render(output_dir=output_dir, themes=(ThemeId.DARK, ThemeId.LIGHT), force=True)

        self.assertEqual(tuple(job.theme_id for job in jobs), (ThemeId.DARK, ThemeId.LIGHT))

    def test_parse_args_supports_force_flag(self) -> None:
        args = parse_args(["--theme", "dark", "--force"])

        self.assertEqual(args.themes, ["dark"])
        self.assertTrue(args.force)

    def test_resolve_themes_validates_theme_names(self) -> None:
        self.assertEqual(resolve_themes(["dark", "light"]), (ThemeId.DARK, ThemeId.LIGHT))

        with self.assertRaises(ValueError):
            resolve_themes(["missing"])

    def test_repository_root_points_at_checkout(self) -> None:
        self.assertTrue((REPO_ROOT / "README.md").is_file())
        self.assertEqual(REPO_ROOT.name, "qlementine-themes")

    def test_readme_contains_embedded_gallery_images(self) -> None:
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(README_IMAGE_HEADER, readme_text)
        for job in screenshot_jobs():
            self.assertIn(f"]({job.relative_path.as_posix()})", readme_text)
            self.assertIn("![", readme_text)


if __name__ == "__main__":
    unittest.main()
