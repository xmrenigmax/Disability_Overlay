from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

class FullScreenCamera(Screen):
    def __init__(self, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        
        # Create layout that fills the screen
        self.layout = FloatLayout()
        
        # Create camera that fills the entire screen
        self.camera = Camera(
            play=True,
            index=0,
            resolution=(1920, 1080),  # HD resolution
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        
        # Force update camera size after initialization
        Clock.schedule_once(self.update_camera_size, 0.1)
        
        # Bind to window size changes
        Window.bind(on_resize=self.on_window_resize)
        
        # Add camera first so it's at the bottom layer
        self.layout.add_widget(self.camera)
        
        # Create switch button that floats on top
        self.switch_button = Button(
            text='Switch Camera',
            size_hint=(None, None),
            size=('150dp', '48dp'),
            pos_hint={'right': 0.98, 'top': 0.98}
        )
        self.switch_button.bind(on_release=self.switch_camera)
        self.layout.add_widget(self.switch_button)
        
        # Add the layout to the screen
        self.add_widget(self.layout)
        
        # Track the current camera index
        self.current_camera_index = 0

    def update_camera_size(self, dt):
        """Update camera size to match window"""
        self.camera.size = Window.size
        self.camera.pos = (0, 0)

    def on_window_resize(self, instance, width, height):
        """Handle window resize events"""
        self.camera.size = (width, height)
        
    def switch_camera(self, instance):
        if hasattr(self.camera, 'index'):
            new_camera_index = (self.current_camera_index + 1) % 2
            try:
                if new_camera_index < len(self.camera.available_cameras):
                    self.camera.index = new_camera_index
                    self.current_camera_index = new_camera_index
            except AttributeError:
                print("No camera to flip")