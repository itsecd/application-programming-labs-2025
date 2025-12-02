from typing import Tuple, Union
import numpy as np
import numpy.typing as npt

# Типы для работы с изображениями
ImageArray = npt.NDArray[np.uint8]
ImageShape = Tuple[int, int, int]
ImagePath = Union[str, bytes]