# -*- coding: utf-8 -*-
"""FaceDetectionService.py - Face Detection with Caching (Singleton Pattern)"""

import cv2
import numpy as np
from typing import List, Tuple


class FaceDetectionService:
    """
    Singleton service for face detection with cached Haar Cascade.
    Solves performance issue from original code that recreated cascade each time.
    """
    _instance = None
    _cascade = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FaceDetectionService, cls).__new__(cls)
            cls._instance._initialize_cascade()
        return cls._instance

    def _initialize_cascade(self):
        """Initialize Haar Cascade once (lazy loading)"""
        if self._cascade is None:
            self._cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image - preserves exact behavior from Features/FaceBeautify.py
        but with cached cascade for better performance.

        Args:
            image: Input image (BGR format)

        Returns:
            List of face rectangles as (x, y, w, h) tuples
        """
        if image is None or image.size == 0:
            return []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Improve image quality before detection
        gray = cv2.equalizeHist(gray)

        # Reduce scaleFactor and minNeighbors to detect more faces
        # scaleFactor: 1.05 = more sensitive, minNeighbors: 3 = less strict
        faces = self._cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        return faces

    def draw_face_rectangles(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]],
                              color=(0, 255, 0), thickness=3) -> np.ndarray:
        """Draw rectangles around detected faces"""
        result = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(result, (x, y), (x+w, y+h), color, thickness)
            cv2.putText(result, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return result
