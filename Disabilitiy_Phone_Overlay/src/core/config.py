# src/core/config.py
from kivy.utils import platform
from kivy.metrics import dp
from typing import Dict, Any, Tuple

class AppConfig:
    """
    Application configuration handling platform-specific settings
    
    Manages:
    - Window configurations
    - UI metrics
    - Feature flags
    - Color schemes
    """
    
    # Base window dimensions
    MIN_WIDTH = 320
    MIN_HEIGHT = 480
    
    # Default colors
    COLORS = {
        'primary': (0.2, 0.6, 1, 1),     # Blue
        'secondary': (0.3, 0.8, 0.4, 1),  # Green
        'accent': (0.9, 0.6, 0.2, 1),     # Orange
        'background': (0, 0, 0, 1),       # Black
        'text': (1, 1, 1, 1)              # White
    }
    
    # UI metrics
    UI_METRICS = {
        'button_height': dp(48),
        'button_width': dp(150),
        'padding': dp(20),
        'spacing': dp(10)
    }

    @staticmethod
    def get_platform_config() -> Dict[str, Any]:
        """Get platform-specific configuration"""
        base_config = {
            'min_resolution': (AppConfig.MIN_WIDTH, AppConfig.MIN_HEIGHT),
            'orientation': 'portrait',
            'fullscreen': 'auto',
            'status_bar': True
        }
        
        if platform == 'android':
            return {
                **base_config,
                'window_state': None,
                'permissions': [
                    'CAMERA',
                    'WRITE_EXTERNAL_STORAGE',
                    'READ_EXTERNAL_STORAGE'
                ]
            }
            
        elif platform == 'ios':
            return {
                **base_config,
                'window_state': None,
                'permissions_plist': {
                    'NSCameraUsageDescription': 'Camera access is required for scanning',
                    'NSPhotoLibraryUsageDescription': 'Photo library access is required for saving scans'
                }
            }
            
        else:  # Windows
            return {
                'fullscreen': True,
                'window_state': 'maximized',
                'orientation': 'landscape',
                'min_resolution': (1280, 720),
                'status_bar': False,
                'dpi_settings': {
                    'KIVY_DPI': '96',
                    'KIVY_METRICS_DENSITY': '1'
                }
            }

    @staticmethod
    def get_feature_flags() -> Dict[str, bool]:
        """Get platform-specific feature availability"""
        return {
            'camera_available': True,
            'file_scanner_available': platform == 'win',
            'quick_scan_available': True,
            'color_filters_enabled': True,
            'translation_enabled': True
        }
    
    @staticmethod
    def get_ui_metrics() -> Dict[str, Any]:
        """Get platform-adjusted UI metrics"""
        metrics = AppConfig.UI_METRICS.copy()
        
        if platform in ('android', 'ios'):
            # Adjust for mobile
            metrics['button_height'] = dp(56)
            metrics['padding'] = dp(16)
            
        return metrics
    
    @staticmethod
    def get_screen_config(screen_name: str) -> Dict[str, Any]:
        """Get screen-specific configuration"""
        configs = {
            'main': {
                'title': 'Accessibility Scanner',
                'show_back_button': False
            },
            'camera': {
                'title': 'Scanner',
                'show_back_button': True,
                'camera_controls': True
            },
            'settings': {
                'title': 'Settings',
                'show_back_button': True
            }
        }
        return configs.get(screen_name, {})