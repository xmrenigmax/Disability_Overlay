# src/camera/filters.py
import cv2
import numpy as np
from typing import Optional, Dict, Any
from kivy.logger import Logger

class ColorFilters:
    """
    Handles image filtering for accessibility features.
    
    Features:
    - Colorblindness simulation/correction
    - Contrast enhancement
    - Brightness adjustment
    - Custom color mapping
    """
    
    # Colorblindness conversion matrices
    COLORBLIND_MATRICES = {
        'deuteranopia': np.array([
            [0.625, 0.375, 0],
            [0.7, 0.3, 0],
            [0, 0.3, 0.7]
        ]),
        'protanopia': np.array([
            [0.567, 0.433, 0],
            [0.558, 0.442, 0],
            [0, 0.242, 0.758]
        ]),
        'tritanopia': np.array([
            [0.95, 0.05, 0],
            [0, 0.433, 0.567],
            [0, 0.475, 0.525]
        ])
    }
    
    def __init__(self):
        self.current_filter = None
        self.brightness = 1.0
        self.contrast = 1.0
        
    def apply_filter(self, frame: np.ndarray, filter_type: str, 
                    settings: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Apply specified filter to frame
        
        Args:
            frame: Input image frame
            filter_type: Type of filter to apply
            settings: Optional filter settings
        """
        try:
            if filter_type in self.COLORBLIND_MATRICES:
                return self._apply_colorblind_filter(frame, filter_type)
            elif filter_type == 'high_contrast':
                return self._apply_contrast(frame, settings)
            elif filter_type == 'custom':
                return self._apply_custom_filter(frame, settings)
            else:
                return frame
                
        except Exception as e:
            Logger.error(f'Filter application failed: {str(e)}')
            return frame
            
    def _apply_colorblind_filter(self, frame: np.ndarray, 
                                filter_type: str) -> np.ndarray:
        """Apply colorblindness simulation/correction"""
        try:
            matrix = self.COLORBLIND_MATRICES[filter_type]
            return cv2.transform(frame, matrix)
        except Exception as e:
            Logger.error(f'Colorblind filter failed: {str(e)}')
            return frame
            
    def _apply_contrast(self, frame: np.ndarray, 
                       settings: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """Apply contrast and brightness adjustments"""
        try:
            # Get settings or use defaults
            contrast = settings.get('contrast', self.contrast) if settings else self.contrast
            brightness = settings.get('brightness', self.brightness) if settings else self.brightness
            
            # Apply adjustments
            adjusted = cv2.convertScaleAbs(
                frame,
                alpha=contrast,
                beta=brightness
            )
            return adjusted
            
        except Exception as e:
            Logger.error(f'Contrast adjustment failed: {str(e)}')
            return frame
            
    def _apply_custom_filter(self, frame: np.ndarray,
                           settings: Dict[str, Any]) -> np.ndarray:
        """Apply custom color mapping with brightness/contrast"""
        try:
            # Get color ranges
            lower_color = np.array(settings.get('lower_color', [0, 0, 0]))
            upper_color = np.array(settings.get('upper_color', [255, 255, 255]))
            
            # Apply brightness and contrast
            contrast = settings.get('contrast', self.contrast)
            brightness = settings.get('brightness', self.brightness)
            
            # Adjust brightness and contrast
            adjusted = cv2.convertScaleAbs(
                frame,
                alpha=contrast,
                beta=brightness * 100
            )
            
            # Create mask for color range
            mask = cv2.inRange(adjusted, lower_color, upper_color)
            
            # Apply color emphasis
            result = adjusted.copy()
            result[mask > 0] = settings.get('target_color', [255, 255, 255])
            
            return result
            
        except Exception as e:
            Logger.error(f'Custom filter failed: {str(e)}')
            return frame
    
    def reset_filters(self) -> None:
        """Reset all filter settings to default"""
        self.current_filter = None
        self.brightness = 1.0
        self.contrast = 1.0
        self.active_color_profile = None
        self.custom_settings = {}
        self._last_frame = None
        Logger.info('Filters reset to default')
        
    def get_current_state(self) -> Dict[str, Any]:
        """Get current filter state"""
        return {
            'current_filter': self.current_filter,
            'brightness': self.brightness,
            'contrast': self.contrast,
            'active_profile': self.active_color_profile,
            'custom_settings': self.custom_settings
        }