# -*- coding: utf-8 -*-
"""BrightnessProcessor.py - Brightness/Contrast adjustment (Strategy Pattern)"""

import cv2
import numpy as np
from enum import Enum
from .BaseProcessor import BaseProcessor, ProcessorConfig


class BrightnessOperation(Enum):
    """Enum for brightness operations"""
    INCREASE = "increase"
    DECREASE = "decrease"
    CONTRAST = "contrast"
    GAMMA = "gamma"
    AUTO = "auto"


class BrightnessProcessor(BaseProcessor):
    """Brightness/Contrast processor implementing Strategy Pattern"""

    def __init__(self, operation: BrightnessOperation, config: ProcessorConfig = None):
        super().__init__(f"Brightness_{operation.value}", config)
        self.operation = operation

    def process(self, image: np.ndarray) -> np.ndarray:
        """Apply brightness/contrast adjustment based on operation"""
        self.validate_image(image)

        if self.operation == BrightnessOperation.INCREASE:
            return self._increase_brightness(image)
        elif self.operation == BrightnessOperation.DECREASE:
            return self._decrease_brightness(image)
        elif self.operation == BrightnessOperation.CONTRAST:
            return self._adjust_contrast(image)
        elif self.operation == BrightnessOperation.GAMMA:
            return self._gamma_correction(image)
        elif self.operation == BrightnessOperation.AUTO:
            return self._auto_brightness(image)
        else:
            raise ValueError(f"Unknown brightness operation: {self.operation}")

    def _adjust_brightness(self, image: np.ndarray, value: int) -> np.ndarray:
        """Core brightness adjustment - preserves exact behavior from Features/Brightness.py"""
        # Convert to int16 to avoid overflow
        adjusted = image.astype(np.int16)
        adjusted = adjusted + value

        # Clip values to [0, 255]
        adjusted = np.clip(adjusted, 0, 255)

        return adjusted.astype(np.uint8)

    def _increase_brightness(self, image: np.ndarray) -> np.ndarray:
        """Increase brightness"""
        value = self.config.get('value', 50)
        return self._adjust_brightness(image, abs(value))

    def _decrease_brightness(self, image: np.ndarray) -> np.ndarray:
        """Decrease brightness"""
        value = self.config.get('value', 50)
        return self._adjust_brightness(image, -abs(value))

    def _adjust_contrast(self, image: np.ndarray) -> np.ndarray:
        """Adjust contrast using cv2.convertScaleAbs"""
        alpha = self.config.get('alpha', 1.0)  # Contrast control
        beta = self.config.get('beta', 0)       # Brightness control
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    def _gamma_correction(self, image: np.ndarray) -> np.ndarray:
        """Gamma correction using lookup table"""
        gamma = self.config.get('gamma', 1.0)

        # Create lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                          for i in range(256)]).astype(np.uint8)

        # Apply lookup table
        return cv2.LUT(image, table)

    def _auto_brightness(self, image: np.ndarray) -> np.ndarray:
        """Auto brightness to target mean"""
        target_mean = self.config.get('target_mean', 128)
        current_mean = np.mean(image)
        diff = target_mean - current_mean
        return self._adjust_brightness(image, int(diff))
