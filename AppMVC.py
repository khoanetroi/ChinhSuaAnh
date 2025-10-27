# -*- coding: utf-8 -*-
"""
AppMVC.py - Image Editing Application using MVC Architecture
Main entry point for the refactored MVC application

Features:
- Blur & Smoothing
- Brightness/Contrast adjustment
- Sharpening
- Edge Detection
- Transform operations
- Face detection and beautification

Architecture:
- Model: ImageModel, ImageHistory, Processors
- View: MainView (UI components)
- Controller: MainController (business logic)
- Services: ImageService, FileService, FaceDetectionService
"""

# IMPORTANT: Fix Tkinter path issue BEFORE importing tkinter
import fix_tkinter  # This sets TCL_LIBRARY and TK_LIBRARY

import tkinter as tk
from Controllers import MainController


def main():
    """Main entry point for the MVC application"""
    # Create Tkinter root window
    root = tk.Tk()

    # Create and run controller (which initializes Model, View, and Services)
    controller = MainController(root)
    controller.run()


if __name__ == "__main__":
    main()
