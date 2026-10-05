"""
Unit tests for the Future Impact frame scroll animation modules and assets.
"""
import os
import unittest
import glob
import re

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lerp(start: float, end: float, factor: float) -> float:
    return start + (end - start) * factor


def clamp(value: float, min_val: float, max_val: float) -> float:
    return min(max(value, min_val), max_val)


def clamp01(v: float) -> float:
    return max(0.0, min(1.0, v))


def ease_in_out_cubic(t: float) -> float:
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def calculate_cover_dimensions(container_w: float, container_h: float, img_w: float, img_h: float):
    if not container_w or not container_h or not img_w or not img_h:
        return {"dx": 0, "dy": 0, "dWidth": 0, "dHeight": 0}

    c_ratio = container_w / container_h
    i_ratio = img_w / img_h

    if c_ratio > i_ratio:
        d_width = container_w
        d_height = container_w / i_ratio
    else:
        d_height = container_h
        d_width = container_h * i_ratio

    dx = (container_w - d_width) / 2
    dy = (container_h - d_height) / 2
    return {"dx": dx, "dy": dy, "dWidth": d_width, "dHeight": d_height}


def calculate_scroll_progress(offset_height: float, inner_height: float, current_scrolled: float) -> float:
    total_distance = offset_height - inner_height
    if total_distance <= 0:
        return 0.0
    return clamp(current_scrolled / total_distance, 0.0, 1.0)


def map_progress_to_frame(progress: float, total_frames: int = 270) -> int:
    frame_scrub_progress = clamp01(progress / 0.85)
    frame_num = int(round(frame_scrub_progress * (total_frames - 1))) + 1
    return int(clamp(frame_num, 1, total_frames))


def map_progress_to_sand(progress: float) -> float:
    return clamp01((progress - 0.85) / 0.15)


class TestScrollAnimationCore(unittest.TestCase):

    def test_lerp_function(self):
        self.assertAlmostEqual(lerp(0, 100, 0.5), 50.0)
        self.assertAlmostEqual(lerp(10, 20, 0.1), 11.0)
        self.assertAlmostEqual(lerp(50, 50, 0.8), 50.0)

    def test_clamp_function(self):
        self.assertEqual(clamp(150, 0, 100), 100)
        self.assertEqual(clamp(-20, 0, 100), 0)
        self.assertEqual(clamp(50, 0, 100), 50)

    def test_clamp01_and_ease(self):
        self.assertEqual(clamp01(-0.2), 0.0)
        self.assertEqual(clamp01(1.2), 1.0)
        self.assertAlmostEqual(ease_in_out_cubic(0.0), 0.0)
        self.assertAlmostEqual(ease_in_out_cubic(0.5), 0.5)
        self.assertAlmostEqual(ease_in_out_cubic(1.0), 1.0)

    def test_cover_dimensions_wider_container(self):
        res = calculate_cover_dimensions(1920, 1080, 800, 600)
        self.assertAlmostEqual(res["dWidth"], 1920)
        self.assertAlmostEqual(res["dHeight"], 1440)
        self.assertAlmostEqual(res["dx"], 0)
        self.assertAlmostEqual(res["dy"], -180)

    def test_cover_dimensions_taller_container(self):
        res = calculate_cover_dimensions(400, 800, 1920, 1080)
        self.assertAlmostEqual(res["dHeight"], 800)
        self.assertAlmostEqual(res["dWidth"], 1422.222, places=2)
        self.assertAlmostEqual(res["dx"], -511.11, places=1)
        self.assertAlmostEqual(res["dy"], 0)

    def test_cover_dimensions_zero_handling(self):
        res = calculate_cover_dimensions(0, 1080, 1920, 1080)
        self.assertEqual(res["dWidth"], 0)

    def test_scroll_progress_calculation(self):
        self.assertAlmostEqual(calculate_scroll_progress(5000, 1000, 0), 0.0)
        self.assertAlmostEqual(calculate_scroll_progress(5000, 1000, 2000), 0.5)
        self.assertAlmostEqual(calculate_scroll_progress(5000, 1000, 4000), 1.0)
        self.assertAlmostEqual(calculate_scroll_progress(5000, 1000, -500), 0.0)
        self.assertAlmostEqual(calculate_scroll_progress(5000, 1000, 6000), 1.0)

    def test_frame_mapping_with_scroll_end_buffer(self):
        self.assertEqual(map_progress_to_frame(0.0, 270), 1)
        self.assertEqual(map_progress_to_frame(0.85, 270), 270)
        self.assertEqual(map_progress_to_frame(1.0, 270), 270)

    def test_sand_scroll_reversibility(self):
        # Sand animation active from 0.85 to 1.0
        self.assertEqual(map_progress_to_sand(0.80), 0.0)
        self.assertEqual(map_progress_to_sand(0.85), 0.0)
        self.assertAlmostEqual(map_progress_to_sand(0.925), 0.5)
        self.assertEqual(map_progress_to_sand(1.0), 1.0)
        # Reverse down-to-up scroll
        self.assertAlmostEqual(map_progress_to_sand(0.925), 0.5)
        self.assertEqual(map_progress_to_sand(0.85), 0.0)


class TestWorkspaceIntegrity(unittest.TestCase):

    def test_frameswl_frames_exist(self):
        frames = glob.glob(os.path.join(WORKSPACE_DIR, "frameswl", "ezgif-frame-*.jpg"))
        self.assertEqual(len(frames), 270, "All 270 frames must be present in frameswl.")

    def test_brand_logo_exists(self):
        logo_path = os.path.join(WORKSPACE_DIR, "LOGO.png")
        self.assertTrue(os.path.exists(logo_path), "Brand logo LOGO.png must exist.")

    def test_file_line_counts_within_limit(self):
        """Rule: Make sure each file must not more then 500 lines of code."""
        check_dirs = [WORKSPACE_DIR, os.path.join(WORKSPACE_DIR, "js"), os.path.join(WORKSPACE_DIR, "css")]
        for d in check_dirs:
            for fname in os.listdir(d):
                fpath = os.path.join(d, fname)
                if os.path.isfile(fpath) and fname.endswith((".js", ".css", ".html", ".py")):
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    self.assertLessEqual(
                        len(lines), 500,
                        f"File {fname} has {len(lines)} lines, exceeding 500 line limit."
                    )


if __name__ == "__main__":
    unittest.main()
