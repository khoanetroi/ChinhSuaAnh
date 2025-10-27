# -*- coding: utf-8 -*-
"""
Histogram.py - Các chức năng xử lý histogram
Bao gồm: Histogram Equalization, CLAHE, Histogram Stretching
"""

import cv2
import numpy as np


def histogram_equalization(img):
    """
    Cân bằng histogram cho ảnh xám hoặc màu
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi cân bằng histogram
    """
    if len(img.shape) == 2:
        # Ảnh xám
        return cv2.equalizeHist(img)
    else:
        # Ảnh màu - chuyển sang YCrCb và cân bằng kênh Y
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


def clahe_equalization(img, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Cân bằng histogram thích ứng CLAHE
    (Contrast Limited Adaptive Histogram Equalization)
    
    Args:
        img: Ảnh đầu vào
        clip_limit: Ngưỡng giới hạn contrast
        tile_grid_size: Kích thước grid cho adaptive equalization
    
    Returns:
        Ảnh sau khi áp dụng CLAHE
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    if len(img.shape) == 2:
        # Ảnh xám
        return clahe.apply(img)
    else:
        # Ảnh màu - chuyển sang LAB và áp dụng CLAHE cho kênh L
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def histogram_stretching(img):
    """
    Kéo giãn histogram tuyến tính
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi kéo giãn histogram
    """
    if len(img.shape) == 2:
        # Ảnh xám
        r_min, r_max = np.min(img), np.max(img)
        stretched = (img.astype(np.float32) - r_min) * (255.0 / (r_max - r_min))
        return np.uint8(np.clip(stretched, 0, 255))
    else:
        # Ảnh màu - áp dụng cho từng kênh
        result = np.zeros_like(img)
        for i in range(3):
            r_min, r_max = np.min(img[:, :, i]), np.max(img[:, :, i])
            stretched = (img[:, :, i].astype(np.float32) - r_min) * (255.0 / (r_max - r_min))
            result[:, :, i] = np.uint8(np.clip(stretched, 0, 255))
        return result


def adaptive_histogram_stretching(img, percentile_low=2, percentile_high=98):
    """
    Kéo giãn histogram thích ứng với percentile
    
    Args:
        img: Ảnh đầu vào
        percentile_low: Percentile thấp (0-100)
        percentile_high: Percentile cao (0-100)
    
    Returns:
        Ảnh sau khi kéo giãn
    """
    if len(img.shape) == 2:
        # Ảnh xám
        p_low = np.percentile(img, percentile_low)
        p_high = np.percentile(img, percentile_high)
        
        stretched = (img.astype(np.float32) - p_low) * (255.0 / (p_high - p_low))
        return np.uint8(np.clip(stretched, 0, 255))
    else:
        # Ảnh màu
        result = np.zeros_like(img)
        for i in range(3):
            p_low = np.percentile(img[:, :, i], percentile_low)
            p_high = np.percentile(img[:, :, i], percentile_high)
            
            stretched = (img[:, :, i].astype(np.float32) - p_low) * (255.0 / (p_high - p_low))
            result[:, :, i] = np.uint8(np.clip(stretched, 0, 255))
        return result


def histogram_matching(source, reference):
    """
    Khớp histogram của ảnh nguồn với ảnh tham chiếu
    
    Args:
        source: Ảnh nguồn
        reference: Ảnh tham chiếu
    
    Returns:
        Ảnh sau khi khớp histogram
    """
    if len(source.shape) == 2:
        # Ảnh xám
        return match_histograms_single_channel(source, reference)
    else:
        # Ảnh màu
        result = np.zeros_like(source)
        for i in range(3):
            result[:, :, i] = match_histograms_single_channel(
                source[:, :, i], 
                reference[:, :, i]
            )
        return result


def match_histograms_single_channel(source, reference):
    """
    Khớp histogram cho một kênh
    
    Args:
        source: Kênh nguồn
        reference: Kênh tham chiếu
    
    Returns:
        Kênh sau khi khớp
    """
    # Tính histogram và CDF
    src_hist, _ = np.histogram(source.flatten(), 256, [0, 256])
    ref_hist, _ = np.histogram(reference.flatten(), 256, [0, 256])
    
    src_cdf = src_hist.cumsum()
    ref_cdf = ref_hist.cumsum()
    
    # Chuẩn hóa
    src_cdf = src_cdf / src_cdf[-1]
    ref_cdf = ref_cdf / ref_cdf[-1]
    
    # Tạo lookup table
    lookup = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        j = np.argmin(np.abs(src_cdf[i] - ref_cdf))
        lookup[i] = j
    
    # Áp dụng lookup table
    return lookup[source]


def calculate_histogram(img):
    """
    Tính histogram của ảnh
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Histogram (hoặc list của histograms cho ảnh màu)
    """
    if len(img.shape) == 2:
        # Ảnh xám
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        return hist
    else:
        # Ảnh màu - tính cho từng kênh
        histograms = []
        for i in range(3):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            histograms.append(hist)
        return histograms


def compare_histogram_methods(img):
    """
    So sánh các phương pháp xử lý histogram
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Dictionary chứa các kết quả
    """
    results = {
        'original': img,
        'equalized': histogram_equalization(img),
        'clahe': clahe_equalization(img),
        'stretched': histogram_stretching(img),
        'adaptive_stretched': adaptive_histogram_stretching(img)
    }
    return results


def auto_enhance(img):
    """
    Tự động tăng cường ảnh bằng histogram
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi tăng cường
    """
    # Tính độ tương phản hiện tại
    if len(img.shape) == 2:
        std = np.std(img)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        std = np.std(gray)
    
    # Chọn phương pháp phù hợp
    if std < 30:
        # Độ tương phản thấp - dùng CLAHE
        return clahe_equalization(img, clip_limit=3.0)
    elif std < 50:
        # Độ tương phản trung bình - dùng histogram equalization
        return histogram_equalization(img)
    else:
        # Độ tương phản cao - dùng adaptive stretching
        return adaptive_histogram_stretching(img)
