# -*- coding: utf-8 -*-
"""ImageService.py - Image Processing Orchestration (SRP, DIP)"""

import cv2
import numpy as np
from typing import Optional
from Models import ImageModel, ImageHistory
from Models.Processors import BaseProcessor


class ImageService:
    """
    Service for image processing orchestration.
    Follows Single Responsibility Principle and Dependency Inversion Principle.
    """

    def __init__(self, model: ImageModel, history: ImageHistory):
        """
        Initialize ImageService with dependencies injected

        Args:
            model: ImageModel instance
            history: ImageHistory instance
        """
        self.model = model
        self.history = history

    def load_image(self, image: np.ndarray, file_path: Optional[str] = None):
        """
        Load image into model and initialize history

        Args:
            image: Image array
            file_path: Optional path to file
        """
        self.model.set_image(image, file_path)
        self.history.set_initial(image)

    def get_current_image(self) -> Optional[np.ndarray]:
        """Get current image from model"""
        return self.model.get_copy()

    def get_original_image(self) -> Optional[np.ndarray]:
        """Get original image from model"""
        return self.model.get_original_copy()

    def has_image(self) -> bool:
        """Check if model has an image"""
        return self.model.has_image()

    def apply_processor(self, processor: BaseProcessor) -> bool:
        """
        Apply a processor to current image

        Args:
            processor: Processor to apply (Strategy Pattern)

        Returns:
            True if successful, False otherwise
        """
        if not self.model.has_image():
            return False

        try:
            current = self.model.get_copy()
            processed = processor.process(current)

            if processed is not None:
                self.model.update_current(processed)
                self.history.push(processed)
                return True
            return False
        except Exception as e:
            print(f"Error applying processor {processor.name}: {e}")
            return False

    def undo(self) -> bool:
        """
        Undo last operation

        Returns:
            True if undo successful, False otherwise
        """
        if not self.history.can_undo():
            return False

        current = self.model.get_copy()
        restored = self.history.undo(current)

        if restored is not None:
            self.model.update_current(restored)
            return True
        return False

    def redo(self) -> bool:
        """
        Redo last undone operation

        Returns:
            True if redo successful, False otherwise
        """
        if not self.history.can_redo():
            return False

        restored = self.history.redo()

        if restored is not None:
            self.model.update_current(restored)
            return True
        return False

    def can_undo(self) -> bool:
        """Check if undo is available"""
        return self.history.can_undo()

    def can_redo(self) -> bool:
        """Check if redo is available"""
        return self.history.can_redo()

    def reset_to_original(self):
        """Reset image to original state"""
        if self.model.has_image():
            self.model.reset_to_original()
            self.history.clear()
            self.history.set_initial(self.model.get_copy())

    def get_image_info(self) -> dict:
        """Get information about current image"""
        if not self.model.has_image():
            return {}

        return {
            'width': self.model.width,
            'height': self.model.height,
            'channels': self.model.channels,
            'file_path': self.model.file_path,
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo()
        }

    def resize_for_display(self, max_width: int = 800, max_height: int = 600) -> Optional[np.ndarray]:
        """
        Resize image for display while maintaining aspect ratio

        Args:
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Resized image or None
        """
        if not self.model.has_image():
            return None

        image = self.model.get_copy()
        h, w = image.shape[:2]

        # Calculate scaling factor
        scale = min(max_width / w, max_height / h, 1.0)

        if scale < 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

        return image
