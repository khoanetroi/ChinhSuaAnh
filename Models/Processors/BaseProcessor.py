# -*- coding: utf-8 -*-
"""BaseProcessor.py - Abstract base for all processors (OCP, DIP)"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass, field
import numpy as np


@dataclass
class ProcessorConfig:
    """Configuration for processors"""
    params: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.params.get(key, default)

    def set(self, key: str, value: Any):
        self.params[key] = value


class BaseProcessor(ABC):
    """Abstract base for all image processors. Follows SOLID principles."""

    def __init__(self, name: str, config: ProcessorConfig = None):
        self.name = name
        self.config = config if config is not None else ProcessorConfig()

    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """Process image and return result"""
        pass

    def validate_image(self, image: np.ndarray):
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            raise ValueError(f"{self.name}: Invalid image")
