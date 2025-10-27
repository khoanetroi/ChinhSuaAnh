# -*- coding: utf-8 -*-
"""
TransformProcessor.py - Image transformation operations processor
"""

import cv2
import numpy as np
from enum import Enum
from .BaseProcessor import BaseProcessor, ProcessorConfig


class TransformType(Enum):
    """Types of transformation operations"""
    ROTATE_90_CW = "rotate_90_clockwise"
    ROTATE_90_CCW = "rotate_90_counterclockwise"
    ROTATE_180 = "rotate_180"
    FLIP_HORIZONTAL = "flip_horizontal"
    FLIP_VERTICAL = "flip_vertical"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"


class TransformProcessor(BaseProcessor):
    """
    Processor for image transformation operations.
    Preserves exact behavior from original Features/Transform.py
    """

    def __init__(self, transform_type: TransformType, config: ProcessorConfig = None):
        super().__init__(f"Transform-{transform_type.value}", config)
        self.transform_type = transform_type

    def process(self, image: np.ndarray) -> np.ndarray:
        """Apply transformation to image"""
        self.validate_image(image)

        if self.transform_type == TransformType.ROTATE_90_CW:
            return self._rotate_90_clockwise(image)
        elif self.transform_type == TransformType.ROTATE_90_CCW:
            return self._rotate_90_counterclockwise(image)
        elif self.transform_type == TransformType.ROTATE_180:
            return self._rotate_180(image)
        elif self.transform_type == TransformType.FLIP_HORIZONTAL:
            return self._flip_horizontal(image)
        elif self.transform_type == TransformType.FLIP_VERTICAL:
            return self._flip_vertical(image)
        elif self.transform_type == TransformType.ZOOM_IN:
            return self._zoom_in(image)
        elif self.transform_type == TransformType.ZOOM_OUT:
            return self._zoom_out(image)
        else:
            raise ValueError(f"Unknown transform type: {self.transform_type}")

    def _rotate_90_clockwise(self, image: np.ndarray) -> np.ndarray:
        """Rotate image 90 degrees clockwise"""
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    def _rotate_90_counterclockwise(self, image: np.ndarray) -> np.ndarray:
        """Rotate image 90 degrees counterclockwise"""
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def _rotate_180(self, image: np.ndarray) -> np.ndarray:
        """Rotate image 180 degrees"""
        return cv2.rotate(image, cv2.ROTATE_180)

    def _flip_horizontal(self, image: np.ndarray) -> np.ndarray:
        """Flip image horizontally"""
        return cv2.flip(image, 1)

    def _flip_vertical(self, image: np.ndarray) -> np.ndarray:
        """Flip image vertically"""
        return cv2.flip(image, 0)

    def _zoom_in(self, image: np.ndarray) -> np.ndarray:
        """Zoom in (enlarge) image"""
        zoom_factor = self.config.get('zoom_factor', 1.3)
        h, w = image.shape[:2]
        new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Crop to original size from center
        start_y = (new_h - h) // 2
        start_x = (new_w - w) // 2
        cropped = resized[start_y:start_y+h, start_x:start_x+w]

        return cropped

    def _zoom_out(self, image: np.ndarray) -> np.ndarray:
        """Zoom out (shrink) image"""
        zoom_factor = self.config.get('zoom_factor', 0.7)
        h, w = image.shape[:2]
        new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Create canvas with original size
        canvas = np.zeros_like(image)
        start_y = (h - new_h) // 2
        start_x = (w - new_w) // 2
        canvas[start_y:start_y+new_h, start_x:start_x+new_w] = resized

        return canvas
