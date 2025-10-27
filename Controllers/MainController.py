# -*- coding: utf-8 -*-
"""MainController.py - Main Controller (MVC Pattern)"""

import tkinter as tk
from typing import Optional
from Models import ImageModel, ImageHistory
from Models.Processors import (
    BlurProcessor, BlurType,
    BrightnessProcessor, BrightnessOperation,
    SharpenProcessor, SharpenType,
    EdgeDetectionProcessor, EdgeDetectionType,
    TransformProcessor, TransformType,
    ProcessorConfig
)
from Services import ImageService, FileService, FaceDetectionService
from Views import MainView


class MainController:
    """
    Main Controller for MVC architecture.
    Handles user interactions and coordinates between Model, View, and Services.
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize Main Controller

        Args:
            root: Tkinter root window
        """
        self.root = root

        # Initialize Model
        self.image_model = ImageModel()
        self.image_history = ImageHistory()

        # Initialize Services
        self.image_service = ImageService(self.image_model, self.image_history)
        self.file_service = FileService()
        self.face_service = FaceDetectionService()

        # Initialize View
        self.view = MainView(root)

        # Create UI with callbacks
        self._setup_view()

        # Setup keyboard shortcuts
        self._setup_shortcuts()

        # Initial state
        self._update_ui()

    def _setup_view(self):
        """Setup view with all callbacks"""
        callbacks = {
            # File operations
            'load_image': self.load_image,
            'save_image': self.save_image,
            'reset_image': self.reset_image,

            # History operations
            'undo_action': self.undo_action,
            'redo_action': self.redo_action,

            # Blur operations
            'apply_average_blur': self.apply_average_blur,
            'apply_gaussian_blur': self.apply_gaussian_blur,
            'apply_median_blur': self.apply_median_blur,
            'apply_bilateral_blur': self.apply_bilateral_blur,

            # Brightness operations
            'increase_brightness': self.increase_brightness,
            'decrease_brightness': self.decrease_brightness,
            'increase_contrast': self.increase_contrast,

            # Sharpen operations
            'apply_basic_sharpen': self.apply_basic_sharpen,
            'apply_laplacian_sharpen': self.apply_laplacian_sharpen,
            'apply_unsharp_mask': self.apply_unsharp_mask,
            'apply_detail_enhance': self.apply_detail_enhance,

            # Edge detection operations
            'apply_roberts_edge': self.apply_roberts_edge,
            'apply_prewitt_edge': self.apply_prewitt_edge,
            'apply_sobel_edge': self.apply_sobel_edge,
            'apply_canny_edge': self.apply_canny_edge,
            'apply_laplacian_edge': self.apply_laplacian_edge,
            'apply_scharr_edge': self.apply_scharr_edge,

            # Transform operations
            'rotate_right_90': self.rotate_right_90,
            'rotate_left_90': self.rotate_left_90,
            'rotate_180': self.rotate_180,
            'flip_horizontal': self.flip_horizontal,
            'flip_vertical': self.flip_vertical,
            'zoom_in_image': self.zoom_in_image,
            'zoom_out_image': self.zoom_out_image,

            # Face beautify
            'open_face_beautify_image': self.open_face_beautify_image,
            'open_face_beautify_camera': self.open_face_beautify_camera,
        }

        self.view.create_ui(callbacks)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        shortcuts = {
            '<Control-o>': lambda e: self.load_image(),
            '<Control-s>': lambda e: self.save_image(),
            '<Control-z>': lambda e: self.undo_action(),
            '<Control-y>': lambda e: self.redo_action(),
        }
        self.view.bind_shortcuts(shortcuts)

    def _update_ui(self):
        """Update UI state (image display, buttons, status)"""
        # Update image display
        if self.image_service.has_image():
            image = self.image_service.get_current_image()
            self.view.display_image(image)
        else:
            self.view.clear_image_display()

        # Update history buttons
        self.view.update_history_buttons(
            self.image_service.can_undo(),
            self.image_service.can_redo()
        )

    def _check_image_loaded(self) -> bool:
        """Check if image is loaded, show warning if not"""
        if not self.image_service.has_image():
            self.view.show_warning(
                "Chưa có ảnh",
                "Vui lòng chọn một ảnh trước khi thực hiện thao tác này."
            )
            return False
        return True

    def _apply_processor(self, processor, status_message: str) -> bool:
        """
        Apply processor and update UI

        Args:
            processor: Processor to apply
            status_message: Status message to display

        Returns:
            True if successful, False otherwise
        """
        if not self._check_image_loaded():
            return False

        try:
            success = self.image_service.apply_processor(processor)
            if success:
                self._update_ui()
                self.view.update_status(status_message)
                return True
            else:
                self.view.show_warning("Cảnh báo", "Không có thay đổi nào được áp dụng cho ảnh.")
                return False
        except Exception as e:
            self.view.show_error("Lỗi", f"Không thể áp dụng thao tác:\n{e}")
            return False

    # === FILE OPERATIONS ===

    def load_image(self):
        """Load image from file"""
        file_path = self.file_service.open_file_dialog()
        if not file_path:
            return

        result = self.file_service.load_image(file_path)
        if result is None:
            self.view.show_error("Lỗi", "Không thể mở ảnh. Vui lòng chọn file ảnh hợp lệ.")
            return

        image, path = result
        self.image_service.load_image(image, path)
        self._update_ui()
        self.view.update_status(f"Đã mở ảnh: {path}")

    def save_image(self):
        """Save current image to file"""
        if not self._check_image_loaded():
            return

        file_path = self.file_service.save_file_dialog()
        if not file_path:
            return

        image = self.image_service.get_current_image()
        success = self.file_service.save_image(image, file_path)

        if success:
            self.view.show_info("Thành công", f"Đã lưu ảnh: {file_path}")
            self.view.update_status(f"Đã lưu ảnh: {file_path}")
        else:
            self.view.show_error("Lỗi", "Không thể lưu ảnh.")

    def reset_image(self):
        """Reset image to original"""
        if not self._check_image_loaded():
            return

        self.image_service.reset_to_original()
        self._update_ui()
        self.view.update_status("Đã reset ảnh về trạng thái ban đầu")

    # === HISTORY OPERATIONS ===

    def undo_action(self):
        """Undo last operation"""
        if self.image_service.undo():
            self._update_ui()
            self.view.update_status("Đã hoàn tác thao tác trước")

    def redo_action(self):
        """Redo last undone operation"""
        if self.image_service.redo():
            self._update_ui()
            self.view.update_status("Đã làm lại thao tác")

    # === BLUR OPERATIONS ===

    def apply_average_blur(self):
        """Apply average blur"""
        processor = BlurProcessor(BlurType.AVERAGE)
        self._apply_processor(processor, "Đã áp dụng làm mờ trung bình")

    def apply_gaussian_blur(self):
        """Apply Gaussian blur"""
        processor = BlurProcessor(BlurType.GAUSSIAN)
        self._apply_processor(processor, "Đã áp dụng làm mờ Gaussian")

    def apply_median_blur(self):
        """Apply median blur"""
        processor = BlurProcessor(BlurType.MEDIAN)
        self._apply_processor(processor, "Đã áp dụng làm mờ trung vị")

    def apply_bilateral_blur(self):
        """Apply bilateral blur"""
        processor = BlurProcessor(BlurType.BILATERAL)
        self._apply_processor(processor, "Đã áp dụng làm mờ bilateral")

    # === BRIGHTNESS OPERATIONS ===

    def increase_brightness(self):
        """Increase brightness"""
        processor = BrightnessProcessor(BrightnessOperation.INCREASE)
        self._apply_processor(processor, "Đã tăng độ sáng")

    def decrease_brightness(self):
        """Decrease brightness"""
        processor = BrightnessProcessor(BrightnessOperation.DECREASE)
        self._apply_processor(processor, "Đã giảm độ sáng")

    def increase_contrast(self):
        """Increase contrast"""
        config = ProcessorConfig()
        config.set('alpha', 1.3)
        config.set('beta', 0)
        processor = BrightnessProcessor(BrightnessOperation.CONTRAST, config)
        self._apply_processor(processor, "Đã tăng độ tương phản")

    # === SHARPEN OPERATIONS ===

    def apply_basic_sharpen(self):
        """Apply basic sharpening"""
        processor = SharpenProcessor(SharpenType.BASIC)
        self._apply_processor(processor, "Đã làm rõ nét cơ bản")

    def apply_laplacian_sharpen(self):
        """Apply Laplacian sharpening"""
        processor = SharpenProcessor(SharpenType.LAPLACIAN)
        self._apply_processor(processor, "Đã làm rõ nét Laplacian")

    def apply_unsharp_mask(self):
        """Apply unsharp mask"""
        processor = SharpenProcessor(SharpenType.UNSHARP_MASK)
        self._apply_processor(processor, "Đã làm rõ nét Unsharp Mask")

    def apply_detail_enhance(self):
        """Apply detail enhancement"""
        processor = SharpenProcessor(SharpenType.DETAIL_ENHANCE)
        self._apply_processor(processor, "Đã tăng cường chi tiết")

    # === EDGE DETECTION OPERATIONS ===

    def apply_roberts_edge(self):
        """Apply Roberts edge detection"""
        processor = EdgeDetectionProcessor(EdgeDetectionType.ROBERTS)
        self._apply_processor(processor, "Đã phát hiện viền Roberts")

    def apply_prewitt_edge(self):
        """Apply Prewitt edge detection"""
        processor = EdgeDetectionProcessor(EdgeDetectionType.PREWITT)
        self._apply_processor(processor, "Đã phát hiện viền Prewitt")

    def apply_sobel_edge(self):
        """Apply Sobel edge detection"""
        processor = EdgeDetectionProcessor(EdgeDetectionType.SOBEL)
        self._apply_processor(processor, "Đã phát hiện viền Sobel")

    def apply_canny_edge(self):
        """Apply Canny edge detection"""
        processor = EdgeDetectionProcessor(EdgeDetectionType.CANNY)
        self._apply_processor(processor, "Đã phát hiện viền Canny")

    def apply_laplacian_edge(self):
        """Apply Laplacian edge detection"""
        processor = EdgeDetectionProcessor(EdgeDetectionType.LAPLACIAN)
        self._apply_processor(processor, "Đã phát hiện viền Laplacian")

    def apply_scharr_edge(self):
        """Apply Scharr edge detection"""
        processor = EdgeDetectionProcessor(EdgeDetectionType.SCHARR)
        self._apply_processor(processor, "Đã phát hiện viền Scharr")

    # === TRANSFORM OPERATIONS ===

    def rotate_right_90(self):
        """Rotate right 90 degrees"""
        processor = TransformProcessor(TransformType.ROTATE_90_CW)
        self._apply_processor(processor, "Đã xoay phải 90°")

    def rotate_left_90(self):
        """Rotate left 90 degrees"""
        processor = TransformProcessor(TransformType.ROTATE_90_CCW)
        self._apply_processor(processor, "Đã xoay trái 90°")

    def rotate_180(self):
        """Rotate 180 degrees"""
        processor = TransformProcessor(TransformType.ROTATE_180)
        self._apply_processor(processor, "Đã xoay 180°")

    def flip_horizontal(self):
        """Flip horizontally"""
        processor = TransformProcessor(TransformType.FLIP_HORIZONTAL)
        self._apply_processor(processor, "Đã lật ngang")

    def flip_vertical(self):
        """Flip vertically"""
        processor = TransformProcessor(TransformType.FLIP_VERTICAL)
        self._apply_processor(processor, "Đã lật dọc")

    def zoom_in_image(self):
        """Zoom in"""
        processor = TransformProcessor(TransformType.ZOOM_IN)
        self._apply_processor(processor, "Đã phóng to")

    def zoom_out_image(self):
        """Zoom out"""
        processor = TransformProcessor(TransformType.ZOOM_OUT)
        self._apply_processor(processor, "Đã thu nhỏ")

    # === FACE BEAUTIFY ===

    def open_face_beautify_image(self):
        """Open face beautify window for image"""
        if not self._check_image_loaded():
            return

        try:
            from Views.FaceBeautifyImageView import FaceBeautifyImageView
            current_image = self.image_service.get_current_image()
            FaceBeautifyImageView(self, current_image)
        except Exception as e:
            self.view.show_error("Lỗi", f"Không thể mở cửa sổ làm đẹp:\n{e}")

    def open_face_beautify_camera(self):
        """Open face beautify window for camera"""
        try:
            from Views.FaceBeautifyCameraView import FaceBeautifyCameraView
            FaceBeautifyCameraView(self)
        except Exception as e:
            self.view.show_error("Lỗi", f"Không thể mở cửa sổ camera:\n{e}")

    def run(self):
        """Start the application"""
        self.view.run()
