# -*- coding: utf-8 -*-
"""MainView.py - Main UI View (MVC Pattern)"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
from typing import Optional, Callable, Dict, Any
from UI import Button, Section, Layout, Colors


class MainView:
    """
    Main View component for MVC architecture.
    Handles all UI creation and updates, no business logic.
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize Main View

        Args:
            root: Tkinter root window
        """
        self.root = root

        # UI components
        self.image_label = None
        self.status_label = None
        self.undo_button = None
        self.redo_button = None
        self.reset_button = None
        self.save_button = None

        # Icons for undo/redo
        self.icons = {}

        # Section frames for collapsible sections
        self.blur_frame = None
        self.brightness_frame = None
        self.sharpen_frame = None
        self.edge_frame = None
        self.transform_frame = None

        # Collapsed state for sections
        self.blur_collapsed = True
        self.brightness_collapsed = True
        self.sharpen_collapsed = True
        self.edge_collapsed = True
        self.transform_collapsed = True

        # Setup window
        Layout.setup_window(self.root, "Ứng Dụng Chỉnh Sửa Ảnh - Nhóm 4 (MVC)")

        # Load icons
        self._load_icons()

    def _load_icons(self):
        """Create icons for undo/redo buttons"""
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
                    (center_x + arrow_width // 2, center_y + arrow_height // 2),
                ]
            else:  # right
                points = [
                    (center_x - arrow_width // 2, center_y - arrow_height // 2),
                    (center_x + arrow_width // 6, center_y - arrow_height // 2),
                    (center_x + arrow_width // 6, center_y - arrow_height // 2 - arrow_margin),
                    (center_x + arrow_width // 2 + arrow_margin, center_y),
                    (center_x + arrow_width // 6, center_y + arrow_height // 2 + arrow_margin),
                    (center_x + arrow_width // 6, center_y + arrow_height // 2),
                    (center_x - arrow_width // 2, center_y + arrow_height // 2),
                ]

            draw.polygon(points, fill=arrow_color)
            return ImageTk.PhotoImage(img)

        self.icons['undo'] = create_arrow_icon(Colors.get_color('info'), direction="left")
        self.icons['redo'] = create_arrow_icon(Colors.get_color('warning'), direction="right")

    def create_ui(self, callbacks: Dict[str, Callable]):
        """
        Create all UI components

        Args:
            callbacks: Dictionary of callback functions for UI events
        """
        # Header
        Layout.create_header(self.root)

        # Main container
        main_container = Layout.create_main_container(self.root)

        # === LEFT PANEL - Controls ===
        left_panel = Layout.create_left_panel(main_container)

        # Open image button
        Button.create_button(
            left_panel,
            text="📂 MỞ ẢNH",
            command=callbacks.get('load_image'),
            bg=Colors.get_color('primary'),
            font_size=12,
            bold=True,
            height=2
        )

        Section.create_separator(left_panel)

        # Scrollable frame for all controls
        scrollable_frame = Layout.create_scrollable_frame(left_panel)

        # === BLUR SECTION (COLLAPSIBLE) ===
        self.blur_frame = Section.create_collapsible_section(
            scrollable_frame,
            "🌫️ LÀM MỜ ẢNH",
            [
                ("Làm Mờ Trung Bình", callbacks.get('apply_average_blur'), Colors.get_color('blur_1')),
                ("Làm Mờ Gaussian", callbacks.get('apply_gaussian_blur'), Colors.get_color('blur_2')),
                ("Làm Mờ Trung Vị", callbacks.get('apply_median_blur'), Colors.get_color('blur_3')),
                ("Làm Mờ Bilateral", callbacks.get('apply_bilateral_blur'), Colors.get_color('blur_4')),
            ],
            "blur",
            self
        )

        Section.create_separator(scrollable_frame)

        # === BRIGHTNESS SECTION (COLLAPSIBLE) ===
        self.brightness_frame = Section.create_collapsible_section(
            scrollable_frame,
            "☀️ ĐỘ SÁNG & TƯƠNG PHẢN",
            [
                ("Tăng Độ Sáng", callbacks.get('increase_brightness'), Colors.get_color('bright_1')),
                ("Giảm Độ Sáng", callbacks.get('decrease_brightness'), Colors.get_color('bright_2')),
                ("Tăng Độ Tương Phản", callbacks.get('increase_contrast'), Colors.get_color('bright_3')),
            ],
            "brightness",
            self
        )

        Section.create_separator(scrollable_frame)

        # === SHARPEN SECTION (COLLAPSIBLE) ===
        self.sharpen_frame = Section.create_collapsible_section(
            scrollable_frame,
            "✨ LÀM RÕ NÉT ẢNH",
            [
                ("Làm Rõ Cơ Bản", callbacks.get('apply_basic_sharpen'), "#00796b"),
                ("Làm Rõ Mạnh", callbacks.get('apply_laplacian_sharpen'), "#00897b"),
                ("Làm Rõ Chuyên Nghiệp", callbacks.get('apply_unsharp_mask'), "#009688"),
                ("Tăng Chi Tiết", callbacks.get('apply_detail_enhance'), "#26a69a"),
            ],
            "sharpen",
            self
        )

        Section.create_separator(scrollable_frame)

        # === EDGE DETECTION SECTION (COLLAPSIBLE) ===
        self.edge_frame = Section.create_collapsible_section(
            scrollable_frame,
            "🔍 PHÁT HIỆN ĐƯỜNG VIỀN",
            [
                ("Viền Cơ Bản (Roberts)", callbacks.get('apply_roberts_edge'), "#5d4037"),
                ("Viền Trung Bình (Prewitt)", callbacks.get('apply_prewitt_edge'), "#6d4c41"),
                ("Viền Mạnh (Sobel)", callbacks.get('apply_sobel_edge'), "#795548"),
                ("Viền Tự Động (Canny)", callbacks.get('apply_canny_edge'), "#8d6e63"),
                ("Viền Laplacian", callbacks.get('apply_laplacian_edge'), "#a1887f"),
                ("Viền Scharr", callbacks.get('apply_scharr_edge'), "#bcaaa4"),
            ],
            "edge",
            self
        )

        Section.create_separator(scrollable_frame)

        # === TRANSFORM SECTION (COLLAPSIBLE) ===
        self.transform_frame = Section.create_collapsible_section(
            scrollable_frame,
            "🔄 XOAY & BIẾN ĐỔI",
            [
                ("↻ Xoay Phải 90°", callbacks.get('rotate_right_90'), "#ff6f00"),
                ("↺ Xoay Trái 90°", callbacks.get('rotate_left_90'), "#ff8f00"),
                ("⟲ Xoay 180°", callbacks.get('rotate_180'), "#ffa726"),
                ("↔ Lật Ngang", callbacks.get('flip_horizontal'), "#ffb74d"),
                ("↕ Lật Dọc", callbacks.get('flip_vertical'), "#ffcc80"),
                ("🔍 Phóng To", callbacks.get('zoom_in_image'), "#fb8c00"),
                ("🔎 Thu Nhỏ", callbacks.get('zoom_out_image'), "#f57c00"),
            ],
            "transform",
            self
        )

        Section.create_separator(scrollable_frame)

        # === FACE BEAUTIFY BUTTONS ===
        Button.create_button(
            scrollable_frame,
            text="📸 Làm Đẹp Từ Ảnh",
            command=callbacks.get('open_face_beautify_image'),
            bg="#e91e63",
            font_size=11,
            bold=True,
            pady_top=5
        )

        Button.create_button(
            scrollable_frame,
            text="📹 Làm Đẹp Từ Camera",
            command=callbacks.get('open_face_beautify_camera'),
            bg="#9c27b0",
            font_size=11,
            bold=True,
            pady_top=5
        )

        Section.create_separator(scrollable_frame)

        # === CONTROL BUTTONS ===
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
            command=callbacks.get('undo_action'),
            bg=Colors.get_color('info'),
            width=12,
            image=self.icons.get('undo'),
            compound='center'
        )
        self.undo_button.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

        self.redo_button = Button.create_control_button(
            button_bar,
            text="",
            command=callbacks.get('redo_action'),
            bg=Colors.get_color('warning'),
            width=12,
            image=self.icons.get('redo'),
            compound='center'
        )
        self.redo_button.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

        self.reset_button = Button.create_control_button(
            button_bar,
            text="🔄 Reset",
            command=callbacks.get('reset_image'),
            bg=Colors.get_color('danger'),
            width=12
        )
        self.reset_button.grid(row=0, column=2, padx=6, pady=6, sticky="ew")

        self.save_button = Button.create_control_button(
            button_bar,
            text="💾 Lưu",
            command=callbacks.get('save_image'),
            bg=Colors.get_color('success'),
            width=12
        )
        self.save_button.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        # === RIGHT PANEL - Image Display ===
        right_panel = Layout.create_right_panel(main_container)
        self.image_label = Layout.create_image_label(right_panel)

        # === STATUS BAR ===
        self.status_label = Layout.create_status_bar(self.root)

    def display_image(self, image: np.ndarray, max_width: int = 800, max_height: int = 600):
        """
        Display image in the UI

        Args:
            image: Image to display (BGR format)
            max_width: Maximum display width
            max_height: Maximum display height
        """
        if image is None:
            return

        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize for display
        h, w = rgb_image.shape[:2]
        scale = min(max_width / w, max_height / h, 1.0)

        if scale < 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            rgb_image = cv2.resize(rgb_image, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Convert to PhotoImage
        pil_image = Image.fromarray(rgb_image)
        photo = ImageTk.PhotoImage(pil_image)

        # Update label
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # Keep reference

    def clear_image_display(self):
        """Clear image display and show placeholder"""
        self.image_label.config(
            image='',
            text="Chưa có ảnh\n\n📷\n\nVui lòng chọn ảnh để bắt đầu"
        )
        self.image_label.image = None

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def update_history_buttons(self, can_undo: bool, can_redo: bool):
        """Update undo/redo button states"""
        self.undo_button.config(state=tk.NORMAL if can_undo else tk.DISABLED)
        self.redo_button.config(state=tk.NORMAL if can_redo else tk.DISABLED)

    def show_error(self, title: str, message: str):
        """Show error message box"""
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        """Show warning message box"""
        messagebox.showwarning(title, message)

    def show_info(self, title: str, message: str):
        """Show info message box"""
        messagebox.showinfo(title, message)

    def bind_shortcuts(self, shortcuts: Dict[str, Callable]):
        """
        Bind keyboard shortcuts

        Args:
            shortcuts: Dictionary of key bindings and callbacks
        """
        for key, callback in shortcuts.items():
            self.root.bind(key, callback)

    def run(self):
        """Start the main event loop"""
        self.root.mainloop()
