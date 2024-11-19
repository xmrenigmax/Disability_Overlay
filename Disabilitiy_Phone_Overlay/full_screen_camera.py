from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout

class FullScreenCamera(Screen):
    def __init__(self, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        layout = BoxLayout()
        self.camera = Camera(play=True)
        layout.add_widget(self.camera)
        self.add_widget(layout)
