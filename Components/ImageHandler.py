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
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
    
    def save(self, image):
        if image is not None:
            if len(self.history) >= self.max_history:
                self.history.pop(0)
            self.history.append(image.copy())
    
    def clear(self):
        self.history.clear()
    
    def get_last(self):
        if self.history:
            return self.history[-1]
        return None
    
    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            return self.history[-1].copy()
        elif len(self.history) == 1:
            return self.history[0].copy()
        return None
