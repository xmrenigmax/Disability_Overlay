from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from main_screen import MainScreen
from loading_screen import LoadingScreen
from full_screen_camera import FullScreenCamera 
from kivy.clock import Clock 

class MainApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0, 0, 0, 1)
        Window.fullscreen = True
        Window.maximize()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Add screens with consistent names
        loading_screen = LoadingScreen(name='loading')
        main_screen = MainScreen(name='main')
        camera_screen = FullScreenCamera(name='full_screen_camera')
        
        # Add screens to manager
        self.screen_manager.add_widget(loading_screen)
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(camera_screen)
        
        # Set initial screen
        self.screen_manager.current = 'loading'
        
        return self.screen_manager
    
    def restore_fullscreen(self, *args):
        """Restore fullscreen after permission dialogs"""
        from kivy.core.window import Window
        def restore(*args):
            Window.fullscreen = True
            Window.maximize()
        # Small delay to ensure window is ready
        Clock.schedule_once(restore, 0.1)

if __name__ == '__main__':
    MainApp().run()