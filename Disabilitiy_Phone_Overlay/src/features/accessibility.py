# src/features/accessibility.py
from typing import Dict, Any, Optional, List
from ..utils.logger import app_logger as logger
from ..core.config import AppConfig

class AccessibilityManager:
    """
    Manages accessibility features for text scanning and display.
    Handles color correction, text enhancement, and UI adaptations.
    """
    
    # Color correction profiles
    COLOR_FILTERS = {
        'deuteranopia': {
            'name': 'Red-Green (Common)',
            'matrix': [
                [0.625, 0.375, 0],
                [0.7, 0.3, 0],
                [0, 0.3, 0.7]
            ]
        },
        'protanopia': {
            'name': 'Red-Green (Rare)',
            'matrix': [
                [0.567, 0.433, 0],
                [0.558, 0.442, 0],
                [0, 0.242, 0.758]
            ]
        },
        'tritanopia': {
            'name': 'Blue-Yellow',
            'matrix': [
                [0.95, 0.05, 0],
                [0, 0.433, 0.567],
                [0, 0.475, 0.525]
            ]
        },
        'high_contrast': {
            'name': 'High Contrast',
            'contrast': 1.5,
            'brightness': 1.2
        }
    }
    
    # Text display profiles
    TEXT_PROFILES = {
        'dyslexic': {
            'font_name': 'OpenDyslexic',
            'font_size': 1.2,
            'line_spacing': 1.5,
            'word_spacing': 1.3
        },
        'large_print': {
            'font_size': 1.5,
            'contrast': 1.3,
            'font_weight': 'bold'
        },
        'high_legibility': {
            'font_name': 'Arial',
            'letter_spacing': 1.2,
            'contrast': 1.2
        }
    }

    def __init__(self):
        self.config = AppConfig()
        self.active_color_filter = None
        self.active_text_profile = None
        self.custom_settings = {
            'font_size': 1.0,
            'contrast': 1.0,
            'brightness': 1.0,
            'word_spacing': 1.0
        }
        
    def get_available_filters(self) -> List[Dict[str, str]]:
        """Get list of available color filters"""
        return [
            {'id': k, 'name': v['name']} 
            for k, v in self.COLOR_FILTERS.items()
        ]
        
    def get_text_profiles(self) -> List[Dict[str, str]]:
        """Get available text enhancement profiles"""
        return [
            {'id': k, 'name': k.replace('_', ' ').title()} 
            for k in self.TEXT_PROFILES.keys()
        ]
        
    def apply_color_filter(self, filter_id: str) -> bool:
        """Apply color correction filter"""
        try:
            if filter_id in self.COLOR_FILTERS:
                self.active_color_filter = filter_id
                logger.info(f"Applied color filter: {filter_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Color filter application failed: {str(e)}")
            return False
            
    def apply_text_profile(self, profile_id: str) -> bool:
        """Apply text enhancement profile"""
        try:
            if profile_id in self.TEXT_PROFILES:
                self.active_text_profile = profile_id
                self.custom_settings.update(self.TEXT_PROFILES[profile_id])
                logger.info(f"Applied text profile: {profile_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Text profile application failed: {str(e)}")
            return False
            
    def update_custom_settings(self, settings: Dict[str, float]) -> None:
        """Update custom accessibility settings"""
        try:
            self.custom_settings.update(settings)
            logger.info("Updated custom settings")
        except Exception as e:
            logger.error(f"Settings update failed: {str(e)}")
            
    def get_current_settings(self) -> Dict[str, Any]:
        """Get current accessibility settings"""
        return {
            'color_filter': self.active_color_filter,
            'text_profile': self.active_text_profile,
            'custom_settings': self.custom_settings
        }
        
    def get_filter_matrix(self) -> Optional[List[List[float]]]:
        """Get current color filter matrix"""
        if self.active_color_filter:
            return self.COLOR_FILTERS[self.active_color_filter].get('matrix')
        return None
        
    def reset_settings(self) -> None:
        """Reset all settings to default"""
        self.active_color_filter = None
        self.active_text_profile = None
        self.custom_settings = {
            'font_size': 1.0,
            'contrast': 1.0,
            'brightness': 1.0,
            'word_spacing': 1.0
        }
        logger.info("Reset accessibility settings")

# Global instance
accessibility_manager = AccessibilityManager()