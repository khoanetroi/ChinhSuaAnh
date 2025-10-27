# -*- coding: utf-8 -*-
"""
FaceBeautifyCamera.py - Fix nhấp nháy màn hình
"""

# IMPORTANT: Fix Tkinter path issue BEFORE importing tkinter
import fix_tkinter  # This sets TCL_LIBRARY and TK_LIBRARY

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import queue
import time


class FaceBeautifyCameraWindow:
    """Cửa sổ camera - Fix nhấp nháy display"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("📹 Camera - Nhận Diện & Làm Đẹp Khuôn Mặt")
        self.window.geometry("1100x750")
        self.window.configure(bg="#f0f0f0")
        
        # Camera
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.faces = []
        
        # Queue để truyền frame từ thread sang main thread
        self.frame_queue = queue.Queue(maxsize=2)
        
        # Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Settings
        self.show_detection = tk.BooleanVar(value=True)
        self.apply_beautify = tk.BooleanVar(value=False)
        self.smooth_level = tk.DoubleVar(value=0.5)
        self.brightness_value = tk.IntVar(value=15)
        
        self.captured_image = None
        
        # Giảm nhấp nháy
        self.frame_count = 0
        self.detection_interval = 20  # Nhận diện mỗi 20 frames
        
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Tạo giao diện"""
        
        # Header
        header = tk.Frame(self.window, bg="#2c3e50", height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title = tk.Label(
            header, text="📹 CAMERA - NHẬN DIỆN & LÀM ĐẸP",
            font=("Arial", 20, "bold"), bg="#2c3e50", fg="white"
        )
        title.pack(pady=20)
        
        # Main container
        main = tk.Frame(self.window, bg="#f0f0f0")
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel
        left_panel = tk.Frame(main, bg="white", width=280, relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Camera controls
        tk.Label(left_panel, text="📹 ĐIỀU KHIỂN CAMERA", 
                font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(pady=(15, 10))
        
        self.btn_start = self.create_button(left_panel, "▶ Bật Camera", self.start_camera, "#27ae60")
        self.btn_stop = self.create_button(left_panel, "⏸ Tắt Camera", self.stop_camera, "#e74c3c")
        self.btn_stop.config(state=tk.DISABLED)
        
        self.btn_capture = self.create_button(left_panel, "📸 Chụp Ảnh", self.capture_image, "#3498db")
        self.btn_capture.config(state=tk.DISABLED)
        
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Settings
        tk.Label(left_panel, text="⚙️ CÀI ĐẶT", 
                font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(pady=(5, 10))
        
        check_frame = tk.Frame(left_panel, bg="white")
        check_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Checkbutton(check_frame, text="Hiện khung nhận diện", variable=self.show_detection,
                      bg="white", font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(check_frame, text="Áp dụng làm đẹp", variable=self.apply_beautify,
                      bg="white", font=("Arial", 10)).pack(anchor="w")
        
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Beautify settings
        tk.Label(left_panel, text="✨ ĐIỀU CHỈNH LÀM ĐẸP", 
                font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(pady=(5, 10))
        
        self.create_slider(left_panel, "Làm mịn da:", self.smooth_level, 0.0, 1.0)
        self.create_slider(left_panel, "Độ sáng:", self.brightness_value, 0, 50, resolution=1)
        
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Info
        info_frame = tk.Frame(left_panel, bg="white")
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.info_label = tk.Label(info_frame, text="Chưa bật camera",
                                   font=("Arial", 9), bg="white", fg="#7f8c8d", justify=tk.LEFT)
        self.info_label.pack(anchor="w")
        
        # Right panel - Video
        right_panel = tk.Frame(main, bg="white", relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.video_label = tk.Label(right_panel, text="📹\n\nNhấn 'Bật Camera' để bắt đầu",
                                    font=("Arial", 16), bg="white", fg="#95a5a6")
        self.video_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Status bar
        status_frame = tk.Frame(self.window, bg="#34495e", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="Sẵn sàng - Nhấn 'Bật Camera' để bắt đầu",
                                     font=("Arial", 10), bg="#34495e", fg="white", anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
    
    def create_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command, font=("Arial", 11, "bold"),
                       bg=color, fg="white", relief=tk.FLAT, cursor="hand2", height=2)
        btn.pack(fill=tk.X, padx=15, pady=5)
        return btn
    
    def create_slider(self, parent, label_text, variable, from_, to, resolution=0.1):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(frame, text=label_text, font=("Arial", 9), bg="white", fg="#2c3e50").pack(anchor="w")
        ttk.Scale(frame, from_=from_, to=to, variable=variable, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=3)
        tk.Label(frame, textvariable=variable, font=("Arial", 8), bg="white", fg="#7f8c8d").pack(anchor="e")
    
    def update_status(self, message):
        self.status_label.config(text=message)
    
    def start_camera(self):
        """Bật camera"""
        if self.is_running:
            return
        
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Lỗi", "Không thể mở camera!")
            return
        
        # Cài đặt camera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.is_running = True
        self.frame_count = 0
        self.faces = []
        
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_capture.config(state=tk.NORMAL)
        self.update_status("✓ Camera đang chạy")
        
        # Start 2 threads: 1 cho capture, 1 cho display
        threading.Thread(target=self.capture_video, daemon=True).start()
        self.update_display()  # Chạy trong main thread
    
    def stop_camera(self):
        """Tắt camera"""
        self.is_running = False
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_capture.config(state=tk.DISABLED)
        
        self.video_label.config(image="", text="📹\n\nNhấn 'Bật Camera' để bắt đầu")
        self.update_status("Camera đã tắt")
    
    def capture_video(self):
        """Thread capture video từ camera"""
        while self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Nhận diện mỗi 20 frames
            if self.frame_count % self.detection_interval == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                
                detected_faces = self.face_cascade.detectMultiScale(
                    gray, 
                    scaleFactor=1.2,
                    minNeighbors=7,
                    minSize=(80, 80),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                if len(detected_faces) > 0:
                    self.faces = list(detected_faces)
            
            self.frame_count += 1
            
            # Làm đẹp
            if self.apply_beautify.get() and len(self.faces) > 0:
                frame = self.apply_beautification(frame)
            
            # Vẽ khung
            if self.show_detection.get() and len(self.faces) > 0:
                for (x, y, w, h) in self.faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            self.current_frame = frame.copy()
            
            # Đưa frame vào queue
            if not self.frame_queue.full():
                self.frame_queue.put(frame)
            
            time.sleep(0.033)  # ~30 FPS
        
        if self.cap is not None:
            self.cap.release()
    
    def update_display(self):
        """Update display trong main thread (không nhấp nháy)"""
        if not self.is_running:
            return
        
        try:
            # Lấy frame từ queue
            if not self.frame_queue.empty():
                frame = self.frame_queue.get_nowait()
                
                # Update info
                face_count = len(self.faces)
                info_text = f"Camera đang chạy\nSố khuôn mặt: {face_count}"
                if self.apply_beautify.get():
                    info_text += "\nĐang làm đẹp: ✓"
                self.info_label.config(text=info_text)
                
                # Display frame
                self.display_frame(frame)
        except:
            pass
        
        # Schedule next update
        if self.is_running:
            self.window.after(33, self.update_display)  # ~30 FPS
    
    def apply_beautification(self, frame):
        """Áp dụng làm đẹp"""
        result = frame.copy()
        
        for (x, y, w, h) in self.faces:
            face_roi = result[y:y+h, x:x+w]
            
            # Làm mịn
            smooth = self.smooth_level.get()
            if smooth > 0:
                d = int(9 + smooth * 15)
                sigma_color = int(50 + smooth * 80)
                sigma_space = int(50 + smooth * 80)
                smoothed = cv2.bilateralFilter(face_roi, d, sigma_color, sigma_space)
                alpha = 0.3 + smooth * 0.5
                face_roi = cv2.addWeighted(face_roi, 1-alpha, smoothed, alpha, 0)
            
            # Làm sáng
            brightness = self.brightness_value.get()
            if brightness > 0:
                face_roi = cv2.convertScaleAbs(face_roi, alpha=1.0, beta=brightness)
            
            result[y:y+h, x:x+w] = face_roi
        
        return result
    
    def display_frame(self, frame):
        """Hiển thị frame"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame_rgb.shape[:2]
        max_width, max_height = 750, 600
        
        aspect = w / h
        if aspect > 1:
            new_w = min(w, max_width)
            new_h = int(new_w / aspect)
        else:
            new_h = min(h, max_height)
            new_w = int(new_h * aspect)
        
        frame_rgb = cv2.resize(frame_rgb, (new_w, new_h))
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk, text="")
    
    def capture_image(self):
        """Chụp ảnh"""
        if self.current_frame is None:
            messagebox.showwarning("Cảnh báo", "Không có frame nào để chụp!")
            return
        
        self.captured_image = self.current_frame.copy()
        
        result = messagebox.askyesno(
            "Xác nhận",
            f"Đã chụp ảnh (phát hiện {len(self.faces)} khuôn mặt)!\n\n"
            "Bạn có muốn áp dụng ảnh này vào cửa sổ chính không?"
        )
        
        if result:
            self.parent.current_image = self.captured_image
            self.parent.display_current_image()
            self.parent.update_status("✓ Đã áp dụng ảnh từ camera")
            messagebox.showinfo("Thành công", "Đã áp dụng ảnh vào cửa sổ chính!")
    
    def on_closing(self):
        """Đóng cửa sổ"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        self.window.destroy()