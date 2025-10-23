# -*- coding: utf-8 -*-

import cv2
import numpy as np


def detect_faces(image):
    """
    Nhận diện khuôn mặt trong ảnh
    Trả về: danh sách các tọa độ khuôn mặt (x, y, w, h)
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces


def draw_face_rectangles(image, faces, color=(0, 255, 0), thickness=3):
    """Vẽ khung chữ nhật xung quanh khuôn mặt"""
    result = image.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(result, (x, y), (x+w, y+h), color, thickness)
        cv2.putText(result, f"Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return result


def smooth_skin(image, faces, smooth_level=0.3):
    """
    Làm mịn da - Bilateral Filter cho vùng khuôn mặt
    smooth_level: 0.0 - 1.0 (mức độ làm mịn)
    """
    result = image.copy()
    for (x, y, w, h) in faces:
        face_roi = result[y:y+h, x:x+w]
        d = int(9 + smooth_level * 20)
        sigma_color = int(50 + smooth_level * 100)
        sigma_space = int(50 + smooth_level * 100)
        smoothed = cv2.bilateralFilter(face_roi, d, sigma_color, sigma_space)
        alpha = 0.3 + smooth_level * 0.7
        blended = cv2.addWeighted(face_roi, 1-alpha, smoothed, alpha, 0)
        result[y:y+h, x:x+w] = blended
    return result


def brighten_face(image, faces, brightness_value=30):
    """Làm sáng khuôn mặt"""
    result = image.copy()
    for (x, y, w, h) in faces:
        face_roi = result[y:y+h, x:x+w]
        brightened = cv2.convertScaleAbs(face_roi, alpha=1.0, beta=brightness_value)
        result[y:y+h, x:x+w] = brightened
    return result


def enhance_face_contrast(image, faces, contrast=1.3):
    """Tăng độ tương phản cho khuôn mặt"""
    result = image.copy()
    for (x, y, w, h) in faces:
        face_roi = result[y:y+h, x:x+w]
        enhanced = cv2.convertScaleAbs(face_roi, alpha=contrast, beta=0)
        result[y:y+h, x:x+w] = enhanced
    return result


def remove_blemishes(image, faces):
    """Làm mờ tì vết, mụn trên khuôn mặt"""
    result = image.copy()
    for (x, y, w, h) in faces:
        face_roi = result[y:y+h, x:x+w]
        denoised = cv2.fastNlMeansDenoisingColored(face_roi, None, 10, 10, 7, 21)
        result[y:y+h, x:x+w] = denoised
    return result


def beautify_face_auto(image, faces):
    """Tự động làm đẹp khuôn mặt (kết hợp nhiều kỹ thuật)"""
    result = image.copy()
    result = smooth_skin(result, faces, smooth_level=0.5)
    result = brighten_face(result, faces, brightness_value=15)
    result = enhance_face_contrast(result, faces, contrast=1.15)
    result = remove_blemishes(result, faces)
    return result


def apply_blur_background(image, faces, blur_amount=21):
    """Làm mờ nền, giữ khuôn mặt nét"""
    result = image.copy()
    blurred = cv2.GaussianBlur(result, (blur_amount, blur_amount), 0)
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    for (x, y, w, h) in faces:
        padding = int(w * 0.2)
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        axes = ((x2 - x1) // 2, (y2 - y1) // 2)
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
    
    mask = cv2.GaussianBlur(mask, (21, 21), 0)
    mask = mask / 255.0
    mask = np.stack([mask] * 3, axis=2)
    result = (result * mask + blurred * (1 - mask)).astype(np.uint8)
    return result


def add_soft_filter(image, intensity=0.3):
    """Thêm filter mềm mại (soft glow effect)"""
    blurred = cv2.GaussianBlur(image, (0, 0), 10)
    result = cv2.addWeighted(image, 1 - intensity, blurred, intensity, 0)
    return result