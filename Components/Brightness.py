# -*- coding: utf-8 -*-
"""
Brightness.py - Các chức năng điều chỉnh độ sáng/tối của ảnh
"""

import cv2
import numpy as np


def adjust_brightness(img, value):
    # Chuyển sang int16 để tránh overflow
    adjusted = img.astype(np.int16)
    adjusted = adjusted + value
    
    # Clip giá trị về khoảng [0, 255]
    adjusted = np.clip(adjusted, 0, 255)
    
    return adjusted.astype(np.uint8)

def increase_brightness(img, value=50):
    return adjust_brightness(img, abs(value))


def decrease_brightness(img, value=50):
    return adjust_brightness(img, -abs(value))


def adjust_contrast_brightness(img, alpha=1.0, beta=0):
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted


def auto_brightness(img, target_mean=128):
    current_mean = np.mean(img)
    diff = target_mean - current_mean
    return adjust_brightness(img, int(diff))


def gamma_correction(img, gamma=1.0):
    # Tạo lookup table
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 
                      for i in range(256)]).astype(np.uint8)
    
    # Áp dụng lookup table
    return cv2.LUT(img, table)


def compare_brightness_levels(img):
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
