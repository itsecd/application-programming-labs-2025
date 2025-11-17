from __future__ import annotations

import cv2
import numpy as np


def resize_to_match(base: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    """Меняет размер overlay под размер base."""
    height, width = base.shape[:2]
    return cv2.resize(overlay, (width, height), interpolation=cv2.INTER_LINEAR)


def alpha_blend(
    base_bgr: np.ndarray,
    overlay_bgr: np.ndarray,
    alpha: float,
) -> np.ndarray:
    """Накладывает overlay на base с прозрачностью alpha (0..1)."""
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("alpha должен быть в [0, 1].")

    if base_bgr.shape[:2] != overlay_bgr.shape[:2]:
        overlay_bgr = resize_to_match(base_bgr, overlay_bgr)

    return cv2.addWeighted(base_bgr, 1.0 - alpha, overlay_bgr, alpha, 0.0)