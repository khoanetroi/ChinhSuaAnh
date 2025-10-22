# -*- coding: utf-8 -*-
"""
App.py - Ứng dụng chỉnh sửa ảnh với giao diện GUI
Các chức năng: Làm mờ, Làm sáng, Làm tối
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from Components import Blur, Brightness


class ImageEditorApp:
    """Class quản lý giao diện ứng dụng chỉnh sửa ảnh"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Chỉnh Sửa Ảnh - Nhóm 4")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Biến lưu trữ ảnh
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_path = None
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        
        # === HEADER ===
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(
            header_frame, 
            text="🎨 ỨNG DỤNG CHỈNH SỬA ẢNH", 
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # === MAIN CONTAINER ===
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === LEFT PANEL - Buttons ===
        left_panel = tk.Frame(main_container, bg="white", width=300, relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Button chọn ảnh
        btn_load = tk.Button(
            left_panel,
            text="📁 Chọn Ảnh",
            command=self.load_image,
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=2
        )
        btn_load.pack(fill=tk.X, padx=15, pady=(20, 10))
        
        # Separator
        separator1 = ttk.Separator(left_panel, orient='horizontal')
        separator1.pack(fill=tk.X, padx=15, pady=10)
        
        # === NHÓM LÀM MỜ ===
        blur_label = tk.Label(
            left_panel,
            text="🌫️ LÀM MỜ ẢNH",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        blur_label.pack(pady=(10, 5))
        
        blur_buttons = [
            ("Làm Mờ Trung Bình", self.apply_average_blur, "#9b59b6"),
            ("Làm Mờ Gaussian", self.apply_gaussian_blur, "#8e44ad"),
            ("Làm Mờ Trung Vị", self.apply_median_blur, "#7d3c98"),
            ("Làm Mờ Bilateral", self.apply_bilateral_blur, "#6c3483"),
        ]
        
        for text, command, color in blur_buttons:
            btn = tk.Button(
                left_panel,
                text=text,
                command=command,
                font=("Arial", 11),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=2
            )
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        # Separator
        separator2 = ttk.Separator(left_panel, orient='horizontal')
        separator2.pack(fill=tk.X, padx=15, pady=10)
        
        # === NHÓM ĐỘ SÁNG ===
        brightness_label = tk.Label(
            left_panel,
            text="💡 ĐỘ SÁNG",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        brightness_label.pack(pady=(10, 5))
        
        brightness_buttons = [
            ("Làm Sáng Ảnh", self.increase_brightness, "#f39c12"),
            ("Làm Tối Ảnh", self.decrease_brightness, "#e67e22"),
            ("Tăng Tương Phản", self.increase_contrast, "#d68910"),
        ]
        
        for text, command, color in brightness_buttons:
            btn = tk.Button(
                left_panel,
                text=text,
                command=command,
                font=("Arial", 11),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=2
            )
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        # Separator
        separator3 = ttk.Separator(left_panel, orient='horizontal')
        separator3.pack(fill=tk.X, padx=15, pady=10)
        
        # === NHÓM KHÁC ===
        other_buttons = [
            ("🔄 Khôi Phục Ảnh Gốc", self.reset_image, "#27ae60"),
            ("💾 Lưu Ảnh", self.save_image, "#16a085"),
        ]
        
        for text, command, color in other_buttons:
            btn = tk.Button(
                left_panel,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=2
            )
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        # === RIGHT PANEL - Image Display ===
        right_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Label hiển thị ảnh
        self.image_label = tk.Label(
            right_panel,
            text="Chưa có ảnh\n\n📷\n\nVui lòng chọn ảnh để bắt đầu",
            font=("Arial", 16),
            bg="white",
            fg="#95a5a6"
        )
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # === FOOTER ===
        footer_frame = tk.Frame(self.root, bg="#34495e", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2024 Ứng Dụng Chỉnh Sửa Ảnh - Nhóm 4",
            font=("Arial", 10),
            bg="#34495e",
            fg="white"
        )
        footer_label.pack(pady=10)
    
    def load_image(self):
        """Chọn và tải ảnh từ file"""
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
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise ValueError("Không thể đọc ảnh")
                
                self.current_image = self.original_image.copy()
                self.image_path = file_path
                
                # Hiển thị ảnh
                self.display_current_image()
                messagebox.showinfo("Thành công", "Đã tải ảnh thành công!")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")
    
    def display_current_image(self):
        """Hiển thị ảnh hiện tại lên giao diện"""
        if self.current_image is None:
            return
        
        # Chuyển đổi từ BGR sang RGB
        image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        
        # Resize ảnh để vừa với khung hiển thị
        display_width = 850
        display_height = 650
        
        h, w = image_rgb.shape[:2]
        aspect_ratio = w / h
        
        if w > display_width or h > display_height:
            if aspect_ratio > 1:
                new_width = display_width
                new_height = int(display_width / aspect_ratio)
            else:
                new_height = display_height
                new_width = int(display_height * aspect_ratio)
            
            image_rgb = cv2.resize(image_rgb, (new_width, new_height))
        
        # Chuyển sang PIL Image
        pil_image = Image.fromarray(image_rgb)
        
        # Chuyển sang PhotoImage
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        # Cập nhật label
        self.image_label.configure(image=self.display_image, text="")
        self.image_label.image = self.display_image
    
    def check_image_loaded(self):
        """Kiểm tra xem đã tải ảnh chưa"""
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return False
        return True
    
    # === CÁC HÀM XỬ LÝ LÀM MỜ ===
    
    def apply_average_blur(self):
        """Áp dụng làm mờ trung bình"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Blur.apply_average_blur(self.current_image, kernel_size=(15, 15))
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã áp dụng làm mờ trung bình!")
    
    def apply_gaussian_blur(self):
        """Áp dụng làm mờ Gaussian"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Blur.apply_gaussian_blur(self.current_image, kernel_size=(15, 15), sigma=3)
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã áp dụng làm mờ Gaussian!")
    
    def apply_median_blur(self):
        """Áp dụng làm mờ trung vị"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Blur.apply_median_blur(self.current_image, kernel_size=15)
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã áp dụng làm mờ trung vị!")
    
    def apply_bilateral_blur(self):
        """Áp dụng làm mờ Bilateral"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Blur.apply_bilateral_blur(self.current_image, d=15, sigma_color=80, sigma_space=80)
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã áp dụng làm mờ Bilateral!")
    
    # === CÁC HÀM XỬ LÝ ĐỘ SÁNG ===
    
    def increase_brightness(self):
        """Làm sáng ảnh"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Brightness.increase_brightness(self.current_image, value=50)
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã làm sáng ảnh!")
    
    def decrease_brightness(self):
        """Làm tối ảnh"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Brightness.decrease_brightness(self.current_image, value=50)
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã làm tối ảnh!")
    
    def increase_contrast(self):
        """Tăng tương phản"""
        if not self.check_image_loaded():
            return
        
        self.current_image = Brightness.adjust_contrast_brightness(self.current_image, alpha=1.5, beta=0)
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã tăng tương phản!")
    
    # === CÁC HÀM KHÁC ===
    
    def reset_image(self):
        """Khôi phục ảnh gốc"""
        if not self.check_image_loaded():
            return
        
        self.current_image = self.original_image.copy()
        self.display_current_image()
        messagebox.showinfo("Thành công", "Đã khôi phục ảnh gốc!")
    
    def save_image(self):
        """Lưu ảnh đã chỉnh sửa"""
        if not self.check_image_loaded():
            return
        
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
                cv2.imwrite(file_path, self.current_image)
                messagebox.showinfo("Thành công", f"Đã lưu ảnh tại:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {str(e)}")


def main():
    """Hàm chính để chạy ứng dụng"""
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
