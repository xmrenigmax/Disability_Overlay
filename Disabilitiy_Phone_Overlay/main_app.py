from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from main_screen import MainScreen
from loading_screen import LoadingScreen
from full_screen_camera import FullScreenCamera  # Ensure this import is present
from kivy.clock import Clock  # Add this import

class MainApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0, 0, 0, 1)
        Window.fullscreen = True  # Force true fullscreen
        Window.maximize()
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoadingScreen(name='loading'))
        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(FullScreenCamera(name='full_screen_camera'))
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

