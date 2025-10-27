# -*- coding: utf-8 -*-
"""
EdgeDetection.py - Các chức năng phát hiện biên
Bao gồm: Roberts, Prewitt, Sobel, Canny
"""

import cv2
import numpy as np


def roberts_edge_detection(img):
    """
    Phát hiện biên bằng toán tử Roberts
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Định nghĩa kernel Roberts
    kernel_roberts_x = np.array([[1, 0],
                                  [0, -1]], dtype=np.float32)
    kernel_roberts_y = np.array([[0, 1],
                                  [-1, 0]], dtype=np.float32)
    
    # Tính gradient
    gx = cv2.filter2D(gray, cv2.CV_64F, kernel_roberts_x)
    gy = cv2.filter2D(gray, cv2.CV_64F, kernel_roberts_y)
    
    # Tính độ lớn gradient
    magnitude = cv2.magnitude(gx, gy)
    
    # Chuyển về 8-bit
    edges = cv2.convertScaleAbs(magnitude)
    
    return edges


def prewitt_edge_detection(img):
    """
    Phát hiện biên bằng toán tử Prewitt
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Định nghĩa kernel Prewitt
    kernel_prewitt_x = np.array([[-1, 0, 1],
                                  [-1, 0, 1],
                                  [-1, 0, 1]], dtype=np.float32)
    
    kernel_prewitt_y = np.array([[1, 1, 1],
                                  [0, 0, 0],
                                  [-1, -1, -1]], dtype=np.float32)
    
    # Tính gradient
    gx = cv2.filter2D(gray, cv2.CV_32F, kernel_prewitt_x)
    gy = cv2.filter2D(gray, cv2.CV_32F, kernel_prewitt_y)
    
    # Tính độ lớn gradient
    magnitude = cv2.magnitude(gx, gy)
    
    # Chuyển về 8-bit
    edges = cv2.convertScaleAbs(magnitude)
    
    return edges


def sobel_edge_detection(img, ksize=3):
    """
    Phát hiện biên bằng toán tử Sobel
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        ksize: Kích thước kernel (1, 3, 5, 7)
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Tính gradient Sobel
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Tính độ lớn gradient
    magnitude = cv2.magnitude(sobelx, sobely)
    
    # Chuyển về 8-bit
    edges = cv2.convertScaleAbs(magnitude)
    
    return edges


def canny_edge_detection(img, threshold1=50, threshold2=150, aperture_size=3):
    """
    Phát hiện biên bằng thuật toán Canny
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        threshold1: Ngưỡng thấp
        threshold2: Ngưỡng cao
        aperture_size: Kích thước aperture cho Sobel
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Áp dụng Canny
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=aperture_size)
    
    return edges


def laplacian_edge_detection(img, ksize=3):
    """
    Phát hiện biên bằng toán tử Laplacian
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
        ksize: Kích thước kernel
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Áp dụng Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
    
    # Chuyển về 8-bit
    edges = cv2.convertScaleAbs(laplacian)
    
    return edges


def scharr_edge_detection(img):
    """
    Phát hiện biên bằng toán tử Scharr (chính xác hơn Sobel)
    
    Args:
        img: Ảnh đầu vào (grayscale hoặc color)
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Tính gradient Scharr
    scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
    scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
    
    # Tính độ lớn gradient
    magnitude = cv2.magnitude(scharrx, scharry)
    
    # Chuyển về 8-bit
    edges = cv2.convertScaleAbs(magnitude)
    
    return edges


def compare_edge_detection_methods(img):
    """
    So sánh các phương pháp phát hiện biên
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Dictionary chứa các kết quả
    """
    results = {
        'original': img,
        'roberts': roberts_edge_detection(img),
        'prewitt': prewitt_edge_detection(img),
        'sobel': sobel_edge_detection(img),
        'canny': canny_edge_detection(img),
        'laplacian': laplacian_edge_detection(img),
        'scharr': scharr_edge_detection(img)
    }
    return results


def auto_canny(img, sigma=0.33):
    """
    Tự động tính ngưỡng cho Canny edge detection
    
    Args:
        img: Ảnh đầu vào
        sigma: Tỷ lệ cho ngưỡng
    
    Returns:
        Ảnh biên
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Tính median
    median = np.median(gray)
    
    # Tính ngưỡng tự động
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    
    # Áp dụng Canny
    edges = cv2.Canny(gray, lower, upper)
    
    return edges


def gradient_direction(img):
    """
    Tính hướng gradient của ảnh
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh hướng gradient (0-360 độ)
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Tính gradient
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Tính góc (radian -> độ)
    direction = np.arctan2(sobely, sobelx) * 180 / np.pi
    
    # Chuyển về [0, 360]
    direction = (direction + 360) % 360
    
    return direction.astype(np.uint8)
