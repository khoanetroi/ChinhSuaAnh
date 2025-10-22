# -*- coding: utf-8 -*-
"""
Blur.py - Các chức năng làm mờ ảnh
"""

import cv2
import numpy as np


def apply_average_blur(img, kernel_size=(5, 5)):
    """
    Áp dụng bộ lọc Average Blur (làm mờ trung bình)
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        kernel_size: Kích thước kernel (width, height), mặc định (5, 5)
    
    Returns:
        Ảnh sau khi làm mờ
    """
    return cv2.blur(img, kernel_size)


def apply_gaussian_blur(img, kernel_size=(5, 5), sigma=1):
    """
    Áp dụng bộ lọc Gaussian Blur (làm mờ Gaussian)
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        kernel_size: Kích thước kernel (width, height), mặc định (5, 5)
        sigma: Độ lệch chuẩn, mặc định 1
    
    Returns:
        Ảnh sau khi làm mờ
    """
    return cv2.GaussianBlur(img, kernel_size, sigma)


def apply_median_blur(img, kernel_size=5):
    """
    Áp dụng bộ lọc Median Blur (làm mờ trung vị)
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        kernel_size: Kích thước kernel (số lẻ), mặc định 5
    
    Returns:
        Ảnh sau khi làm mờ
    """
    return cv2.medianBlur(img, kernel_size)


def apply_bilateral_blur(img, d=9, sigma_color=75, sigma_space=75):
    """
    Áp dụng bộ lọc Bilateral Blur (làm mờ song phương - giữ cạnh)
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        d: Đường kính của mỗi pixel neighborhood
        sigma_color: Filter sigma trong color space
        sigma_space: Filter sigma trong coordinate space
    
    Returns:
        Ảnh sau khi làm mờ
    """
    return cv2.bilateralFilter(img, d, sigma_color, sigma_space)


def compare_blur_methods(img):
    """
    So sánh các phương pháp làm mờ khác nhau
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Dictionary chứa các ảnh đã làm mờ với các phương pháp khác nhau
    """
    results = {
        'original': img,
        'average': apply_average_blur(img),
        'gaussian': apply_gaussian_blur(img),
        'median': apply_median_blur(img),
        'bilateral': apply_bilateral_blur(img)
    }
    return results