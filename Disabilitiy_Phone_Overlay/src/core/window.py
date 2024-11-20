# src/core/window.py
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger
from kivy.clock import Clock
from typing import Tuple, Optional
import ctypes

class WindowManager:
    """
    Handles window configuration and management across platforms
    
    Features:
    - Window size management
    - DPI scaling
    - Fullscreen handling
    - Platform-specific adjustments
    """
    
    def __init__(self):
        self._window_configured: bool = False
        self._fullscreen_enabled: bool = False
        Window.bind(
            on_resize=self._handle_resize,
            on_restore=self.restore_fullscreen
        )
    
    def configure_window(self, min_width: int, min_height: int) -> bool:
        """
        Configure window with platform-specific settings
        
        Args:
            min_width: Minimum window width
            min_height: Minimum window height
        """
        try:
            # Set minimum dimensions
            Window.minimum_width = min_width
            Window.minimum_height = min_height
            
            # Basic setup
            Window.clearcolor = (0, 0, 0, 1)
            
            # Platform specific configuration
            if platform == 'win':
                self._configure_windows()
            elif platform in ('android', 'ios'):
                self._configure_mobile()
                
            self._window_configured = True
            Logger.info('Window: Configuration completed')
            return True
            
        except Exception as e:
            Logger.error(f'Window configuration failed: {str(e)}')
            return False
    
    def _configure_windows(self) -> None:
        """Configure Windows-specific window settings"""
        try:
            # Set DPI awareness
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                ctypes.windll.user32.SetProcessDPIAware()
            
            # Configure window state
            Window.maximize()
            Window.fullscreen = True
            self._fullscreen_enabled = True
            
        except Exception as e:
            Logger.warning(f'Windows configuration failed: {str(e)}')
    
    def _configure_mobile(self) -> None:
        """Configure mobile platform window settings"""
        Window.fullscreen = 'auto'
        Window.orientation = 'portrait'
    
    def _handle_resize(self, instance, width: int, height: int) -> None:
        """
        Handle window resize events
        
        Args:
            width: New window width
            height: New window height
        """
        try:
            if platform == 'win':
                # Enforce minimum dimensions on desktop
                if width < Window.minimum_width or height < Window.minimum_height:
                    Window.size = (
                        max(width, Window.minimum_width),
                        max(height, Window.minimum_height)
                    )
                    
            Logger.debug(f'Window resized to: {width}x{height}')
            
        except Exception as e:
            Logger.error(f'Resize handling failed: {str(e)}')
    
    def restore_fullscreen(self, *args) -> None:
        """Restore window state after minimize/maximize"""
        if platform == 'win' and self._fullscreen_enabled:
            try:
                Window.maximize()
                Window.fullscreen = True
                Logger.info('Window: Fullscreen restored')
            except Exception as e:
                Logger.error(f'Fullscreen restoration failed: {str(e)}')
    
    def get_window_size(self) -> Tuple[int, int]:
        """Get current window dimensions"""
        return Window.size
    
    def set_fullscreen(self, enable: bool) -> None:
        """
        Toggle fullscreen mode
        
        Args:
            enable: True to enable fullscreen, False to disable
        """
        if platform == 'win':
            Window.fullscreen = enable
            self._fullscreen_enabled = enable
            if not enable:
                Window.maximize()
    
    @property
    def is_configured(self) -> bool:
        """Check if window is configured"""
        return self._window_configured