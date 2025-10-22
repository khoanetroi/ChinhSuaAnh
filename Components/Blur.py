# -*- coding: utf-8 -*-
"""
Blur.py - Các chức năng làm mờ ảnh
"""

import cv2
import numpy as np


def apply_average_blur(img, kernel_size=(5, 5)):
    return cv2.blur(img, kernel_size)


def apply_gaussian_blur(img, kernel_size=(5, 5), sigma=1):
    return cv2.GaussianBlur(img, kernel_size, sigma)


def apply_median_blur(img, kernel_size=5):
    return cv2.medianBlur(img, kernel_size)


def apply_bilateral_blur(img, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(img, d, sigma_color, sigma_space)


def compare_blur_methods(img):
    results = {
        'original': img,
        'average': apply_average_blur(img),
        'gaussian': apply_gaussian_blur(img),
        'median': apply_median_blur(img),
        'bilateral': apply_bilateral_blur(img)
    }
    return results