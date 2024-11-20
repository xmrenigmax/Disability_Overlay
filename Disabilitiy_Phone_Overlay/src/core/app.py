# src/core/app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger
import os

from ..utils.permissions import request_permissions
from ..screens.main_screen import MainScreen
from ..screens.loading_screen import LoadingScreen
from ..screens.camera_screen import CameraScreen

class MainApp(App):
    """
    Main application class handling screen management and platform setup.
    
    Handles:
    - Screen navigation and history
    - Platform-specific initialization (iOS/Android/Windows)
    - Window configuration
    - Permission management
    """
    
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        # Core attributes
        self.screen_manager = None
        self._screens_initialized = False
        self.history = ['main']  # Screen navigation history
        
        # Set up platform-specific configurations
        self._configure_platform()
        
    def _configure_platform(self):
        """Set up platform-specific settings"""
        if platform == 'win':
            # Windows-specific setup
            os.environ['KIVY_DPI'] = '96'
            os.environ['KIVY_METRICS_DENSITY'] = '1'
            self._setup_windows_dpi()
        elif platform == 'android':
            # Android-specific setup
            self._request_android_permissions()
        elif platform == 'ios':
            # iOS-specific setup (handled in Info.plist)
            Logger.info('iOS: Platform configured')
            
    def _setup_windows_dpi(self):
        """Configure Windows DPI handling"""
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
            Logger.info('Windows: DPI awareness configured')
        except Exception as e:
            Logger.warning(f'Windows DPI configuration failed: {str(e)}')
            
    def _request_android_permissions(self):
        """Request necessary Android permissions"""
        try:
            from android.permissions import request_permissions, Permission # type: ignore
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            Logger.info('Android: Permissions requested')
        except Exception as e:
            Logger.error(f'Android permissions failed: {str(e)}')
            
    def build(self):
        """Initialize application UI and screens"""
        try:
            # Create screen manager
            self.screen_manager = ScreenManager(transition=NoTransition())
            
            # Initialize screens
            screens = {
                'main': MainScreen(name='main'),
                'loading': LoadingScreen(name='loading'),
                'camera': CameraScreen(name='camera')
            }
            
            # Add screens to manager
            for screen in screens.values():
                self.screen_manager.add_widget(screen)
                
            # Set initial screen
            self.screen_manager.current = 'main'
            self._screens_initialized = True
            
            return self.screen_manager
            
        except Exception as e:
            Logger.error(f'Application build failed: {str(e)}')
            return None
            
    def switch_screen(self, screen_name: str):
        """
        Switch to specified screen and update history
        
        Args:
            screen_name: Name of screen to switch to
        """
        if screen_name in self.screen_manager.screen_names:
            self.screen_manager.current = screen_name
            self.history.append(screen_name)
            Logger.info(f'Switched to screen: {screen_name}')
            
    def go_back(self):
        """Navigate to previous screen"""
        if len(self.history) > 1:
            self.history.pop()  # Remove current screen
            previous = self.history[-1]  # Get previous
            self.screen_manager.current = previous
            Logger.info(f'Navigated back to: {previous}')
            return True
        return False

# Entry point
if __name__ == '__main__':
    try:
        MainApp().run()
    except Exception as e:
        Logger.critical(f'Application crashed: {str(e)}')