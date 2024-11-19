from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera

class CameraOverlay(FloatLayout):
    def __init__(self, **kwargs):
        super(CameraOverlay, self).__init__(**kwargs)
        self.camera = Camera(play=True)
        self.add_widget(self.camera)
