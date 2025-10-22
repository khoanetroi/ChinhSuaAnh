# -*- coding: utf-8 -*-
"""
Layout.py - Component xử lý layout (header, status bar, container, scrollable frame)
"""

import tkinter as tk
from tkinter import ttk


def create_header(root, title="🎨 ỨNG DỤNG CHỈNH SỬA ẢNH"):
    header_frame = tk.Frame(root, bg="#2c3e50", height=80)
    header_frame.pack(fill=tk.X, side=tk.TOP)
    
    title_label = tk.Label(
        header_frame, 
        text=title, 
        font=("Arial", 24, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=20)
    
    return header_frame


def create_status_bar(root, initial_text="Sẵn sàng - Vui lòng chọn ảnh để bắt đầu"):
    status_frame = tk.Frame(root, bg="#34495e", height=35)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    status_label = tk.Label(
        status_frame,
        text=initial_text,
        font=("Arial", 10),
        bg="#34495e",
        fg="white",
        anchor="w"
    )
    status_label.pack(side=tk.LEFT, padx=20, pady=8)
    
    return status_label


def create_main_container(root):
    main_container = tk.Frame(root, bg="#f0f0f0")
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    return main_container


def create_left_panel(parent, width=320):
    left_panel = tk.Frame(parent, bg="white", width=width, relief=tk.RAISED, borderwidth=2)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    left_panel.pack_propagate(False)
    
    return left_panel


def create_right_panel(parent):
    right_panel = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=2)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    return right_panel


def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return scrollable_frame


def create_image_label(parent):
    image_label = tk.Label(
        parent,
        text="Chưa có ảnh\n\n📷\n\nVui lòng chọn ảnh để bắt đầu",
        font=("Arial", 16),
        bg="white",
        fg="#95a5a6"
    )
    image_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    return image_label


def create_control_frame(parent):
    control_frame = tk.Frame(parent, bg="white")
    control_frame.pack(fill=tk.X, padx=10, pady=5)
    
    return control_frame


def setup_window(root, title="Ứng Dụng Chỉnh Sửa Ảnh"):
    root.title(title)
    
    # Responsive window size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = min(1200, int(screen_width * 0.8))
    window_height = min(800, int(screen_height * 0.85))
    
    # Center window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#f0f0f0")
    root.minsize(900, 600)
