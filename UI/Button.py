# -*- coding: utf-8 -*-
"""
Button.py - Component xử lý tất cả về button
"""

import tkinter as tk
from . import Colors


def create_button(parent, text, command, bg, font_size=11, bold=False, pady_top=8, height=2):
    font_style = ("Segoe UI", font_size, "bold" if bold else "normal")
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=font_style,
        bg=bg,
        fg="white",
        relief=tk.FLAT,
        cursor="hand2",
        height=height,
        bd=0,
        activebackground=Colors.darken_color(bg),
        activeforeground="white"
    )
    btn.pack(fill=tk.X, padx=12, pady=(pady_top, 6))
    
    # Thêm hover effect
    add_hover_effect(btn, bg)
    
    return btn


def create_control_button(parent, text, command, bg, width=16, image=None, compound="left"):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        fg="white",
        relief=tk.FLAT,
        cursor="hand2",
        bd=0,
        padx=10,
        pady=8,
        activebackground=Colors.darken_color(bg)
    )

    if width is not None:
        btn.config(width=width)

    if image is not None:
        btn.config(image=image, compound=compound, padx=6, pady=6)
        btn.image = image  # giữ tham chiếu để không bị GC
    
    # Thêm hover effect
    add_hover_effect(btn, bg)
    
    return btn


def create_section_button(parent, text, command, color):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 9),
        bg=color,
        fg="white",
        relief=tk.FLAT,
        cursor="hand2",
        bd=0,
        pady=6,
        activebackground=Colors.darken_color(color),
        activeforeground="white"
    )
    btn.pack(fill=tk.X, padx=8, pady=3)
    
    # Thêm hover effect
    add_hover_effect(btn, color)
    
    return btn


def add_hover_effect(button, original_color):
    button.bind("<Enter>", lambda e: button.config(bg=Colors.lighten_color(original_color)))
    button.bind("<Leave>", lambda e: button.config(bg=original_color))


def create_header_button(parent, text, command, bg="#1a1a2e"):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        fg="#53a8b6",
        relief=tk.FLAT,
        cursor="hand2",
        anchor="w",
        bd=0,
        padx=12,
        pady=8
    )
    btn.pack(fill=tk.X, pady=2)
    
    return btn
