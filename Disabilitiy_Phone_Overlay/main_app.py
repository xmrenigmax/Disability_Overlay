from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from main_screen import MainScreen
from loading_screen import LoadingScreen
from full_screen_camera import FullScreenCamera

class MainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoadingScreen(name='loading'))
        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(FullScreenCamera(name='full_screen_camera'))
        return self.screen_manager

if __name__ == '__main__':
    MainApp().run()
