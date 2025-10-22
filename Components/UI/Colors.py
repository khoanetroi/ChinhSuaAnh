# -*- coding: utf-8 -*-
"""
Colors.py - Xử lý màu sắc và hiệu ứng màu
"""


def lighten_color(hex_color, factor=1.1):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    return f'#{r:02x}{g:02x}{b:02x}'


def darken_color(hex_color, factor=0.8):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f'#{r:02x}{g:02x}{b:02x}'


# Định nghĩa bảng màu chuẩn cho ứng dụng
COLORS = {
    'primary': '#3498db',      # Xanh dương chính
    'success': '#27ae60',      # Xanh lá - thành công
    'danger': '#e74c3c',       # Đỏ - nguy hiểm
    'warning': '#f39c12',      # Cam - cảnh báo
    'info': '#3498db',         # Xanh - thông tin
    'dark': '#2c3e50',         # Tối
    'light': '#ecf0f1',        # Sáng
    'gray': '#95a5a6',         # Xám
    
    # Màu cho blur effects
    'blur_1': '#9b59b6',
    'blur_2': '#8e44ad',
    'blur_3': '#7d3c98',
    'blur_4': '#6c3483',
    
    # Màu cho brightness effects
    'bright_1': '#f39c12',
    'bright_2': '#e67e22',
    'bright_3': '#d68910',
}


def get_color(color_name):
    return COLORS.get(color_name)
