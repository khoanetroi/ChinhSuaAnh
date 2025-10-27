# -*- coding: utf-8 -*-
"""SharpenProcessor.py - Image sharpening (Strategy Pattern)"""

import cv2
import numpy as np
from enum import Enum
from .BaseProcessor import BaseProcessor, ProcessorConfig


class SharpenType(Enum):
    """Enum for sharpening operations"""
    BASIC = "basic"
    LAPLACIAN = "laplacian"
    UNSHARP_MASK = "unsharp_mask"
    HIGHPASS = "highpass"
    ADAPTIVE = "adaptive"
    DETAIL_ENHANCE = "detail_enhance"
    EDGE_PRESERVE = "edge_preserve"


class SharpenProcessor(BaseProcessor):
    """Sharpen processor implementing Strategy Pattern"""

    def __init__(self, sharpen_type: SharpenType, config: ProcessorConfig = None):
        super().__init__(f"Sharpen_{sharpen_type.value}", config)
        self.sharpen_type = sharpen_type

    def process(self, image: np.ndarray) -> np.ndarray:
        """Apply sharpening based on type"""
        self.validate_image(image)

        if self.sharpen_type == SharpenType.BASIC:
            return self._sharpen_basic(image)
        elif self.sharpen_type == SharpenType.LAPLACIAN:
            return self._sharpen_laplacian(image)
        elif self.sharpen_type == SharpenType.UNSHARP_MASK:
            return self._unsharp_mask(image)
        elif self.sharpen_type == SharpenType.HIGHPASS:
            return self._sharpen_highpass(image)
        elif self.sharpen_type == SharpenType.ADAPTIVE:
            return self._adaptive_sharpen(image)
        elif self.sharpen_type == SharpenType.DETAIL_ENHANCE:
            return self._detail_enhance(image)
        elif self.sharpen_type == SharpenType.EDGE_PRESERVE:
            return self._edge_preserve_sharpen(image)
        else:
            raise ValueError(f"Unknown sharpen type: {self.sharpen_type}")

    def _sharpen_basic(self, image: np.ndarray) -> np.ndarray:
        """Basic sharpening using kernel - preserves exact behavior from Features/Sharpen.py"""
        strength = self.config.get('strength', 1.0)

        # Basic sharpening kernel
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)

        # Adjust strength
        kernel = kernel * strength
        kernel[1, 1] = 1 + 4 * strength

        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened

    def _sharpen_laplacian(self, image: np.ndarray) -> np.ndarray:
        """Sharpen using Laplacian operator"""
        strength = self.config.get('strength', 1.0)

        # Calculate Laplacian
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)

        # Combine with original
        sharpened = cv2.addWeighted(image, 1.0, laplacian, strength, 0)

        return sharpened

    def _unsharp_mask(self, image: np.ndarray) -> np.ndarray:
        """Sharpen using Unsharp Masking"""
        kernel_size = self.config.get('kernel_size', (5, 5))
        sigma = self.config.get('sigma', 1.0)
        amount = self.config.get('amount', 1.0)
        threshold = self.config.get('threshold', 0)

        # Create blurred image
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)

        # Create mask
        mask = cv2.subtract(image, blurred)

        # Apply threshold if needed
        if threshold > 0:
            _, mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY)

        # Combine with original
        sharpened = cv2.addWeighted(image, 1.0, mask, amount, 0)

        return sharpened

    def _sharpen_highpass(self, image: np.ndarray) -> np.ndarray:
        """Sharpen using High-pass filter"""
        kernel_size = self.config.get('kernel_size', 3)

        # Create low-pass filter
        lowpass = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

        # High-pass = Original - Low-pass
        highpass = cv2.subtract(image, lowpass)

        # Combine
        sharpened = cv2.add(image, highpass)

        return sharpened

    def _adaptive_sharpen(self, image: np.ndarray) -> np.ndarray:
        """Adaptive sharpening based on image blur amount"""
        blur_amount = self.config.get('blur_amount', None)

        # Calculate blur amount if not provided
        if blur_amount is None:
            # Use Laplacian variance to estimate blur
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

            # More blur = lower variance
            # Adjust strength based on variance
            if laplacian_var < 100:
                strength = 2.0  # Very blurry
            elif laplacian_var < 500:
                strength = 1.5  # Slightly blurry
            else:
                strength = 1.0  # Relatively sharp
        else:
            strength = blur_amount

        # Use unsharp mask with calculated strength
        temp_config = ProcessorConfig()
        temp_config.set('kernel_size', (5, 5))
        temp_config.set('sigma', 1.0)
        temp_config.set('amount', strength)
        temp_config.set('threshold', 0)

        original_config = self.config
        self.config = temp_config
        result = self._unsharp_mask(image)
        self.config = original_config

        return result

    def _detail_enhance(self, image: np.ndarray) -> np.ndarray:
        """Detail enhancement using cv2.detailEnhance - CRITICAL feature"""
        sigma_s = self.config.get('sigma_s', 60)
        sigma_r = self.config.get('sigma_r', 0.07)

        return cv2.detailEnhance(image, sigma_s=sigma_s, sigma_r=sigma_r)

    def _edge_preserve_sharpen(self, image: np.ndarray) -> np.ndarray:
        """Sharpen while preserving edges"""
        # Use bilateral filter to preserve edges
        smooth = cv2.bilateralFilter(image, 9, 75, 75)

        # Create mask from difference
        mask = cv2.subtract(image, smooth)

        # Combine to sharpen
        sharpened = cv2.add(image, mask)

        return sharpened
