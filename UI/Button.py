# -*- coding: utf-8 -*-
"""
Button.py - Component xử lý tất cả về button
"""

import tkinter as tk
from . import Colors


def create_button(parent, text, command, bg, font_size=11, bold=False, pady_top=5, height=2):
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
        height=height,
        activebackground=Colors.darken_color(bg),
        activeforeground="white"
    )
    btn.pack(fill=tk.X, padx=15, pady=(pady_top, 5))
    
    # Thêm hover effect
    add_hover_effect(btn, bg)
    
    return btn


def create_control_button(parent, text, command, bg, width=14):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=bg,
        fg="white",
        relief=tk.FLAT,
        cursor="hand2",
        width=width,
        activebackground=Colors.darken_color(bg)
    )
    
    # Thêm hover effect
    add_hover_effect(btn, bg)
    
    return btn


def create_section_button(parent, text, command, color):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10),
        bg=color,
        fg="white",
        relief=tk.FLAT,
        cursor="hand2",
        height=1,
        activebackground=Colors.darken_color(color),
        activeforeground="white"
    )
    btn.pack(fill=tk.X, padx=5, pady=2)
    
    # Thêm hover effect
    add_hover_effect(btn, color)
    
    return btn


def add_hover_effect(button, original_color):
    button.bind("<Enter>", lambda e: button.config(bg=Colors.lighten_color(original_color)))
    button.bind("<Leave>", lambda e: button.config(bg=original_color))


def create_header_button(parent, text, command, bg="#ecf0f1"):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=bg,
        fg="#2c3e50",
        relief=tk.FLAT,
        cursor="hand2",
        anchor="w",
        padx=10
    )
    btn.pack(fill=tk.X, pady=5)
    
    return btn
