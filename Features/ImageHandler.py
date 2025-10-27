# -*- coding: utf-8 -*-
"""
ImageHandler.py - Xử lý các thao tác với ảnh (load, display, save)
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox


def load_image_from_file():
    file_path = filedialog.askopenfilename(
        title="Chọn ảnh",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        try:
            # Đọc ảnh bằng OpenCV
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError("Không thể đọc ảnh")
            return image, file_path
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")
            return None, None
    
    return None, None


def save_image_to_file(image):
    file_path = filedialog.asksaveasfilename(
        title="Lưu ảnh",
        defaultextension=".jpg",
        filetypes=[
            ("JPEG", "*.jpg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        try:
            cv2.imwrite(file_path, image)
            return True, file_path
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {str(e)}")
            return False, None
    
    return False, None


def convert_to_display_image(image, max_width=850, max_height=650):
    if image is None:
        return None
    
    # Chuyển đổi từ BGR sang RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize ảnh để vừa với khung hiển thị
    h, w = image_rgb.shape[:2]
    aspect_ratio = w / h
    
    if w > max_width or h > max_height:
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        image_rgb = cv2.resize(image_rgb, (new_width, new_height))
    
    # Chuyển sang PIL Image
    pil_image = Image.fromarray(image_rgb)
    
    # Chuyển sang PhotoImage
    photo_image = ImageTk.PhotoImage(pil_image)
    
    return photo_image


class ImageHistory:
    """Quản lý lịch sử ảnh với tính năng hoàn tác/redo."""

    def __init__(self, max_history=20):
        self.max_history = max_history
        self.undo_stack = []
        self.redo_stack = []

    def set_initial(self, image):
        """Thiết lập trạng thái ban đầu khi mở/reset ảnh."""
        self.undo_stack = []
        self.redo_stack = []
        if image is not None:
            self.undo_stack.append(image.copy())

    def push_state(self, image):
        """Lưu trạng thái mới sau mỗi lần chỉnh sửa."""
        if image is None:
            return

        if self.undo_stack and np.array_equal(image, self.undo_stack[-1]):
            # Không lưu nếu ảnh không thay đổi
            self.redo_stack.clear()
            return

        self.undo_stack.append(image.copy())
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def clear(self):
        self.undo_stack = []
        self.redo_stack = []

    def get_last(self):
        if self.undo_stack:
            return self.undo_stack[-1].copy()
        return None

    def undo(self, current_image):
        """Hoàn tác về trạng thái trước đó."""
        if len(self.undo_stack) <= 1:
            return None

        if current_image is not None:
            self.redo_stack.append(current_image.copy())

        self.undo_stack.pop()
        return self.undo_stack[-1].copy()

    def redo(self):
        """Làm lại bước vừa hoàn tác."""
        if not self.redo_stack:
            return None

        restored = self.redo_stack.pop()
        self.undo_stack.append(restored.copy())
        return restored.copy()
