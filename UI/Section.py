# -*- coding: utf-8 -*-
"""
Section.py - Component xử lý collapsible section
"""

import tkinter as tk
from tkinter import ttk
from . import Button


def create_collapsible_section(parent, title, buttons, section_name, app_instance):
    # Container cho toàn bộ section
    section_container = tk.Frame(parent, bg="#16213e")
    section_container.pack(fill=tk.X, padx=8, pady=4)
    
    # Header có thể click
    header_frame = tk.Frame(section_container, bg="#1a1a2e", relief=tk.FLAT, borderwidth=0)
    header_frame.pack(fill=tk.X)
    
    # Icon và title
    arrow = "▼" if getattr(app_instance, f"{section_name}_collapsed") else "▶"
    header_btn = Button.create_header_button(
        header_frame,
        text=f"{arrow} {title}",
        command=lambda: toggle_section(section_name, content_frame, header_btn, title, app_instance)
    )
    
    # Content frame (chứa các button)
    content_frame = tk.Frame(section_container, bg="#16213e")
    if not getattr(app_instance, f"{section_name}_collapsed"):
        content_frame.pack(fill=tk.X, pady=4)
    
    # Tạo các button trong section
    for text, command, color in buttons:
        Button.create_section_button(content_frame, text, command, color)
    
    return content_frame


def toggle_section(section_name, content_frame, header_btn, title, app_instance):
    is_collapsed = getattr(app_instance, f"{section_name}_collapsed")
    
    if is_collapsed:
        # Mở rộng
        content_frame.pack(fill=tk.X, pady=4)
        header_btn.config(text=f"▼ {title}")
        setattr(app_instance, f"{section_name}_collapsed", False)
    else:
        # Thu gọn
        content_frame.pack_forget()
        header_btn.config(text=f"▶ {title}")
        setattr(app_instance, f"{section_name}_collapsed", True)


def create_separator(parent):
    separator = tk.Frame(parent, bg="#0f3460", height=2)
    separator.pack(fill=tk.X, padx=12, pady=8)
    return separator


def create_section_label(parent, text):
    label = tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 11, "bold"),
        bg="#16213e",
        fg="#53a8b6"
    )
    label.pack(pady=(8, 4))
    return label
