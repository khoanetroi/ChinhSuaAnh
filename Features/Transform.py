# -*- coding: utf-8 -*-
"""
Transform.py - Các chức năng biến đổi hình học
Bao gồm: Xoay, Lật, Thay đổi kích thước, Cắt ảnh
"""

import cv2
import numpy as np


def rotate_90_clockwise(img):
    """
    Xoay ảnh 90 độ theo chiều kim đồng hồ
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi xoay
    """
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


def rotate_90_counterclockwise(img):
    """
    Xoay ảnh 90 độ ngược chiều kim đồng hồ
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi xoay
    """
    return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


def rotate_180(img):
    """
    Xoay ảnh 180 độ
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi xoay
    """
    return cv2.rotate(img, cv2.ROTATE_180)


def rotate_custom(img, angle, scale=1.0):
    """
    Xoay ảnh theo góc tùy chỉnh
    
    Args:
        img: Ảnh đầu vào
        angle: Góc xoay (độ)
        scale: Tỷ lệ zoom (1.0 = giữ nguyên)
    
    Returns:
        Ảnh sau khi xoay
    """
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    
    # Tạo ma trận xoay
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Áp dụng xoay
    rotated = cv2.warpAffine(img, rotation_matrix, (width, height))
    
    return rotated


def flip_horizontal(img):
    """
    Lật ảnh theo chiều ngang (trái-phải)
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi lật
    """
    return cv2.flip(img, 1)


def flip_vertical(img):
    """
    Lật ảnh theo chiều dọc (trên-dưới)
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi lật
    """
    return cv2.flip(img, 0)


def flip_both(img):
    """
    Lật ảnh cả hai chiều
    
    Args:
        img: Ảnh đầu vào
    
    Returns:
        Ảnh sau khi lật
    """
    return cv2.flip(img, -1)


def resize_by_percentage(img, percentage):
    """
    Thay đổi kích thước theo phần trăm
    
    Args:
        img: Ảnh đầu vào
        percentage: Phần trăm (50 = thu nhỏ 50%, 200 = phóng to 200%)
    
    Returns:
        Ảnh sau khi thay đổi kích thước
    """
    scale = percentage / 100.0
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)


def resize_to_dimensions(img, width, height):
    """
    Thay đổi kích thước theo chiều rộng và cao cụ thể
    
    Args:
        img: Ảnh đầu vào
        width: Chiều rộng mới
        height: Chiều cao mới
    
    Returns:
        Ảnh sau khi thay đổi kích thước
    """
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)


def resize_keep_aspect_ratio(img, target_width=None, target_height=None):
    """
    Thay đổi kích thước giữ nguyên tỷ lệ
    
    Args:
        img: Ảnh đầu vào
        target_width: Chiều rộng mục tiêu (None = tự động)
        target_height: Chiều cao mục tiêu (None = tự động)
    
    Returns:
        Ảnh sau khi thay đổi kích thước
    """
    height, width = img.shape[:2]
    
    if target_width is not None:
        scale = target_width / width
        new_width = target_width
        new_height = int(height * scale)
    elif target_height is not None:
        scale = target_height / height
        new_height = target_height
        new_width = int(width * scale)
    else:
        return img
    
    return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)


def crop_center(img, crop_width, crop_height):
    """
    Cắt ảnh từ trung tâm
    
    Args:
        img: Ảnh đầu vào
        crop_width: Chiều rộng vùng cắt
        crop_height: Chiều cao vùng cắt
    
    Returns:
        Ảnh sau khi cắt
    """
    height, width = img.shape[:2]
    
    # Tính toán vị trí bắt đầu
    start_x = max(0, (width - crop_width) // 2)
    start_y = max(0, (height - crop_height) // 2)
    
    # Đảm bảo không vượt quá kích thước ảnh
    end_x = min(width, start_x + crop_width)
    end_y = min(height, start_y + crop_height)
    
    return img[start_y:end_y, start_x:end_x]


def crop_rectangle(img, x, y, width, height):
    """
    Cắt ảnh theo hình chữ nhật
    
    Args:
        img: Ảnh đầu vào
        x: Tọa độ x góc trên trái
        y: Tọa độ y góc trên trái
        width: Chiều rộng
        height: Chiều cao
    
    Returns:
        Ảnh sau khi cắt
    """
    img_height, img_width = img.shape[:2]
    
    # Đảm bảo tọa độ hợp lệ
    x = max(0, min(x, img_width))
    y = max(0, min(y, img_height))
    width = min(width, img_width - x)
    height = min(height, img_height - y)
    
    return img[y:y+height, x:x+width]


def add_border(img, border_size=10, border_color=(0, 0, 0)):
    """
    Thêm viền cho ảnh
    
    Args:
        img: Ảnh đầu vào
        border_size: Độ dày viền
        border_color: Màu viền (B, G, R)
    
    Returns:
        Ảnh có viền
    """
    return cv2.copyMakeBorder(
        img, 
        border_size, border_size, border_size, border_size,
        cv2.BORDER_CONSTANT,
        value=border_color
    )


def perspective_transform(img, src_points, dst_points):
    """
    Biến đổi phối cảnh (perspective transform)
    
    Args:
        img: Ảnh đầu vào
        src_points: 4 điểm nguồn [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        dst_points: 4 điểm đích [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    
    Returns:
        Ảnh sau biến đổi
    """
    src_points = np.float32(src_points)
    dst_points = np.float32(dst_points)
    
    # Tính ma trận biến đổi
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    
    # Áp dụng biến đổi
    height, width = img.shape[:2]
    transformed = cv2.warpPerspective(img, matrix, (width, height))
    
    return transformed


def zoom_in(img, zoom_factor=1.5):
    """
    Phóng to ảnh từ trung tâm
    
    Args:
        img: Ảnh đầu vào
        zoom_factor: Hệ số phóng to (>1)
    
    Returns:
        Ảnh sau khi phóng to
    """
    height, width = img.shape[:2]
    
    # Tính kích thước mới
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    
    # Phóng to
    zoomed = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Cắt về kích thước ban đầu từ trung tâm
    start_x = (new_width - width) // 2
    start_y = (new_height - height) // 2
    
    return zoomed[start_y:start_y+height, start_x:start_x+width]


def zoom_out(img, zoom_factor=0.7):
    """
    Thu nhỏ ảnh và thêm viền đen
    
    Args:
        img: Ảnh đầu vào
        zoom_factor: Hệ số thu nhỏ (<1)
    
    Returns:
        Ảnh sau khi thu nhỏ
    """
    height, width = img.shape[:2]
    
    # Tính kích thước mới
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    
    # Thu nhỏ
    zoomed = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Tạo canvas đen
    canvas = np.zeros((height, width, 3), dtype=np.uint8) if len(img.shape) == 3 else np.zeros((height, width), dtype=np.uint8)
    
    # Đặt ảnh thu nhỏ vào giữa canvas
    start_x = (width - new_width) // 2
    start_y = (height - new_height) // 2
    
    canvas[start_y:start_y+new_height, start_x:start_x+new_width] = zoomed
    
    return canvas
