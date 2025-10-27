# -*- coding: utf-8 -*-
"""ImageHistory.py - Undo/Redo management (Command Pattern)"""

import numpy as np
from typing import Optional
from collections import deque


class ImageHistory:
    """Manages undo/redo history. Single Responsibility: History only."""

    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.undo_stack: deque = deque(maxlen=max_history)
        self.redo_stack: deque = deque(maxlen=max_history)

    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()

    def set_initial(self, image: np.ndarray):
        self.clear()
        if image is not None:
            self.undo_stack.append(image.copy())

    def push(self, image: np.ndarray):
        if image is None:
            return
        if self.undo_stack and np.array_equal(image, self.undo_stack[-1]):
            return
        self.undo_stack.append(image.copy())
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        return len(self.undo_stack) > 1

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def undo(self, current_image: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        if not self.can_undo():
            return None
        if current_image is not None:
            self.redo_stack.append(current_image.copy())
        self.undo_stack.pop()
        return self.undo_stack[-1].copy()

    def redo(self) -> Optional[np.ndarray]:
        if not self.can_redo():
            return None
        restored = self.redo_stack.pop()
        self.undo_stack.append(restored.copy())
        return restored.copy()
