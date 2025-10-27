# -*- coding: utf-8 -*-
"""ImageModel.py - Image data representation (SRP)"""

import cv2
import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class ImageModel:
    """Represents image data and state. Single Responsibility: Data only."""
    original: Optional[np.ndarray] = None
    current: Optional[np.ndarray] = None
    file_path: Optional[str] = None
    width: int = 0
    height: int = 0
    channels: int = 0

    def __post_init__(self):
        if self.current is not None:
            self._update_dimensions()

    def set_image(self, image: np.ndarray, file_path: Optional[str] = None):
        if image is None:
            raise ValueError("Image cannot be None")
        self.original = image.copy()
        self.current = image.copy()
        self.file_path = file_path
        self._update_dimensions()

    def update_current(self, image: np.ndarray):
        if image is None:
            raise ValueError("Image cannot be None")
        self.current = image.copy()
        self._update_dimensions()

    def reset_to_original(self):
        if self.original is not None:
            self.current = self.original.copy()
            self._update_dimensions()

    def _update_dimensions(self):
        if self.current is not None:
            self.height, self.width = self.current.shape[:2]
            self.channels = self.current.shape[2] if len(self.current.shape) > 2 else 1

    def has_image(self) -> bool:
        return self.current is not None

    def get_copy(self) -> Optional[np.ndarray]:
        return self.current.copy() if self.current is not None else None

    def get_original_copy(self) -> Optional[np.ndarray]:
        return self.original.copy() if self.original is not None else None
