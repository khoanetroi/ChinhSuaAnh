# -*- coding: utf-8 -*-
"""
Sharpen.py - Các chức năng làm rõ nét ảnh
Bao gồm: Sharpening, Unsharp Masking, High-pass Filter
"""

import cv2
import numpy as np


def sharpen_basic(img, strength=1.0):
    """
    Làm rõ nét ảnh bằng kernel cơ bản
    
    Args:
        img: Ảnh đầu vào
        strength: Độ mạnh của sharpening (0.0 - 2.0)
    
    Returns:
        Ảnh sau khi làm rõ nét
    """
    # Kernel làm rõ nét cơ bản
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)
    
    # Điều chỉnh độ mạnh
    kernel = kernel * strength
    kernel[1, 1] = 1 + 4 * strength
    
    sharpened = cv2.filter2D(img, -1, kernel)
    return sharpened


def sharpen_laplacian(img, strength=1.0):
    """
    Làm rõ nét bằng Laplacian operator
    
    Args:
        img: Ảnh đầu vào
        strength: Độ mạnh của sharpening
    
    Returns:
        Ảnh sau khi làm rõ nét
    """
    # Tính Laplacian
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)
    
    # Kết hợp với ảnh gốc
    sharpened = cv2.addWeighted(img, 1.0, laplacian, strength, 0)
    
    return sharpened


def unsharp_mask(img, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """
    Làm rõ nét bằng Unsharp Masking
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel cho Gaussian blur
        sigma: Sigma cho Gaussian blur
        amount: Độ mạnh của sharpening
        threshold: Ngưỡng để áp dụng sharpening
    
    Returns:
        Ảnh sau khi làm rõ nét
    """
    # Tạo ảnh mờ
    blurred = cv2.GaussianBlur(img, kernel_size, sigma)
    
    # Tạo mask
    mask = cv2.subtract(img, blurred)
    
    # Áp dụng threshold nếu cần
    if threshold > 0:
        _, mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY)
    
    # Kết hợp với ảnh gốc
    sharpened = cv2.addWeighted(img, 1.0, mask, amount, 0)
    
    return sharpened


def sharpen_highpass(img, kernel_size=3):
    """
    Làm rõ nét bằng High-pass filter
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
    
    Returns:
        Ảnh sau khi làm rõ nét
    """
    # Tạo low-pass filter
    lowpass = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    
    # High-pass = Original - Low-pass
    highpass = cv2.subtract(img, lowpass)
    
    # Kết hợp
    sharpened = cv2.add(img, highpass)
    
    return sharpened


def adaptive_sharpen(img, blur_amount=None):
    """
    Làm rõ nét thích ứng dựa trên độ mờ của ảnh
    
    Args:
        img: Ảnh đầu vào
        blur_amount: Độ mờ ước tính (None = tự động tính)
    
    Returns:
        Ảnh sau khi làm rõ nét
    """
    # Tính độ mờ nếu không được cung cấp
    if blur_amount is None:
        # Sử dụng Laplacian variance để ước tính độ mờ
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Ảnh càng mờ thì variance càng thấp
        # Điều chỉnh strength dựa trên variance
        if laplacian_var < 100:
            strength = 2.0  # Ảnh rất mờ
        elif laplacian_var < 500:
            strength = 1.5  # Ảnh hơi mờ
        else:
            strength = 1.0  # Ảnh khá rõ
    else:
        strength = blur_amount
    
    return unsharp_mask(img, kernel_size=(5, 5), sigma=1.0, amount=strength)


def compare_sharpen_methods(img):
    """
    So sánh các phương pháp làm rõ nét
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Dictionary chứa các kết quả
    """
    results = {
        'original': img,
        'basic': sharpen_basic(img, 1.0),
        'laplacian': sharpen_laplacian(img, 0.5),
        'unsharp': unsharp_mask(img, (5, 5), 1.0, 1.5),
        'highpass': sharpen_highpass(img, 3),
        'adaptive': adaptive_sharpen(img)
    }
    return results


def detail_enhance(img, sigma_s=60, sigma_r=0.07):
    """
    Tăng cường chi tiết ảnh
    
    Args:
        img: Ảnh đầu vào
        sigma_s: Spatial sigma
        sigma_r: Range sigma
    
    Returns:
        Ảnh sau khi tăng cường
    """
    return cv2.detailEnhance(img, sigma_s=sigma_s, sigma_r=sigma_r)


def edge_preserve_sharpen(img):
    """
    Làm rõ nét trong khi bảo toàn cạnh
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi làm rõ nét
    """
    # Sử dụng bilateral filter để giữ cạnh
    smooth = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Tạo mask từ sự khác biệt
    mask = cv2.subtract(img, smooth)
    
    # Kết hợp để làm rõ nét
    sharpened = cv2.add(img, mask)
    
    return sharpened
