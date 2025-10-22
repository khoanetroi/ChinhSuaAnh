# -*- coding: utf-8 -*-
"""
Brightness.py - Các chức năng điều chỉnh độ sáng/tối của ảnh
"""

import cv2
import numpy as np


def adjust_brightness(img, value):
    """
    Điều chỉnh độ sáng của ảnh
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        value: Giá trị điều chỉnh độ sáng
               - Giá trị dương: làm sáng ảnh
               - Giá trị âm: làm tối ảnh
               - Khoảng đề xuất: -100 đến +100
    
    Returns:
        Ảnh sau khi điều chỉnh độ sáng
    """
    # Chuyển sang int16 để tránh overflow
    adjusted = img.astype(np.int16)
    adjusted = adjusted + value
    
    # Clip giá trị về khoảng [0, 255]
    adjusted = np.clip(adjusted, 0, 255)
    
    return adjusted.astype(np.uint8)


def increase_brightness(img, value=50):
    """
    Làm sáng ảnh
    
    Args:
        img: Ảnh đầu vào
        value: Mức độ làm sáng (mặc định 50)
    
    Returns:
        Ảnh đã được làm sáng
    """
    return adjust_brightness(img, abs(value))


def decrease_brightness(img, value=50):
    """
    Làm tối ảnh
    
    Args:
        img: Ảnh đầu vào
        value: Mức độ làm tối (mặc định 50)
    
    Returns:
        Ảnh đã được làm tối
    """
    return adjust_brightness(img, -abs(value))


def adjust_contrast_brightness(img, alpha=1.0, beta=0):
    """
    Điều chỉnh độ tương phản và độ sáng
    Công thức: new_img = alpha * img + beta
    
    Args:
        img: Ảnh đầu vào
        alpha: Hệ số tương phản (contrast)
               - alpha = 1.0: giữ nguyên
               - alpha > 1.0: tăng tương phản
               - 0 < alpha < 1.0: giảm tương phản
        beta: Giá trị điều chỉnh độ sáng (brightness)
              - beta > 0: làm sáng
              - beta < 0: làm tối
    
    Returns:
        Ảnh sau khi điều chỉnh
    """
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted


def auto_brightness(img, target_mean=128):
    """
    Tự động điều chỉnh độ sáng để đạt giá trị trung bình mong muốn
    
    Args:
        img: Ảnh đầu vào (grayscale)
        target_mean: Giá trị trung bình mục tiêu (mặc định 128)
    
    Returns:
        Ảnh đã được điều chỉnh độ sáng tự động
    """
    current_mean = np.mean(img)
    diff = target_mean - current_mean
    return adjust_brightness(img, int(diff))


def gamma_correction(img, gamma=1.0):
    """
    Điều chỉnh độ sáng bằng Gamma Correction
    
    Args:
        img: Ảnh đầu vào
        gamma: Giá trị gamma
               - gamma < 1: làm sáng ảnh
               - gamma = 1: giữ nguyên
               - gamma > 1: làm tối ảnh
    
    Returns:
        Ảnh sau khi áp dụng gamma correction
    """
    # Tạo lookup table
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 
                      for i in range(256)]).astype(np.uint8)
    
    # Áp dụng lookup table
    return cv2.LUT(img, table)


def compare_brightness_levels(img):
    """
    So sánh các mức độ sáng/tối khác nhau
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Dictionary chứa các ảnh với độ sáng khác nhau
    """
    results = {
        'original': img,
        'darker': decrease_brightness(img, 50),
        'brighter': increase_brightness(img, 50),
        'high_contrast': adjust_contrast_brightness(img, alpha=1.5, beta=0),
        'low_contrast': adjust_contrast_brightness(img, alpha=0.5, beta=0),
        'gamma_bright': gamma_correction(img, gamma=0.5),
        'gamma_dark': gamma_correction(img, gamma=2.0)
    }
    return results
