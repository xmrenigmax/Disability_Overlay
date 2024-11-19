from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np
from text_processor import TextProcessor 
from text_overlay import DraggableText
from color_filters import ColorFilters


class FullScreenCamera(Screen):
    def __init__(self, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        self.text_processor = TextProcessor()
        self.color_filters = ColorFilters()
        
        # Create layout that fills the screen
        self.layout = FloatLayout()
        
        # Create camera that fills the entire screen
        self.camera = Camera(
            play=True,
            index=0,
            resolution=(1920, 1080),
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        
        # Add camera to layout
        self.layout.add_widget(self.camera)
        
        # Create buttons
        self.create_buttons()
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Initialize camera index
        self.current_camera_index = 0
        
        # Set up window handling
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(self.update_camera_size, 0.1)
        
        # Bind to texture updates for frame processing
        self.camera.bind(on_texture=self.on_texture)

    def create_buttons(self):
        # Switch camera button
        self.switch_button = Button(
            text='Switch Camera',
            size_hint=(None, None),
            size=('150dp', '48dp'),
            pos_hint={'right': 0.98, 'top': 0.98}
        )
        self.switch_button.bind(on_release=self.switch_camera)
        self.layout.add_widget(self.switch_button)
        
        # Filter button
        self.filter_button = Button(
            text='Color Filter',
            size_hint=(None, None),
            size=('150dp', '48dp'),
            pos_hint={'right': 0.98, 'top': 0.88}
        )
        self.filter_button.bind(on_release=self.show_filter_options)
        self.layout.add_widget(self.filter_button)

    def on_texture(self, instance, value):
        """Called when camera texture updates"""
        if self.camera.texture:
            # Get texture pixels as numpy array
            pixels = np.frombuffer(self.camera.texture.pixels, dtype=np.uint8)
            # Reshape to image dimensions
            width = self.camera.texture.width
            height = self.camera.texture.height
            frame = pixels.reshape(height, width, 4)  # RGBA format
            # Convert to RGB for processing
            frame = frame[:, :, :3]
            
            # Process frame
            if frame is not None:
                text = self.text_processor.detect_text(frame)
                if text:
                    self.show_detected_text(text)

    def update_camera_size(self, dt):
        self.camera.size = Window.size
        self.camera.pos = (0, 0)

    def on_window_resize(self, instance, width, height):
        self.camera.size = (width, height)
        
    def switch_camera(self, instance):
        if hasattr(self.camera, 'index'):
            try:
                # Get number of available cameras
                num_cameras = len(self.camera._camera.get_devices())
                
                if num_cameras > 1:
                    # Only switch if multiple cameras exist
                    new_camera_index = (self.current_camera_index + 1) % num_cameras
                    self.camera.index = new_camera_index
                    self.current_camera_index = new_camera_index
                else:
                    print("Only one camera available")
                    # Could add UI feedback here if desired
                    
            except Exception as e:
                print(f"Camera switch failed: {str(e)}")

    def show_detected_text(self, text):
        draggable_text = DraggableText(text=text)
        self.layout.add_widget(draggable_text)

    def show_filter_options(self, instance):
        """Show color filter options"""
        pass