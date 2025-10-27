# -*- coding: utf-8 -*-
"""
Layout.py - Component xử lý layout (header, status bar, container, scrollable frame)
"""

import tkinter as tk
from tkinter import ttk


def create_header(root, title="🎨 ỨNG DỤNG CHỈNH SỬA ẢNH"):
    header_frame = tk.Frame(root, bg="#1a1a2e", height=70)
    header_frame.pack(fill=tk.X, side=tk.TOP)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame, 
        text=title, 
        font=("Segoe UI", 20, "bold"),
        bg="#1a1a2e",
        fg="#eee"
    )
    title_label.pack(pady=18)
    
    return header_frame


def create_status_bar(root, initial_text="Sẵn sàng - Vui lòng chọn ảnh để bắt đầu"):
    status_frame = tk.Frame(root, bg="#16213e", height=32)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_frame.pack_propagate(False)
    
    status_label = tk.Label(
        status_frame,
        text=initial_text,
        font=("Segoe UI", 9),
        bg="#16213e",
        fg="#aaa",
        anchor="w"
    )
    status_label.pack(side=tk.LEFT, padx=15, pady=6)
    
    return status_label


def create_main_container(root):
    main_container = tk.Frame(root, bg="#0f3460")
    main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)
    
    return main_container


def create_left_panel(parent, width=360):
    left_panel = tk.Frame(parent, bg="#16213e", width=width, relief=tk.FLAT, borderwidth=0)
    left_panel.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
    left_panel.grid_propagate(False)
    left_panel.pack_propagate(False)
    
    return left_panel


def create_right_panel(parent):
    right_panel = tk.Frame(parent, bg="#16213e", relief=tk.FLAT, borderwidth=0)
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.grid_rowconfigure(0, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)
    right_panel.pack_propagate(False)
    
    return right_panel


def create_scrollable_frame(parent):
    container = tk.Frame(parent, bg="#16213e")
    container.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container, bg="#16213e", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#16213e")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    def _resize_canvas(event):
        canvas.itemconfig(frame_window, width=event.width)

    frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.bind("<Configure>", _resize_canvas)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame


def create_image_label(parent):
    image_label = tk.Label(
        parent,
        text="Chưa có ảnh\n\n📷\n\nVui lòng chọn ảnh để bắt đầu",
        font=("Segoe UI", 14),
        bg="#16213e",
        fg="#53a8b6"
    )
    image_label.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
    
    return image_label


def create_control_frame(parent):
    control_frame = tk.Frame(parent, bg="#16213e")
    control_frame.pack(fill=tk.X, padx=10, pady=8)
    
    return control_frame


def setup_window(root, title="Ứng Dụng Chỉnh Sửa Ảnh"):
    root.title(title)
    
    # Responsive window size - larger for better display
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = min(1400, int(screen_width * 0.85))
    window_height = min(900, int(screen_height * 0.9))
    
    # Center window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#0f3460")
    root.minsize(1100, 700)
