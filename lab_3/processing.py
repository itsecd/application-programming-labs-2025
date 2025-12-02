from __future__ import annotations
from typing import Literal
import numpy as np
from numpy.typing import NDArray

GradientDirection = Literal["horizontal", "vertical"]

def apply_gradient_lightening(
    image: NDArray[np.uint8],
    direction: GradientDirection = "horizontal",
    intensity: float = 1.0,
) -> NDArray[np.uint8]:
    """Применяет градиентное осветление к изображению.

    Осветление происходит линейно от 0 до 100×intensity единиц яркости
    в выбранном направлении.

    Args:
        image (NDArray[np.uint8]): Исходное изображение в формате RGB (H×W×3).
        direction (GradientDirection): Направление градиента.
            "horizontal" – слева направо,
            "vertical"   – сверху вниз.
        intensity (float): Коэффициент силы эффекта.
            1.0 – стандартное осветление до +100,
            0.0 – без изменений.

    Returns:
        NDArray[np.uint8]: Обработанное изображение (новый массив).
    """
    result = image.astype(np.float32)
    height, width = image.shape[:2]

    if direction == "horizontal":
        gradient = np.linspace(0, 1, width, dtype=np.float32)
        gradient = np.tile(gradient, (height, 1))
    else:
        gradient = np.linspace(0, 1, height, dtype=np.float32)
        gradient = np.tile(gradient, (width, 1)).T

    brightening = gradient[:, :, np.newaxis] * 255 * intensity
    result += brightening

    return np.clip(result, 0, 255).astype(np.uint8)