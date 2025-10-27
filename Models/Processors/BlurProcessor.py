# -*- coding: utf-8 -*-
"""BlurProcessor.py - Blur image processing (Strategy Pattern)"""

import cv2
import numpy as np
from enum import Enum
from .BaseProcessor import BaseProcessor, ProcessorConfig


class BlurType(Enum):
    """Enum for blur operations"""
    AVERAGE = "average"
    GAUSSIAN = "gaussian"
    MEDIAN = "median"
    BILATERAL = "bilateral"


class BlurProcessor(BaseProcessor):
    """Blur processor implementing Strategy Pattern"""

    def __init__(self, blur_type: BlurType, config: ProcessorConfig = None):
        super().__init__(f"Blur_{blur_type.value}", config)
        self.blur_type = blur_type

    def process(self, image: np.ndarray) -> np.ndarray:
        """Apply blur based on type"""
        self.validate_image(image)

        if self.blur_type == BlurType.AVERAGE:
            return self._apply_average_blur(image)
        elif self.blur_type == BlurType.GAUSSIAN:
            return self._apply_gaussian_blur(image)
        elif self.blur_type == BlurType.MEDIAN:
            return self._apply_median_blur(image)
        elif self.blur_type == BlurType.BILATERAL:
            return self._apply_bilateral_blur(image)
        else:
            raise ValueError(f"Unknown blur type: {self.blur_type}")

    def _apply_average_blur(self, image: np.ndarray) -> np.ndarray:
        """Average blur using cv2.blur"""
        kernel_size = self.config.get('kernel_size', (5, 5))
        return cv2.blur(image, kernel_size)

    def _apply_gaussian_blur(self, image: np.ndarray) -> np.ndarray:
        """Gaussian blur using cv2.GaussianBlur"""
        kernel_size = self.config.get('kernel_size', (5, 5))
        sigma = self.config.get('sigma', 1)
        return cv2.GaussianBlur(image, kernel_size, sigma)

    def _apply_median_blur(self, image: np.ndarray) -> np.ndarray:
        """Median blur using cv2.medianBlur"""
        kernel_size = self.config.get('kernel_size', 5)
        return cv2.medianBlur(image, kernel_size)

    def _apply_bilateral_blur(self, image: np.ndarray) -> np.ndarray:
        """Bilateral blur using cv2.bilateralFilter - preserves edges"""
        d = self.config.get('d', 9)
        sigma_color = self.config.get('sigma_color', 75)
        sigma_space = self.config.get('sigma_space', 75)
        return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
