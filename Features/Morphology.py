# -*- coding: utf-8 -*-
"""
Morphology.py - Các chức năng xử lý hình thái học
Bao gồm: Erosion, Dilation, Opening, Closing, Gradient, Top Hat, Black Hat
"""

import cv2
import numpy as np


def create_kernel(shape='rect', size=(5, 5)):
    """
    Tạo phần tử cấu trúc (structuring element)
    
    Args:
        shape: Hình dạng ('rect', 'ellipse', 'cross')
        size: Kích thước kernel
    
    Returns:
        Kernel
    """
    if shape == 'rect':
        return cv2.getStructuringElement(cv2.MORPH_RECT, size)
    elif shape == 'ellipse':
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
    elif shape == 'cross':
        return cv2.getStructuringElement(cv2.MORPH_CROSS, size)
    else:
        return np.ones(size, np.uint8)


def erosion(img, kernel_size=(3, 3), kernel_shape='rect', iterations=1):
    """
    Phép co (Erosion)
    Làm mỏng các vùng sáng, loại bỏ nhiễu nhỏ
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
        iterations: Số lần lặp
    
    Returns:
        Ảnh sau khi erosion
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.erode(img, kernel, iterations=iterations)


def dilation(img, kernel_size=(3, 3), kernel_shape='rect', iterations=1):
    """
    Phép giãn (Dilation)
    Làm dày các vùng sáng, lấp đầy lỗ nhỏ
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
        iterations: Số lần lặp
    
    Returns:
        Ảnh sau khi dilation
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.dilate(img, kernel, iterations=iterations)


def opening(img, kernel_size=(5, 5), kernel_shape='rect'):
    """
    Phép mở (Opening) = Erosion + Dilation
    Loại bỏ nhiễu nhỏ, làm mịn đường viền
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
    
    Returns:
        Ảnh sau khi opening
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def closing(img, kernel_size=(5, 5), kernel_shape='rect'):
    """
    Phép đóng (Closing) = Dilation + Erosion
    Lấp đầy lỗ nhỏ, nối các vùng gần nhau
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
    
    Returns:
        Ảnh sau khi closing
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


def morphological_gradient(img, kernel_size=(3, 3), kernel_shape='rect'):
    """
    Gradient hình thái học = Dilation - Erosion
    Phát hiện đường viền
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
    
    Returns:
        Ảnh gradient
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)


def top_hat(img, kernel_size=(9, 9), kernel_shape='rect'):
    """
    Top Hat = Original - Opening
    Trích xuất các vùng sáng nhỏ
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
    
    Returns:
        Ảnh top hat
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)


def black_hat(img, kernel_size=(9, 9), kernel_shape='rect'):
    """
    Black Hat = Closing - Original
    Trích xuất các vùng tối nhỏ
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
        kernel_shape: Hình dạng kernel
    
    Returns:
        Ảnh black hat
    """
    kernel = create_kernel(kernel_shape, kernel_size)
    return cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)


def remove_noise(img, kernel_size=(3, 3)):
    """
    Loại bỏ nhiễu bằng opening
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
    
    Returns:
        Ảnh sau khi loại bỏ nhiễu
    """
    return opening(img, kernel_size, 'ellipse')


def fill_holes(img, kernel_size=(5, 5)):
    """
    Lấp đầy lỗ bằng closing
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
    
    Returns:
        Ảnh sau khi lấp đầy lỗ
    """
    return closing(img, kernel_size, 'ellipse')


def extract_boundary(img, kernel_size=(3, 3)):
    """
    Trích xuất đường viền bằng morphological gradient
    
    Args:
        img: Ảnh đầu vào
        kernel_size: Kích thước kernel
    
    Returns:
        Ảnh đường viền
    """
    return morphological_gradient(img, kernel_size, 'rect')


def skeletonize(img):
    """
    Tạo bộ xương (skeleton) của ảnh nhị phân
    
    Args:
        img: Ảnh nhị phân đầu vào
    
    Returns:
        Ảnh skeleton
    """
    skeleton = np.zeros(img.shape, np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    
    while True:
        eroded = cv2.erode(img, kernel)
        temp = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(img, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        img = eroded.copy()
        
        if cv2.countNonZero(img) == 0:
            break
    
    return skeleton


def compare_morphology_operations(img):
    """
    So sánh các phép toán hình thái học
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Dictionary chứa các kết quả
    """
    results = {
        'original': img,
        'erosion': erosion(img, (5, 5)),
        'dilation': dilation(img, (5, 5)),
        'opening': opening(img, (5, 5)),
        'closing': closing(img, (5, 5)),
        'gradient': morphological_gradient(img, (3, 3)),
        'tophat': top_hat(img, (9, 9)),
        'blackhat': black_hat(img, (9, 9))
    }
    return results


def adaptive_morphology(img, operation='denoise'):
    """
    Áp dụng phép hình thái học thích ứng
    
    Args:
        img: Ảnh đầu vào
        operation: Loại thao tác ('denoise', 'fill', 'boundary', 'skeleton')
    
    Returns:
        Ảnh sau xử lý
    """
    # Chuyển sang grayscale nếu cần
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Tạo ảnh nhị phân
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    if operation == 'denoise':
        return remove_noise(binary, (3, 3))
    elif operation == 'fill':
        return fill_holes(binary, (5, 5))
    elif operation == 'boundary':
        return extract_boundary(binary, (3, 3))
    elif operation == 'skeleton':
        return skeletonize(binary)
    else:
        return binary


def hit_or_miss(img, kernel):
    """
    Phép Hit-or-Miss Transform
    Dùng để tìm kiếm pattern cụ thể
    
    Args:
        img: Ảnh nhị phân đầu vào
        kernel: Structuring element
    
    Returns:
        Ảnh kết quả
    """
    return cv2.morphologyEx(img, cv2.MORPH_HITMISS, kernel)


def connected_components_analysis(img):
    """
    Phân tích các thành phần liên thông
    
    Args:
        img: Ảnh nhị phân đầu vào
    
    Returns:
        Tuple (số lượng components, ảnh labeled, stats, centroids)
    """
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
    return num_labels, labels, stats, centroids
