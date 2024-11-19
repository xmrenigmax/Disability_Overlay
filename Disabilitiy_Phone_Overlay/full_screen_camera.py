from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class FullScreenCamera(Screen):
    def __init__(self, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Create the camera widget
        self.camera = Camera(play=True)
        self.layout.add_widget(self.camera)
        
        # Create a button to switch cameras
        self.switch_button = Button(text='Switch Camera', size_hint=(None, None), size=('150dp', '48dp'))
        self.switch_button.bind(on_release=self.switch_camera)
        self.layout.add_widget(self.switch_button)
        
        # Add the layout to the screen
        self.add_widget(self.layout)
        
        # Track the current camera index
        self.current_camera_index = 0
    
    def switch_camera(self, instance):
        # Check if the camera supports switching
        if hasattr(self.camera, 'index'):
            new_camera_index = (self.current_camera_index + 1) % 2  # Assuming 2 cameras (front and back)
            try:
                # Ensure the new camera index is within the valid range
                if new_camera_index < len(self.camera.available_cameras):
                    self.camera.index = new_camera_index
                    self.current_camera_index = new_camera_index
                else:
                    print("No camera to flip")
            except AttributeError:
                print("No camera to flip")
        else:
            print("No camera to flip")
    
    def start_camera(self, instance):
        self.camera.play = True
