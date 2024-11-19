from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.app import App
from kivy.core.window import Window

class FullScreenCamera(Screen):
    def __init__(self, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        self.camera = Camera(play=True)
        self.add_widget(self.camera)

class FullScreenCameraApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FullScreenCamera(name='camera'))
        return sm

    def on_start(self):
        Window.fullscreen = 'auto'
