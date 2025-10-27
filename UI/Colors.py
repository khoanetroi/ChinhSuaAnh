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


# Định nghĩa bảng màu chuẩn cho ứng dụng - Modern Dark Theme
COLORS = {
    'primary': '#e94560',      # Đỏ hồng chính
    'success': '#06d6a0',      # Xanh lá - thành công
    'danger': '#ef476f',       # Đỏ - nguy hiểm
    'warning': '#ffd166',      # Vàng - cảnh báo
    'info': '#118ab2',         # Xanh - thông tin
    'dark': '#1a1a2e',         # Tối
    'light': '#53a8b6',        # Sáng xanh
    'gray': '#95a5a6',         # Xám
    
    # Màu cho blur effects - Purple tones
    'blur_1': '#a855f7',
    'blur_2': '#9333ea',
    'blur_3': '#7e22ce',
    'blur_4': '#6b21a8',
    
    # Màu cho brightness effects - Orange/Yellow tones
    'bright_1': '#fb923c',
    'bright_2': '#f97316',
    'bright_3': '#ea580c',
}


def get_color(color_name):
    return COLORS.get(color_name)
