# -*- coding: utf-8 -*-
"""FileService.py - File I/O Operations (SRP)"""

import cv2
import numpy as np
from typing import Optional, Tuple
from tkinter import filedialog
import os


class FileService:
    """Service for file operations - follows Single Responsibility Principle"""

    @staticmethod
    def load_image(file_path: str) -> Optional[Tuple[np.ndarray, str]]:
        """
        Load image from file path

        Args:
            file_path: Path to image file

        Returns:
            Tuple of (image, file_path) or None if failed
        """
        if not file_path or not os.path.exists(file_path):
            return None

        try:
            image = cv2.imread(file_path)
            if image is None:
                return None
            return image, file_path
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    @staticmethod
    def save_image(image: np.ndarray, file_path: str) -> bool:
        """
        Save image to file path

        Args:
            image: Image to save
            file_path: Destination path

        Returns:
            True if successful, False otherwise
        """
        if image is None or not file_path:
            return False

        try:
            cv2.imwrite(file_path, image)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    @staticmethod
    def open_file_dialog() -> Optional[str]:
        """
        Open file dialog to select image

        Returns:
            Selected file path or None if cancelled
        """
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        return file_path if file_path else None

    @staticmethod
    def save_file_dialog(default_name: str = "edited_image.jpg") -> Optional[str]:
        """
        Open file dialog to save image

        Args:
            default_name: Default filename

        Returns:
            Selected file path or None if cancelled
        """
        filetypes = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff *.tif"),
            ("All files", "*.*")
        ]
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".jpg",
            initialfile=default_name,
            filetypes=filetypes
        )
        return file_path if file_path else None

    @staticmethod
    def get_file_info(file_path: str) -> Optional[dict]:
        """
        Get file information

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file info or None if file doesn't exist
        """
        if not file_path or not os.path.exists(file_path):
            return None

        try:
            stat = os.stat(file_path)
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified': stat.st_mtime
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
