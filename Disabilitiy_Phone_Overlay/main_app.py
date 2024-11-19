from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from main_screen import MainScreen

class MainApp(App):
    def build(self):
        # Create the ScreenManager
        sm = ScreenManager()
        
        # Add the MainScreen to the ScreenManager
        sm.add_widget(MainScreen(name='main_screen'))
        
        return sm

if __name__ == '__main__':
    MainApp().run()