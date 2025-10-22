# -*- coding: utf-8 -*-
"""
App.py - Ứng dụng chỉnh sửa ảnh với giao diện GUI
Các chức năng: Làm mờ, Làm sáng, Làm tối
"""

import tkinter as tk
from tkinter import messagebox
from Features import Blur, Brightness, ImageHandler
from UI import Button, Section, Layout, Colors


class ImageEditorApp:
    """Class quản lý giao diện ứng dụng chỉnh sửa ảnh"""
    
    def __init__(self, root):
        self.root = root
        
        # Thiết lập cửa sổ
        Layout.setup_window(self.root, "Ứng Dụng Chỉnh Sửa Ảnh - Nhóm 4")
        
        # Biến lưu trữ ảnh
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_path = None
        
        # Lưu lịch sử để undo
        self.history = ImageHandler.ImageHistory(max_history=10)
        
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
        Layout.create_header(self.root)
        
        # === MAIN CONTAINER ===
        main_container = Layout.create_main_container(self.root)
        
        # === LEFT PANEL - Buttons ===
        left_panel = Layout.create_left_panel(main_container)
        
        # Tạo scrollable frame cho buttons
        scrollable_frame = Layout.create_scrollable_frame(left_panel)
        
        # === BUTTON CHỌN ẢNH ===
        Button.create_button(
            scrollable_frame,
            text="📁 Chọn Ảnh",
            command=self.load_image,
            bg=Colors.get_color('primary'),
            font_size=13,
            bold=True,
            pady_top=15
        )
        
        Section.create_separator(scrollable_frame)
        
        # === NHÓM LÀM MỜ (COLLAPSIBLE) ===
        self.blur_frame = Section.create_collapsible_section(
            scrollable_frame,
            "🌫️ LÀM MỜ ẢNH",
            [
                ("Làm Mờ Trung Bình", self.apply_average_blur, Colors.get_color('blur_1')),
                ("Làm Mờ Gaussian", self.apply_gaussian_blur, Colors.get_color('blur_2')),
                ("Làm Mờ Trung Vị", self.apply_median_blur, Colors.get_color('blur_3')),
                ("Làm Mờ Bilateral", self.apply_bilateral_blur, Colors.get_color('blur_4')),
            ],
            "blur",
            self
        )
        
        # === NHÓM ĐỘ SÁNG (COLLAPSIBLE) ===
        self.brightness_frame = Section.create_collapsible_section(
            scrollable_frame,
            "💡 ĐỘ SÁNG",
            [
                ("Làm Sáng Ảnh", self.increase_brightness, Colors.get_color('bright_1')),
                ("Làm Tối Ảnh", self.decrease_brightness, Colors.get_color('bright_2')),
                ("Tăng Tương Phản", self.increase_contrast, Colors.get_color('bright_3')),
            ],
            "brightness",
            self
        )
        
        Section.create_separator(scrollable_frame)
        
        # === NÚT ĐIỀU KHIỂN ===
        control_frame = Layout.create_control_frame(scrollable_frame)
        
        # Reset button
        reset_btn = Button.create_control_button(
            control_frame,
            text="🔄 Reset",
            command=self.reset_image,
            bg=Colors.get_color('danger')
        )
        reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save button
        save_btn = Button.create_control_button(
            control_frame,
            text="💾 Lưu",
            command=self.save_image,
            bg=Colors.get_color('success')
        )
        save_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # === RIGHT PANEL - Image Display ===
        right_panel = Layout.create_right_panel(main_container)
        
        # Label hiển thị ảnh
        self.image_label = Layout.create_image_label(right_panel)
        
        # === STATUS BAR ===
        self.status_label = Layout.create_status_bar(self.root)
    
    def save_to_history(self):
        """Lưu trạng thái hiện tại vào history"""
        self.history.save(self.current_image)
    
    def update_status(self, message):
        """Cập nhật status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def load_image(self):
        """Chọn và tải ảnh từ file"""
        image, file_path = ImageHandler.load_image_from_file()
        
        if image is not None:
            self.original_image = image
            self.current_image = self.original_image.copy()
            self.image_path = file_path
            self.history.clear()
            
            # Hiển thị ảnh
            self.display_current_image()
            self.update_status(f"✓ Đã tải ảnh: {file_path.split('/')[-1]}")
    
    def display_current_image(self):
        """Hiển thị ảnh hiện tại lên giao diện"""
        if self.current_image is None:
            return
        
        # Chuyển đổi sang PhotoImage
        self.display_image = ImageHandler.convert_to_display_image(
            self.current_image,
            max_width=850,
            max_height=650
        )
        
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
        
        success, file_path = ImageHandler.save_image_to_file(self.current_image)
        
        if success:
            self.update_status(f"💾 Đã lưu ảnh: {file_path.split('/')[-1]}")


def main():
    """Hàm chính để chạy ứng dụng"""
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
