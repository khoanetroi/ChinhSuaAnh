# -*- coding: utf-8 -*-
"""FaceBeautifyProcessor.py - Face beautification (Strategy Pattern)"""

import cv2
import numpy as np
from enum import Enum
from typing import Tuple, List
from .BaseProcessor import BaseProcessor, ProcessorConfig


class FaceBeautifyType(Enum):
    """Enum for face beautification operations"""
    SMOOTH_SKIN = "smooth_skin"
    BRIGHTEN_FACE = "brighten_face"
    ENHANCE_CONTRAST = "enhance_contrast"
    REMOVE_BLEMISHES = "remove_blemishes"
    AUTO_BEAUTIFY = "auto_beautify"
    BLUR_BACKGROUND = "blur_background"
    SOFT_FILTER = "soft_filter"


class FaceBeautifyProcessor(BaseProcessor):
    """Face beautification processor implementing Strategy Pattern"""

    def __init__(self, beautify_type: FaceBeautifyType, config: ProcessorConfig = None):
        super().__init__(f"FaceBeautify_{beautify_type.value}", config)
        self.beautify_type = beautify_type

    def process(self, image: np.ndarray) -> np.ndarray:
        """Apply face beautification based on type"""
        self.validate_image(image)

        # Detect faces if needed (all operations except soft_filter need faces)
        if self.beautify_type != FaceBeautifyType.SOFT_FILTER:
            faces = self._detect_faces(image)
            if len(faces) == 0:
                # No faces detected, return original image
                return image
        else:
            faces = []

        if self.beautify_type == FaceBeautifyType.SMOOTH_SKIN:
            return self._smooth_skin(image, faces)
        elif self.beautify_type == FaceBeautifyType.BRIGHTEN_FACE:
            return self._brighten_face(image, faces)
        elif self.beautify_type == FaceBeautifyType.ENHANCE_CONTRAST:
            return self._enhance_face_contrast(image, faces)
        elif self.beautify_type == FaceBeautifyType.REMOVE_BLEMISHES:
            return self._remove_blemishes(image, faces)
        elif self.beautify_type == FaceBeautifyType.AUTO_BEAUTIFY:
            return self._beautify_face_auto(image, faces)
        elif self.beautify_type == FaceBeautifyType.BLUR_BACKGROUND:
            return self._apply_blur_background(image, faces)
        elif self.beautify_type == FaceBeautifyType.SOFT_FILTER:
            return self._add_soft_filter(image)
        else:
            raise ValueError(f"Unknown face beautify type: {self.beautify_type}")

    def _detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in image - preserves exact behavior from Features/FaceBeautify.py"""
        # Note: This recreates cascade each time (performance issue)
        # In Service layer, we'll cache this using Singleton pattern
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Improve image quality before detection
        gray = cv2.equalizeHist(gray)

        # Reduce scaleFactor and minNeighbors to detect more faces
        # scaleFactor: 1.05 = more sensitive, minNeighbors: 3 = less strict
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces

    def _smooth_skin(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Smooth skin using Bilateral Filter"""
        smooth_level = self.config.get('smooth_level', 0.3)
        result = image.copy()

        for (x, y, w, h) in faces:
            face_roi = result[y:y+h, x:x+w]
            d = int(9 + smooth_level * 20)
            sigma_color = int(50 + smooth_level * 100)
            sigma_space = int(50 + smooth_level * 100)
            smoothed = cv2.bilateralFilter(face_roi, d, sigma_color, sigma_space)
            alpha = 0.3 + smooth_level * 0.7
            blended = cv2.addWeighted(face_roi, 1-alpha, smoothed, alpha, 0)
            result[y:y+h, x:x+w] = blended

        return result

    def _brighten_face(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Brighten face regions"""
        brightness_value = self.config.get('brightness_value', 30)
        result = image.copy()

        for (x, y, w, h) in faces:
            face_roi = result[y:y+h, x:x+w]
            brightened = cv2.convertScaleAbs(face_roi, alpha=1.0, beta=brightness_value)
            result[y:y+h, x:x+w] = brightened

        return result

    def _enhance_face_contrast(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Enhance contrast for face regions"""
        contrast = self.config.get('contrast', 1.3)
        result = image.copy()

        for (x, y, w, h) in faces:
            face_roi = result[y:y+h, x:x+w]
            enhanced = cv2.convertScaleAbs(face_roi, alpha=contrast, beta=0)
            result[y:y+h, x:x+w] = enhanced

        return result

    def _remove_blemishes(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Remove blemishes from face regions"""
        result = image.copy()

        for (x, y, w, h) in faces:
            face_roi = result[y:y+h, x:x+w]
            denoised = cv2.fastNlMeansDenoisingColored(face_roi, None, 10, 10, 7, 21)
            result[y:y+h, x:x+w] = denoised

        return result

    def _beautify_face_auto(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Auto beautify combining multiple techniques"""
        result = image.copy()

        # Apply operations in sequence
        temp_config_smooth = ProcessorConfig()
        temp_config_smooth.set('smooth_level', 0.5)
        original_config = self.config
        self.config = temp_config_smooth
        result = self._smooth_skin(result, faces)

        temp_config_bright = ProcessorConfig()
        temp_config_bright.set('brightness_value', 15)
        self.config = temp_config_bright
        result = self._brighten_face(result, faces)

        temp_config_contrast = ProcessorConfig()
        temp_config_contrast.set('contrast', 1.15)
        self.config = temp_config_contrast
        result = self._enhance_face_contrast(result, faces)

        self.config = original_config
        result = self._remove_blemishes(result, faces)

        return result

    def _apply_blur_background(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """Blur background while keeping face sharp"""
        blur_amount = self.config.get('blur_amount', 21)
        result = image.copy()
        blurred = cv2.GaussianBlur(result, (blur_amount, blur_amount), 0)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        for (x, y, w, h) in faces:
            padding = int(w * 0.2)
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            axes = ((x2 - x1) // 2, (y2 - y1) // 2)
            cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)

        mask = cv2.GaussianBlur(mask, (21, 21), 0)
        mask = mask / 255.0
        mask = np.stack([mask] * 3, axis=2)
        result = (result * mask + blurred * (1 - mask)).astype(np.uint8)

        return result

    def _add_soft_filter(self, image: np.ndarray) -> np.ndarray:
        """Add soft filter (soft glow effect)"""
        intensity = self.config.get('intensity', 0.3)
        blurred = cv2.GaussianBlur(image, (0, 0), 10)
        result = cv2.addWeighted(image, 1 - intensity, blurred, intensity, 0)
        return result
