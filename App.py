# -*- coding: utf-8 -*-
"""
App.py - Ứng dụng chỉnh sửa ảnh chuyên nghiệp với giao diện GUI
Các chức năng: 
- Làm mờ & làm mịn ảnh
- Điều chỉnh độ sáng, tối, tương phản
- Lọc & khử nhiễu
- Làm rõ nét
- Tìm đường viền
- Cân bằng màu sắc
- Hiệu ứng đặc biệt
- Xoay & lật ảnh (MỚI!)
- Nhận diện và làm đẹp khuôn mặt
"""

import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
from Features import Blur, Brightness, ImageHandler, FaceBeautify, Sharpen, EdgeDetection, Histogram, Morphology, Transform
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
        
        # Lưu lịch sử để undo/redo
        self.history = ImageHandler.ImageHistory()
        self.undo_button = None
        self.redo_button = None
        self.icons = {}

        # Status message
        self.status_message = ""
        
        # Trạng thái collapse của các section
        self.blur_collapsed = True
        self.brightness_collapsed = True
        self.sharpen_collapsed = True
        self.edge_collapsed = True
        self.histogram_collapsed = True
        self.morphology_collapsed = True
        self.transform_collapsed = True
        
        # Nạp icon
        self.load_icons()

        # Tạo giao diện
        self.create_widgets()
        self.setup_shortcuts()
        self.update_history_controls()

    def load_icons(self):
        """Tạo icon lớn cho các nút điều khiển."""
        icon_size = 40
        circle_padding = 2
        arrow_margin = 7

        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def get_contrast_color(hex_color):
            r, g, b = hex_to_rgb(hex_color)
            brightness = 0.299 * r + 0.587 * g + 0.114 * b
            return "#102a43" if brightness > 170 else "#ffffff"

        def create_arrow_icon(base_color, direction="left"):
            background_color = Colors.darken_color(base_color, factor=0.85)
            arrow_color = get_contrast_color(base_color)

            img = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            draw.ellipse(
                (circle_padding, circle_padding, icon_size - circle_padding, icon_size - circle_padding),
                fill=background_color
            )

            center_x = icon_size // 2
            center_y = icon_size // 2
            arrow_width = icon_size - arrow_margin * 2
            arrow_height = icon_size // 2

            if direction == "left":
                points = [
                    (center_x + arrow_width // 2, center_y - arrow_height // 2),
                    (center_x - arrow_width // 6, center_y - arrow_height // 2),
                    (center_x - arrow_width // 6, center_y - arrow_height // 2 - arrow_margin),
                    (center_x - arrow_width // 2 - arrow_margin, center_y),
                    (center_x - arrow_width // 6, center_y + arrow_height // 2 + arrow_margin),
                    (center_x - arrow_width // 6, center_y + arrow_height // 2),
                    (center_x + arrow_width // 2, center_y + arrow_height // 2)
                ]
            else:
                points = [
                    (center_x - arrow_width // 2, center_y - arrow_height // 2),
                    (center_x + arrow_width // 6, center_y - arrow_height // 2),
                    (center_x + arrow_width // 6, center_y - arrow_height // 2 - arrow_margin),
                    (center_x + arrow_width // 2 + arrow_margin, center_y),
                    (center_x + arrow_width // 6, center_y + arrow_height // 2 + arrow_margin),
                    (center_x + arrow_width // 6, center_y + arrow_height // 2),
                    (center_x - arrow_width // 2, center_y + arrow_height // 2)
                ]

            draw.polygon(points, fill=arrow_color)
            return ImageTk.PhotoImage(img)

        undo_color = Colors.get_color('info') or '#118ab2'
        redo_color = Colors.get_color('warning') or '#ffd166'

        self.icons['undo'] = create_arrow_icon(undo_color, direction='left')
        self.icons['redo'] = create_arrow_icon(redo_color, direction='right')

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
            "LÀM MỜ ẢNH",
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
            "ĐỘ SÁNG",
            [
                ("Làm Sáng Ảnh", self.increase_brightness, Colors.get_color('bright_1')),
                ("Làm Tối Ảnh", self.decrease_brightness, Colors.get_color('bright_2')),
                ("Tăng Tương Phản", self.increase_contrast, Colors.get_color('bright_3')),
            ],
            "brightness",
            self
        )
        
        Section.create_separator(scrollable_frame)
        
        # === NHÓM LÀM RÕ NÉT (COLLAPSIBLE) ===
        self.sharpen_frame = Section.create_collapsible_section(
            scrollable_frame,
            "LÀM RÕ NÉT",
            [
                ("Làm Rõ Cơ Bản", self.apply_basic_sharpen, "#00796b"),
                ("Làm Rõ Mạnh", self.apply_laplacian_sharpen, "#00897b"),
                ("Làm Rõ Chuyên Nghiệp", self.apply_unsharp_mask, "#009688"),
                ("Tăng Chi Tiết", self.apply_detail_enhance, "#26a69a"),
            ],
            "sharpen",
            self
        )
        
        # === NHÓM PHÁT HIỆN BIÊN (COLLAPSIBLE) ===
        self.edge_frame = Section.create_collapsible_section(
            scrollable_frame,
            "TÌM ĐƯỜNG VIỀN",
            [
                ("Viền Cơ Bản (Roberts)", self.apply_roberts_edge, "#5d4037"),
                ("Viền Trung Bình (Prewitt)", self.apply_prewitt_edge, "#6d4c41"),
                ("Viền Mạnh (Sobel)", self.apply_sobel_edge, "#795548"),
                ("Viền Tự Động (Canny)", self.apply_canny_edge, "#8d6e63"),
            ],
            "edge",
            self
        )
        
        # === NHÓM HISTOGRAM (COLLAPSIBLE) ===
        self.histogram_frame = Section.create_collapsible_section(
            scrollable_frame,
            "CÂN BẰNG MÀU SẮC",
            [
                ("Cân Bằng Sáng Tối", self.apply_histogram_equalization, "#c2185b"),
                ("Cân Bằng Thông Minh", self.apply_clahe, "#d81b60"),
                ("Tăng Độ Tương Phản", self.apply_histogram_stretching, "#e91e63"),
                ("Tự Động Làm Đẹp", self.apply_auto_enhance, "#f06292"),
            ],
            "histogram",
            self
        )
        
        # === NHÓM HÌNH THÁI HỌC (COLLAPSIBLE) ===
        self.morphology_frame = Section.create_collapsible_section(
            scrollable_frame,
            "HIỆU ỨNG ĐẶC BIỆT",
            [
                ("Làm Mỏng", self.apply_erosion, "#1565c0"),
                ("Làm Dày", self.apply_dilation, "#1976d2"),
                ("Loại Nhiễu Nhỏ", self.apply_opening, "#1e88e5"),
                ("Lấp Lỗ Hổng", self.apply_closing, "#42a5f5"),
            ],
            "morphology",
            self
        )
        
        # === NHÓM XOAY & LẬT ẢNH (COLLAPSIBLE) ===
        self.transform_frame = Section.create_collapsible_section(
            scrollable_frame,
            "XOAY & LẬT ẢNH",
            [
                ("Xoay Phải 90°", self.rotate_right_90, "#ff6f00"),
                ("Xoay Trái 90°", self.rotate_left_90, "#ff8f00"),
                ("Xoay 180°", self.rotate_180, "#ffa726"),
                ("Lật Ngang", self.flip_horizontal, "#ffb74d"),
                ("Lật Dọc", self.flip_vertical, "#ffcc80"),
                ("Phóng To", self.zoom_in_image, "#fb8c00"),
                ("Thu Nhỏ", self.zoom_out_image, "#f57c00"),
            ],
            "transform",
            self
        )
        
        Section.create_separator(scrollable_frame)
        
        # === NHẬN DIỆN VÀ LÀM ĐẸP KHUÔN MẶT ===
        Button.create_button(
            scrollable_frame,
            text="📸 Làm Đẹp Từ Ảnh",
            command=self.open_face_beautify_image,
            bg="#e91e63",
            font_size=11,
            bold=True,
            pady_top=5
        )
        
        Button.create_button(
            scrollable_frame,
            text="📹 Làm Đẹp Từ Camera",
            command=self.open_face_beautify_camera,
            bg="#9c27b0",
            font_size=11,
            bold=True,
            pady_top=5
        )
        
        Section.create_separator(scrollable_frame)
        
        # === NÚT ĐIỀU KHIỂN ===
        control_frame = Layout.create_control_frame(scrollable_frame)

        button_bar = tk.Frame(control_frame, bg="#16213e")
        button_bar.pack(fill=tk.X, padx=5, pady=4)

        button_bar.grid_columnconfigure(0, weight=1, minsize=50)
        button_bar.grid_columnconfigure(1, weight=1, minsize=50)
        button_bar.grid_columnconfigure(2, weight=1, minsize=50)
        button_bar.grid_columnconfigure(3, weight=1, minsize=50)

        self.undo_button = Button.create_control_button(
            button_bar,
            text="",
            command=self.undo_action,
            bg=Colors.get_color('info'),
            width=12,
            image=self.icons.get('undo'),
            compound='center'
        )
        self.undo_button.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

        self.redo_button = Button.create_control_button(
            button_bar,
            text="",
            command=self.redo_action,
            bg=Colors.get_color('warning'),
            width=12,
            image=self.icons.get('redo'),
            compound='center'
        )
        self.redo_button.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

        self.reset_button = Button.create_control_button(
            button_bar,
            text="🔄 Reset",
            command=self.reset_image,
            bg=Colors.get_color('danger'),
            width=12
        )
        self.reset_button.grid(row=0, column=2, padx=6, pady=6, sticky="ew")

        self.save_button = Button.create_control_button(
            button_bar,
            text="💾 Lưu",
            command=self.save_image,
            bg=Colors.get_color('success'),
            width=12
        )
        self.save_button.grid(row=0, column=3, padx=6, pady=6, sticky="ew")
        
        # === RIGHT PANEL - Image Display ===
        right_panel = Layout.create_right_panel(main_container)
        
        # Label hiển thị ảnh
        self.image_label = Layout.create_image_label(right_panel)
        
        # === STATUS BAR ===
        self.status_label = Layout.create_status_bar(self.root)
    
    def update_status(self, message):
        """Cập nhật status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def apply_effect(self, operation, status_message, *args, **kwargs):
        """Thực thi hàm xử lý ảnh và cập nhật UI/lịch sử."""
        if not self.check_image_loaded():
            return

        try:
            new_image = operation(self.current_image, *args, **kwargs)
        except Exception as error:
            messagebox.showerror("Lỗi", f"Không thể áp dụng thao tác:\n{error}")
            return

        self.apply_and_update(new_image, status_message)

    def apply_and_update(self, new_image, status_message):
        """Cập nhật ảnh hiện tại và lưu lịch sử."""
        if new_image is None:
            messagebox.showwarning("Cảnh báo", "Không có thay đổi nào được áp dụng cho ảnh.")
            return

        self.current_image = new_image
        self.history.push_state(self.current_image)
        self.display_current_image()
        self.update_status(status_message)
        self.update_history_controls()

    def setup_shortcuts(self):
        """Đăng ký các phím tắt tiện dụng."""
        self.root.bind("<Control-o>", lambda event: self.load_image())
        self.root.bind("<Control-s>", lambda event: self.save_image())
        self.root.bind("<Control-z>", self.undo_action)
        self.root.bind("<Control-y>", self.redo_action)
        self.root.bind("<Control-Shift-Z>", self.redo_action)
        self.root.bind("<Control-r>", lambda event: self.reset_image())

    def update_history_controls(self):
        """Kích hoạt/vô hiệu các nút tùy theo trạng thái lịch sử."""
        if not all([self.undo_button, self.redo_button, self.reset_button, self.save_button]):
            return

        has_image = self.current_image is not None
        can_undo = len(self.history.undo_stack) > 1
        can_redo = len(self.history.redo_stack) > 0

        self.undo_button.config(state=tk.NORMAL if can_undo else tk.DISABLED)
        self.redo_button.config(state=tk.NORMAL if can_redo else tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL if has_image else tk.DISABLED)
        self.save_button.config(state=tk.NORMAL if has_image else tk.DISABLED)

    def undo_action(self, event=None):
        """Hoàn tác thao tác gần nhất."""
        if self.current_image is None:
            return "break"

        previous_image = self.history.undo(self.current_image)

        if previous_image is None:
            self.update_status("⚠️ Không còn bước để hoàn tác")
            self.update_history_controls()
            return "break"

        self.current_image = previous_image
        self.display_current_image()
        self.update_status("↩️ Đã hoàn tác")
        self.update_history_controls()
        return "break"

    def redo_action(self, event=None):
        """Làm lại thao tác đã hoàn tác."""
        if self.current_image is None:
            return "break"

        restored_image = self.history.redo()

        if restored_image is None:
            self.update_status("⚠️ Không có bước để làm lại")
            self.update_history_controls()
            return "break"

        self.current_image = restored_image
        self.display_current_image()
        self.update_status("↪️ Đã làm lại")
        self.update_history_controls()
        return "break"
    
    def load_image(self):
        """Chọn và tải ảnh từ file"""
        image, file_path = ImageHandler.load_image_from_file()

        if image is not None:
            self.original_image = image
            self.current_image = self.original_image.copy()
            self.image_path = file_path
            self.history.set_initial(self.current_image)

            # Hiển thị ảnh
            self.display_current_image()
            filename = os.path.basename(file_path)
            self.update_status(f"✓ Đã tải ảnh: {filename}")
            self.update_history_controls()

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
        self.update_history_controls()
    
    def check_image_loaded(self):
        """Kiểm tra xem đã tải ảnh chưa"""
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return False
        return True
    
    # === CHỨC NĂNG NHẬN DIỆN VÀ LÀM ĐẸP KHUÔN MẶT ===
    
    def open_face_beautify_image(self):
        """Mở cửa sổ làm đẹp từ ảnh"""
        if not self.check_image_loaded():
            return
        
        try:
            from FaceBeautifyWindow import FaceBeautifyWindow
            FaceBeautifyWindow(self, self.current_image)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở cửa sổ:\n{str(e)}")
    
    def open_face_beautify_camera(self):
        """Mở cửa sổ camera nhận diện và làm đẹp"""
        try:
            from FaceBeautifyCamera import FaceBeautifyCameraWindow
            FaceBeautifyCameraWindow(self)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở cửa sổ:\n{str(e)}")
    
    # === CÁC HÀM XỬ LÝ LÀM MỜ ===
    
    def apply_average_blur(self):
        """Áp dụng làm mờ trung bình"""
        self.apply_effect(
            Blur.apply_average_blur,
            "✓ Đã áp dụng làm mờ trung bình",
            kernel_size=(15, 15)
        )
    
    def apply_gaussian_blur(self):
        """Áp dụng làm mờ Gaussian"""
        self.apply_effect(
            Blur.apply_gaussian_blur,
            "✓ Đã áp dụng làm mờ Gaussian",
            kernel_size=(15, 15),
            sigma=3
        )
    
    def apply_median_blur(self):
        """Áp dụng làm mờ trung vị"""
        self.apply_effect(
            Blur.apply_median_blur,
            "✓ Đã áp dụng làm mờ trung vị",
            kernel_size=15
        )
    
    def apply_bilateral_blur(self):
        """Áp dụng làm mờ Bilateral"""
        self.apply_effect(
            Blur.apply_bilateral_blur,
            "✓ Đã áp dụng làm mờ Bilateral",
            d=15,
            sigma_color=80,
            sigma_space=80
        )
    
    # === CÁC HÀM XỬ LÝ ĐỘ SÁNG ===
    
    def increase_brightness(self):
        """Làm sáng ảnh"""
        self.apply_effect(
            Brightness.increase_brightness,
            "✓ Đã làm sáng ảnh",
            value=50
        )
    
    def decrease_brightness(self):
        """Làm tối ảnh"""
        self.apply_effect(
            Brightness.decrease_brightness,
            "✓ Đã làm tối ảnh",
            value=50
        )
    
    def increase_contrast(self):
        """Tăng tương phản"""
        self.apply_effect(
            Brightness.adjust_contrast_brightness,
            "✓ Đã tăng tương phản",
            alpha=1.5,
            beta=0
        )
    
    # === CÁC HÀM XỬ LÝ LÀM RÕ NÉT ===
    
    def apply_basic_sharpen(self):
        """Áp dụng làm rõ nét cơ bản"""
        self.apply_effect(
            Sharpen.sharpen_basic,
            "✓ Đã làm rõ nét ảnh",
            strength=1.0
        )

    def apply_laplacian_sharpen(self):
        """Áp dụng làm rõ nét Laplacian"""
        self.apply_effect(
            Sharpen.sharpen_laplacian,
            "✓ Đã làm rõ nét bằng Laplacian",
            strength=0.5
        )

    def apply_unsharp_mask(self):
        """Áp dụng Unsharp Mask"""
        self.apply_effect(
            Sharpen.unsharp_mask,
            "✓ Đã áp dụng Unsharp Mask",
            kernel_size=(5, 5),
            sigma=1.0,
            amount=1.5
        )

    def apply_detail_enhance(self):
        """Áp dụng tăng cường chi tiết"""
        self.apply_effect(
            Sharpen.detail_enhance,
            "✓ Đã tăng cường chi tiết"
        )

    # === CÁC HÀM XỬ LÝ PHÁT HIỆN BIÊN ===

    def apply_roberts_edge(self):
        """Áp dụng phát hiện biên Roberts"""
        self.apply_effect(
            EdgeDetection.roberts_edge_detection,
            "✓ Đã phát hiện biên bằng Roberts"
        )

    def apply_prewitt_edge(self):
        """Áp dụng phát hiện biên Prewitt"""
        self.apply_effect(
            EdgeDetection.prewitt_edge_detection,
            "✓ Đã phát hiện biên bằng Prewitt"
        )

    def apply_sobel_edge(self):
        """Áp dụng phát hiện biên Sobel"""
        self.apply_effect(
            EdgeDetection.sobel_edge_detection,
            "✓ Đã phát hiện viền bằng Sobel",
            ksize=3
        )

    def apply_canny_edge(self):
        """Áp dụng phát hiện biên Canny"""
        self.apply_effect(
            EdgeDetection.auto_canny,
            "✓ Đã phát hiện viền bằng Canny"
        )

    # === CÁC HÀM XỬ LÝ HISTOGRAM ===

    def apply_histogram_equalization(self):
        """Áp dụng cân bằng histogram"""
        self.apply_effect(
            Histogram.histogram_equalization,
            "✓ Đã cân bằng histogram"
        )

    def apply_clahe(self):
        """Áp dụng CLAHE"""
        self.apply_effect(
            Histogram.clahe_equalization,
            "✓ Đã áp dụng CLAHE",
            clip_limit=2.0
        )

    def apply_histogram_stretching(self):
        """Áp dụng kéo giãn histogram"""
        self.apply_effect(
            Histogram.histogram_stretching,
            "✓ Đã kéo giãn histogram"
        )

    def apply_auto_enhance(self):
        """Áp dụng tự động tăng cường"""
        self.apply_effect(
            Histogram.auto_enhance,
            "✓ Đã tự động tăng cường ảnh"
        )

    # === CÁC HÀM XỬ LÝ HÌNH THÁI HỌC ===

    def apply_erosion(self):
        """Áp dụng phép co (Erosion)"""
        self.apply_effect(
            Morphology.erosion,
            "✓ Đã áp dụng phép co (Erosion)",
            kernel_size=(3, 3),
            iterations=1
        )

    def apply_dilation(self):
        """Áp dụng phép giãn (Dilation)"""
        self.apply_effect(
            Morphology.dilation,
            "✓ Đã áp dụng phép giãn (Dilation)",
            kernel_size=(3, 3),
            iterations=1
        )

    def apply_opening(self):
        """Áp dụng phép mở (Opening)"""
        self.apply_effect(
            Morphology.opening,
            "✓ Đã áp dụng phép mở (Opening)",
            kernel_size=(5, 5)
        )

    def apply_closing(self):
        """Áp dụng phép đóng (Closing)"""
        self.apply_effect(
            Morphology.closing,
            "✓ Đã áp dụng phép đóng (Closing)",
            kernel_size=(5, 5)
        )

    # === CÁC HÀM XỬ LÝ XOAY & LẬT ẢNH ===

    def rotate_right_90(self):
        """Xoay ảnh 90 độ sang phải"""
        self.apply_effect(
            Transform.rotate_90_clockwise,
            "✓ Đã xoay ảnh 90° sang phải"
        )

    def rotate_left_90(self):
        """Xoay ảnh 90 độ sang trái"""
        self.apply_effect(
            Transform.rotate_90_counterclockwise,
            "✓ Đã xoay ảnh 90° sang trái"
        )

    def rotate_180(self):
        """Xoay ảnh 180 độ"""
        self.apply_effect(
            Transform.rotate_180,
            "✓ Đã xoay ảnh 180°"
        )

    def flip_horizontal(self):
        """Lật ảnh theo chiều ngang"""
        self.apply_effect(
            Transform.flip_horizontal,
            "✓ Đã lật ảnh theo chiều ngang"
        )

    def flip_vertical(self):
        """Lật ảnh theo chiều dọc"""
        self.apply_effect(
            Transform.flip_vertical,
            "✓ Đã lật ảnh theo chiều dọc"
        )

    def zoom_in_image(self):
        """Phóng to ảnh"""
        self.apply_effect(
            Transform.zoom_in,
            "✓ Đã phóng to ảnh",
            zoom_factor=1.3
        )

    def zoom_out_image(self):
        """Thu nhỏ ảnh"""
        self.apply_effect(
            Transform.zoom_out,
            "✓ Đã thu nhỏ ảnh",
            zoom_factor=0.7
        )
    
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