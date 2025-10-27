# -*- coding: utf-8 -*-
"""
EdgeDetectionProcessor.py - Edge detection operations processor
"""

import cv2
import numpy as np
from enum import Enum
from .BaseProcessor import BaseProcessor, ProcessorConfig


class EdgeDetectionType(Enum):
    """Types of edge detection operations"""
    ROBERTS = "roberts"
    PREWITT = "prewitt"
    SOBEL = "sobel"
    CANNY = "canny"
    LAPLACIAN = "laplacian"
    SCHARR = "scharr"


class EdgeDetectionProcessor(BaseProcessor):
    """
    Processor for edge detection operations.
    Preserves exact behavior from original Features/EdgeDetection.py
    """

    def __init__(self, detection_type: EdgeDetectionType, config: ProcessorConfig = None):
        super().__init__(f"EdgeDetection-{detection_type.value}", config)
        self.detection_type = detection_type

    def process(self, image: np.ndarray) -> np.ndarray:
        """Apply edge detection to image"""
        self.validate_image(image)

        if self.detection_type == EdgeDetectionType.ROBERTS:
            return self._roberts_edge(image)
        elif self.detection_type == EdgeDetectionType.PREWITT:
            return self._prewitt_edge(image)
        elif self.detection_type == EdgeDetectionType.SOBEL:
            return self._sobel_edge(image)
        elif self.detection_type == EdgeDetectionType.CANNY:
            return self._canny_edge(image)
        elif self.detection_type == EdgeDetectionType.LAPLACIAN:
            return self._laplacian_edge(image)
        elif self.detection_type == EdgeDetectionType.SCHARR:
            return self._scharr_edge(image)
        else:
            raise ValueError(f"Unknown detection type: {self.detection_type}")

    def _roberts_edge(self, image: np.ndarray) -> np.ndarray:
        """Roberts Cross edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Roberts kernels
        roberts_cross_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
        roberts_cross_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)

        # Apply kernels
        grad_x = cv2.filter2D(gray, cv2.CV_32F, roberts_cross_x)
        grad_y = cv2.filter2D(gray, cv2.CV_32F, roberts_cross_y)

        # Combine gradients
        edges = np.sqrt(grad_x**2 + grad_y**2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def _prewitt_edge(self, image: np.ndarray) -> np.ndarray:
        """Prewitt edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Prewitt kernels
        prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
        prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)

        # Apply kernels
        grad_x = cv2.filter2D(gray, cv2.CV_32F, prewitt_x)
        grad_y = cv2.filter2D(gray, cv2.CV_32F, prewitt_y)

        # Combine gradients
        edges = np.sqrt(grad_x**2 + grad_y**2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def _sobel_edge(self, image: np.ndarray) -> np.ndarray:
        """Sobel edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ksize = self.config.get('ksize', 3)

        # Apply Sobel
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

        # Combine gradients
        edges = np.sqrt(grad_x**2 + grad_y**2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def _canny_edge(self, image: np.ndarray) -> np.ndarray:
        """Canny edge detection with automatic thresholds"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Auto thresholds
        sigma = self.config.get('sigma', 0.33)
        median = np.median(gray)
        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))

        # Apply Canny
        edges = cv2.Canny(gray, lower, upper)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def _laplacian_edge(self, image: np.ndarray) -> np.ndarray:
        """Laplacian edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ksize = self.config.get('ksize', 3)

        # Apply Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
        edges = np.absolute(laplacian)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def _scharr_edge(self, image: np.ndarray) -> np.ndarray:
        """Scharr edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Scharr
        grad_x = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
        grad_y = cv2.Scharr(gray, cv2.CV_64F, 0, 1)

        # Combine gradients
        edges = np.sqrt(grad_x**2 + grad_y**2)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
