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
        
        # Responsive window size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(1200, int(screen_width * 0.8))
        window_height = min(800, int(screen_height * 0.85))
        
        # Center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#f0f0f0")
        self.root.minsize(900, 600)
        
        # Biến lưu trữ ảnh
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_path = None
        
        # Lưu lịch sử để undo
        self.history = []
        
        # Status message
        self.status_message = ""
        
        # Trạng thái collapse của các section
        self.blur_collapsed = True
        self.brightness_collapsed = True
        
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
        left_panel = tk.Frame(main_container, bg="white", width=320, relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Tạo scrollable frame cho buttons
        canvas = tk.Canvas(left_panel, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # === BUTTON CHỌN ẢNH ===
        self.create_button(
            scrollable_frame,
            text="📁 Chọn Ảnh",
            command=self.load_image,
            bg="#3498db",
            font_size=13,
            bold=True,
            pady_top=15
        )
        
        self.create_separator(scrollable_frame)
        
        # === NHÓM LÀM MỜ (COLLAPSIBLE) ===
        self.blur_frame = self.create_collapsible_section(
            scrollable_frame,
            "🌫️ LÀM MỜ ẢNH",
            [
                ("Làm Mờ Trung Bình", self.apply_average_blur, "#9b59b6"),
                ("Làm Mờ Gaussian", self.apply_gaussian_blur, "#8e44ad"),
                ("Làm Mờ Trung Vị", self.apply_median_blur, "#7d3c98"),
                ("Làm Mờ Bilateral", self.apply_bilateral_blur, "#6c3483"),
            ],
            "blur"
        )
        
        # === NHÓM ĐỘ SÁNG (COLLAPSIBLE) ===
        self.brightness_frame = self.create_collapsible_section(
            scrollable_frame,
            "💡 ĐỘ SÁNG",
            [
                ("Làm Sáng Ảnh", self.increase_brightness, "#f39c12"),
                ("Làm Tối Ảnh", self.decrease_brightness, "#e67e22"),
                ("Tăng Tương Phản", self.increase_contrast, "#d68910"),
            ],
            "brightness"
        )
        
        self.create_separator(scrollable_frame)
        
        # === NÚT ĐIỀU KHIỂN ===
        control_frame = tk.Frame(scrollable_frame, bg="white")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Reset button
        reset_color = "#e74c3c"
        reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset",
            command=self.reset_image,
            font=("Arial", 11, "bold"),
            bg=reset_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=14,
            activebackground=self.darken_color(reset_color)
        )
        reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg=self.lighten_color(reset_color)))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg=reset_color))
        
        # Save button
        save_color = "#27ae60"
        save_btn = tk.Button(
            control_frame,
            text="💾 Lưu",
            command=self.save_image,
            font=("Arial", 11, "bold"),
            bg=save_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=14,
            activebackground=self.darken_color(save_color)
        )
        save_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=self.lighten_color(save_color)))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=save_color))
        
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
        
        # === STATUS BAR ===
        status_frame = tk.Frame(self.root, bg="#34495e", height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="Sẵn sàng - Vui lòng chọn ảnh để bắt đầu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=8)
    
    def create_button(self, parent, text, command, bg, font_size=11, bold=False, pady_top=5):
        """Helper method để tạo button dễ dàng"""
        font_style = ("Arial", font_size, "bold" if bold else "normal")
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=font_style,
            bg=bg,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            activebackground=self.darken_color(bg),
            activeforeground="white"
        )
        btn.pack(fill=tk.X, padx=15, pady=(pady_top, 5))
        
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=self.lighten_color(bg)))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn
    
    def lighten_color(self, hex_color):
        """Làm sáng màu lên một chút"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * 1.1))
        g = min(255, int(g * 1.1))
        b = min(255, int(b * 1.1))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def darken_color(self, hex_color):
        """Làm tối màu xuống một chút"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_separator(self, parent):
        """Helper method để tạo separator"""
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill=tk.X, padx=15, pady=10)
        return separator
    
    def create_section_label(self, parent, text):
        """Helper method để tạo section label"""
        label = tk.Label(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        label.pack(pady=(10, 5))
        return label
    
    def create_collapsible_section(self, parent, title, buttons, section_name):
        """Tạo section có thể thu gọn/mở rộng"""
        # Container cho toàn bộ section
        section_container = tk.Frame(parent, bg="white")
        section_container.pack(fill=tk.X, padx=10, pady=5)
        
        # Header có thể click
        header_frame = tk.Frame(section_container, bg="#ecf0f1", relief=tk.RAISED, borderwidth=1)
        header_frame.pack(fill=tk.X)
        
        # Icon và title
        arrow = "▼" if getattr(self, f"{section_name}_collapsed") else "▶"
        header_btn = tk.Button(
            header_frame,
            text=f"{arrow} {title}",
            command=lambda: self.toggle_section(section_name, content_frame, header_btn, title),
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            relief=tk.FLAT,
            cursor="hand2",
            anchor="w",
            padx=10
        )
        header_btn.pack(fill=tk.X, pady=5)
        
        # Content frame (chứa các button)
        content_frame = tk.Frame(section_container, bg="white")
        if not getattr(self, f"{section_name}_collapsed"):
            content_frame.pack(fill=tk.X, pady=5)
        
        # Tạo các button
        for text, command, color in buttons:
            btn = tk.Button(
                content_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=1,
                activebackground=self.darken_color(color),
                activeforeground="white"
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.lighten_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        return content_frame
    
    def toggle_section(self, section_name, content_frame, header_btn, title):
        """Toggle hiển thị/ẩn section"""
        is_collapsed = getattr(self, f"{section_name}_collapsed")
        
        if is_collapsed:
            # Mở rộng
            content_frame.pack(fill=tk.X, pady=5)
            header_btn.config(text=f"▼ {title}")
            setattr(self, f"{section_name}_collapsed", False)
        else:
            # Thu gọn
            content_frame.pack_forget()
            header_btn.config(text=f"▶ {title}")
            setattr(self, f"{section_name}_collapsed", True)
    
    def save_to_history(self):
        """Lưu trạng thái hiện tại vào history"""
        if self.current_image is not None:
            # Giới hạn history ở 10 bước
            if len(self.history) >= 10:
                self.history.pop(0)
            self.history.append(self.current_image.copy())
    
    def update_status(self, message):
        """Cập nhật status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
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
                self.history.clear()
                
                # Hiển thị ảnh
                self.display_current_image()
                self.update_status(f"✓ Đã tải ảnh: {file_path.split('/')[-1]}")
                
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
        
        self.save_to_history()
        self.current_image = Blur.apply_average_blur(self.current_image, kernel_size=(15, 15))
        self.display_current_image()
        self.update_status("✓ Đã áp dụng làm mờ trung bình")
    
    def apply_gaussian_blur(self):
        """Áp dụng làm mờ Gaussian"""
        if not self.check_image_loaded():
            return
        
        self.save_to_history()
        self.current_image = Blur.apply_gaussian_blur(self.current_image, kernel_size=(15, 15), sigma=3)
        self.display_current_image()
        self.update_status("✓ Đã áp dụng làm mờ Gaussian")
    
    def apply_median_blur(self):
        """Áp dụng làm mờ trung vị"""
        if not self.check_image_loaded():
            return
        
        self.save_to_history()
        self.current_image = Blur.apply_median_blur(self.current_image, kernel_size=15)
        self.display_current_image()
        self.update_status("✓ Đã áp dụng làm mờ trung vị")
    
    def apply_bilateral_blur(self):
        """Áp dụng làm mờ Bilateral"""
        if not self.check_image_loaded():
            return
        
        self.save_to_history()
        self.current_image = Blur.apply_bilateral_blur(self.current_image, d=15, sigma_color=80, sigma_space=80)
        self.display_current_image()
        self.update_status("✓ Đã áp dụng làm mờ Bilateral")
    
    # === CÁC HÀM XỬ LÝ ĐỘ SÁNG ===
    
    def increase_brightness(self):
        """Làm sáng ảnh"""
        if not self.check_image_loaded():
            return
        
        self.save_to_history()
        self.current_image = Brightness.increase_brightness(self.current_image, value=50)
        self.display_current_image()
        self.update_status("✓ Đã làm sáng ảnh")
    
    def decrease_brightness(self):
        """Làm tối ảnh"""
        if not self.check_image_loaded():
            return
        
        self.save_to_history()
        self.current_image = Brightness.decrease_brightness(self.current_image, value=50)
        self.display_current_image()
        self.update_status("✓ Đã làm tối ảnh")
    
    def increase_contrast(self):
        """Tăng tương phản"""
        if not self.check_image_loaded():
            return
        
        self.save_to_history()
        self.current_image = Brightness.adjust_contrast_brightness(self.current_image, alpha=1.5, beta=0)
        self.display_current_image()
        self.update_status("✓ Đã tăng tương phản")
    
    # === CÁC HÀM KHÁC ===
    
    def reset_image(self):
        """Khôi phục ảnh gốc"""
        if not self.check_image_loaded():
            return
        
        self.history.clear()
        self.current_image = self.original_image.copy()
        self.display_current_image()
        self.update_status("🔄 Đã reset về ảnh gốc")
    
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
                self.update_status(f"💾 Đã lưu ảnh: {file_path.split('/')[-1]}")
            except Exception as e:
                self.update_status(f"❌ Lỗi: {str(e)}")


def main():
    """Hàm chính để chạy ứng dụng"""
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
