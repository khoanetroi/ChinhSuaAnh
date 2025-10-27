# -*- coding: utf-8 -*-
"""Processors Package - Image Processing Strategies (Strategy Pattern)"""

from .BaseProcessor import BaseProcessor, ProcessorConfig
from .EdgeDetectionProcessor import EdgeDetectionProcessor, EdgeDetectionType
from .TransformProcessor import TransformProcessor, TransformType
from .BlurProcessor import BlurProcessor, BlurType
from .BrightnessProcessor import BrightnessProcessor, BrightnessOperation
from .SharpenProcessor import SharpenProcessor, SharpenType
from .FaceBeautifyProcessor import FaceBeautifyProcessor, FaceBeautifyType

__all__ = [
    'BaseProcessor', 'ProcessorConfig',
    'EdgeDetectionProcessor', 'EdgeDetectionType',
    'TransformProcessor', 'TransformType',
    'BlurProcessor', 'BlurType',
    'BrightnessProcessor', 'BrightnessOperation',
    'SharpenProcessor', 'SharpenType',
    'FaceBeautifyProcessor', 'FaceBeautifyType'
]
