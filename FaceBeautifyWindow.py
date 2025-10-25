# -*- coding: utf-8 -*-
"""
FaceBeautifyWindow.py - Cửa sổ làm đẹp khuôn mặt từ ảnh (không phải camera)
Copy file này vào: thư mục gốc (cùng cấp với App.py)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from Features import FaceBeautify


class FaceBeautifyWindow:
    """Cửa sổ riêng cho chức năng nhận diện và làm đẹp khuôn mặt từ ảnh"""
    
    def __init__(self, parent, original_image):
        """
        parent: cửa sổ cha (App)
        original_image: ảnh gốc từ App chính
        """
        self.parent = parent
        self.original_image = original_image.copy() if original_image is not None else None
        self.current_image = original_image.copy() if original_image is not None else None
        self.display_image = None
        self.faces = []
        
        # Giá trị mặc định
        self.DEFAULT_SMOOTH = 0.5
        self.DEFAULT_BRIGHTNESS = 20
        self.DEFAULT_CONTRAST = 1.2
        
        # Tạo cửa sổ mới
        self.window = tk.Toplevel(parent.root)
        self.window.title("Nhận Diện và Làm Đẹp Khuôn Mặt - Từ Ảnh")
        self.window.geometry("1000x700")
        self.window.configure(bg="#f0f0f0")
        
        # Biến trạng thái
        self.smooth_level = tk.DoubleVar(value=self.DEFAULT_SMOOTH)
        self.brightness_value = tk.IntVar(value=self.DEFAULT_BRIGHTNESS)
        self.contrast_value = tk.DoubleVar(value=self.DEFAULT_CONTRAST)
        
        self.create_widgets()
        
        if self.original_image is not None:
            self.detect_faces_auto()
    
    def create_widgets(self):
        """Tạo giao diện cho cửa sổ"""
        
        # Header
        header = tk.Frame(self.window, bg="#2c3e50", height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title = tk.Label(
            header,
            text="👤 NHẬN DIỆN VÀ LÀM ĐẸP KHUÔN MẶT - TỪ ẢNH",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=20)
        
        # Main container
        main = tk.Frame(self.window, bg="#f0f0f0")
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel
        left_panel = tk.Frame(main, bg="white", width=280, relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Scrollable frame
        canvas = tk.Canvas(left_panel, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        tk.Label(scroll_frame, text="🔍 NHẬN DIỆN", font=("Arial", 12, "bold"),
                bg="white", fg="#2c3e50").pack(pady=(15, 10))
        
        self.create_button(scroll_frame, "Nhận Diện Khuôn Mặt", 
                          self.detect_faces_manual, "#3498db")
        self.create_button(scroll_frame, "Xóa Khung Nhận Diện", 
                          self.clear_detection, "#e74c3c")
        
        ttk.Separator(scroll_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        tk.Label(scroll_frame, text="✨ LÀM ĐẸP TỰ ĐỘNG", font=("Arial", 12, "bold"),
                bg="white", fg="#2c3e50").pack(pady=(5, 10))
        
        self.create_button(scroll_frame, "Làm Đẹp Tự Động", 
                          self.auto_beautify, "#27ae60")
        
        ttk.Separator(scroll_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        tk.Label(scroll_frame, text="🎨 ĐIỀU CHỈNH CHI TIẾT", font=("Arial", 12, "bold"),
                bg="white", fg="#2c3e50").pack(pady=(5, 10))
        
        # Sliders
        self.create_slider_control(scroll_frame, "Làm Mịn Da:", 
                                   self.smooth_level, 0.0, 1.0, self.apply_smooth_skin)
        self.create_slider_control(scroll_frame, "Độ Sáng:", 
                                   self.brightness_value, 0, 50, self.apply_brighten, resolution=1)
        self.create_slider_control(scroll_frame, "Tương Phản:", 
                                   self.contrast_value, 1.0, 2.0, self.apply_contrast)
        
        # Nút Reset (gộp cả ảnh và giá trị)
        reset_btn = tk.Button(
            scroll_frame, 
            text="🔄 Reset Giá Trị Mặc Định",
            command=self.reset_to_default,
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=2
        )
        reset_btn.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Separator(scroll_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        tk.Label(scroll_frame, text="🌟 HIỆU ỨNG", font=("Arial", 12, "bold"),
                bg="white", fg="#2c3e50").pack(pady=(5, 10))
        
        self.create_button(scroll_frame, "Làm Mờ Nền", self.apply_blur_bg, "#9b59b6")
        self.create_button(scroll_frame, "Filter Mềm Mại", self.apply_soft_filter, "#f39c12")
        self.create_button(scroll_frame, "Giảm Tì Vết", self.apply_remove_blemishes, "#1abc9c")
        
        ttk.Separator(scroll_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Nút Áp Dụng
        apply_btn = tk.Button(
            scroll_frame,
            text="✅ Áp Dụng Vào Ảnh Chính",
            command=self.apply_changes,
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=2
        )
        apply_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Right panel
        right_panel = tk.Frame(main, bg="white", relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(
            right_panel,
            text="Đang chờ xử lý...",
            font=("Arial", 14),
            bg="white",
            fg="#95a5a6"
        )
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Status bar
        status_frame = tk.Frame(self.window, bg="#34495e", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="Sẵn sàng",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
    
    def create_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command, font=("Arial", 10),
                       bg=color, fg="white", relief=tk.FLAT, cursor="hand2", height=2)
        btn.pack(fill=tk.X, padx=10, pady=5)
        return btn
    
    def create_control_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
                       bg=color, fg="white", relief=tk.FLAT, cursor="hand2", width=12)
        return btn
    
    def create_slider_control(self, parent, label_text, variable, from_, to, command, resolution=0.1):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.X, padx=10, pady=8)
        
        label = tk.Label(frame, text=label_text, font=("Arial", 9),
                        bg="white", fg="#2c3e50")
        label.pack(anchor="w")
        
        slider = ttk.Scale(frame, from_=from_, to=to, variable=variable,
                          orient=tk.HORIZONTAL, command=lambda v: command())
        slider.pack(fill=tk.X, pady=5)
        
        value_label = tk.Label(frame, textvariable=variable, font=("Arial", 8),
                              bg="white", fg="#7f8c8d")
        value_label.pack(anchor="e")
        
        return slider
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.window.update_idletasks()
    
    def display_current_image(self):
        if self.current_image is None:
            return
        
        image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        h, w = image_rgb.shape[:2]
        
        max_width, max_height = 700, 550
        aspect = w / h
        
        if w > max_width or h > max_height:
            if aspect > 1:
                new_w = max_width
                new_h = int(max_width / aspect)
            else:
                new_h = max_height
                new_w = int(max_height * aspect)
            image_rgb = cv2.resize(image_rgb, (new_w, new_h))
        
        pil_image = Image.fromarray(image_rgb)
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        self.image_label.configure(image=self.display_image, text="")
        self.image_label.image = self.display_image
    
    def check_image(self):
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Không có ảnh để xử lý!")
            return False
        return True
    
    def check_faces_detected(self):
        if len(self.faces) == 0:
            messagebox.showwarning("Cảnh báo", 
                                 "Chưa nhận diện khuôn mặt!\nVui lòng nhấn 'Nhận Diện Khuôn Mặt' trước.")
            return False
        return True
    
    def detect_faces_auto(self):
        if not self.check_image():
            return
        
        self.faces = FaceBeautify.detect_faces(self.current_image)
        
        if len(self.faces) > 0:
            self.current_image = FaceBeautify.draw_face_rectangles(self.current_image, self.faces)
            self.display_current_image()
            self.update_status(f"✓ Đã tìm thấy {len(self.faces)} khuôn mặt")
        else:
            self.display_current_image()
            self.update_status("⚠ Không tìm thấy khuôn mặt nào")
    
    def detect_faces_manual(self):
        if not self.check_image():
            return
        
        self.current_image = self.original_image.copy()
        self.faces = FaceBeautify.detect_faces(self.current_image)
        
        if len(self.faces) > 0:
            self.current_image = FaceBeautify.draw_face_rectangles(self.current_image, self.faces)
            self.display_current_image()
            self.update_status(f"✓ Đã tìm thấy {len(self.faces)} khuôn mặt")
            messagebox.showinfo("Thành công", f"Đã tìm thấy {len(self.faces)} khuôn mặt!")
        else:
            self.display_current_image()
            self.update_status("⚠ Không tìm thấy khuôn mặt")
            messagebox.showwarning("Thông báo", "Không tìm thấy khuôn mặt nào trong ảnh!")
    
    def clear_detection(self):
        if not self.check_image():
            return
        
        self.current_image = self.original_image.copy()
        self.faces = []
        self.display_current_image()
        self.update_status("Đã xóa khung nhận diện")
    
    def auto_beautify(self):
        if not self.check_image() or not self.check_faces_detected():
            return
        
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.beautify_face_auto(self.current_image, self.faces)
        self.display_current_image()
        self.update_status("✓ Đã áp dụng làm đẹp tự động")
    
    def apply_smooth_skin(self):
        if not self.check_image() or not self.check_faces_detected():
            return
        
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.smooth_skin(self.current_image, self.faces, 
                                                      smooth_level=self.smooth_level.get())
        self.display_current_image()
        self.update_status(f"✓ Làm mịn da: {self.smooth_level.get():.2f}")
    
    def apply_brighten(self):
        if not self.check_image() or not self.check_faces_detected():
            return
        
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.brighten_face(self.current_image, self.faces, 
                                                        brightness_value=self.brightness_value.get())
        self.display_current_image()
        self.update_status(f"✓ Độ sáng: {self.brightness_value.get()}")
    
    def apply_contrast(self):
        if not self.check_image() or not self.check_faces_detected():
            return
        
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.enhance_face_contrast(self.current_image, self.faces, 
                                                                contrast=self.contrast_value.get())
        self.display_current_image()
        self.update_status(f"✓ Tương phản: {self.contrast_value.get():.2f}")
    
    def apply_blur_bg(self):
        if not self.check_image() or not self.check_faces_detected():
            return
        
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.apply_blur_background(self.current_image, self.faces)
        self.display_current_image()
        self.update_status("✓ Đã làm mờ nền")
    
    def apply_soft_filter(self):
        if not self.check_image():
            return
        
        # Copy từ ảnh gốc để xóa khung nhận diện
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.add_soft_filter(self.current_image, intensity=0.3)
        self.display_current_image()
        self.update_status("✓ Đã áp dụng filter mềm mại")
    
    def apply_remove_blemishes(self):
        if not self.check_image() or not self.check_faces_detected():
            return
        
        self.current_image = self.original_image.copy()
        self.current_image = FaceBeautify.remove_blemishes(self.current_image, self.faces)
        self.display_current_image()
        self.update_status("✓ Đã giảm tì vết")
    
    def reset_to_default(self):
        """Reset ảnh về gốc và các giá trị về mặc định (giữ lại kết quả nhận diện)"""
        if not self.check_image():
            return
        
        # Reset ảnh về gốc
        self.current_image = self.original_image.copy()
        
        # Giữ lại kết quả nhận diện (self.faces), vẽ lại khung nếu có
        if len(self.faces) > 0:
            self.current_image = FaceBeautify.draw_face_rectangles(self.current_image, self.faces)
        
        # Reset giá trị slider
        self.smooth_level.set(self.DEFAULT_SMOOTH)
        self.brightness_value.set(self.DEFAULT_BRIGHTNESS)
        self.contrast_value.set(self.DEFAULT_CONTRAST)
        
        self.display_current_image()
        self.update_status(f"🔄 Đã reset về ảnh gốc và giá trị mặc định (giữ {len(self.faces)} khuôn mặt đã nhận diện)")
    

    def apply_changes(self):
        if not self.check_image():
            return
        
        result = messagebox.askyesno(
            "Xác nhận",
            "Áp dụng các thay đổi vào ảnh chính?\n(Ảnh trong cửa sổ chính sẽ được cập nhật)"
        )
        
        if result:
            self.parent.current_image = self.current_image.copy()
            self.parent.display_current_image()
            self.parent.update_status("✓ Đã áp dụng làm đẹp khuôn mặt")
            
            self.update_status("✅ Đã áp dụng vào ảnh chính")
            messagebox.showinfo("Thành công", "Đã áp dụng các thay đổi vào ảnh chính!")
            
            self.window.destroy()