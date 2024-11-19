# color_filters.py
import cv2
import numpy as np

class ColorFilters:
    def __init__(self):
        self.current_filter = None
        
    def apply_deuteranopia(self, frame):
        # Simulate deuteranopia color blindness
        matrix = np.array([
            [0.625, 0.375, 0],
            [0.7, 0.3, 0],
            [0, 0.3, 0.7]
        ])
        return cv2.transform(frame, matrix)
    
    def apply_protanopia(self, frame):
        # Simulate protanopia color blindness
        matrix = np.array([
            [0.567, 0.433, 0],
            [0.558, 0.442, 0],
            [0, 0.242, 0.758]
        ])
        return cv2.transform(frame, matrix)