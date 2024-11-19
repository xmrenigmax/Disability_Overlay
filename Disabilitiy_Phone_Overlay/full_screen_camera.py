from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
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
        
        # Initialize processors
        self.text_processor = TextProcessor()
        self.color_filters = ColorFilters()
        
        # Create main layout
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        
        # Status label for feedback
        self.status_label = Label(
            text="Initializing camera...",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.status_label)
        
        # Initialize camera later
        self.camera = None
        self.current_camera_index = 0
        
        # Create UI elements
        self.create_buttons()
        
        # Schedule camera initialization
        Clock.schedule_once(self.initialize_camera, 0.5)

    def initialize_camera(self, dt=None):
        """Initialize camera asynchronously with error handling"""
        try:
            # Initialize OpenCV capture first
            import cv2
            self.cv2_cap = cv2.VideoCapture(0)
            if not self.cv2_cap.isOpened():
                raise Exception("Failed to open camera")

            # Get supported resolution
            width = int(self.cv2_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cv2_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
            # Create Kivy camera with detected resolution
            self.camera = Camera(
                play=True,
                index=0,
                resolution=(width, height),
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0}
            )
                    
            # Add camera to layout
            self.layout.add_widget(self.camera, index=0)
            
            # Set up handlers
            Window.bind(on_resize=self.on_window_resize)
            self.camera.bind(on_texture=self.on_camera_frame)
            
            # Update status
            self.status_label.text = "Camera ready"
            Clock.schedule_once(lambda dt: self.layout.remove_widget(self.status_label), 2)
                
        except Exception as e:
            self.status_label.text = f"Camera error: {str(e)}"
            print(f"Camera initialization failed: {str(e)}")

    def _test_camera(self, dt):
        """Test if camera is capturing frames"""
        if not self.camera or not self.camera._camera:
            self.status_label.text = "Camera initialization failed"
            return False
        
        try:
            # Try to grab a test frame
            if not self.camera.texture:
                print("No camera texture available")
                return False
        except Exception as e:
            print(f"Camera test failed: {str(e)}")
            return False
        
        return True

    def create_buttons(self):
        """Create UI buttons"""
        # Camera switch button
        self.switch_button = Button(
            text='Switch Camera',
            size_hint=(None, None),
            size=('150dp', '48dp'),
            pos_hint={'right': 0.98, 'top': 0.98}
        )
        self.switch_button.bind(on_release=self.switch_camera)
        self.layout.add_widget(self.switch_button)
        
        # Color filter button
        self.filter_button = Button(
            text='Color Filter',
            size_hint=(None, None),
            size=('150dp', '48dp'),
            pos_hint={'right': 0.98, 'top': 0.88}
        )
        self.filter_button.bind(on_release=self.show_filter_options)
        self.layout.add_widget(self.filter_button)

    def on_camera_frame(self, instance, value):
        """Process new camera frames with error handling"""
        if not self.camera or not self.camera.texture:
            return
            
        try:
            # Convert texture to numpy array with error checking
            pixels = self.camera.texture.pixels
            if not pixels:
                return
                
            pixels = np.frombuffer(pixels, dtype=np.uint8)
            if pixels.size == 0:
                return
                
            width = self.camera.texture.width
            height = self.camera.texture.height
            
            frame = pixels.reshape(height, width, 4)  # RGBA format
            if frame is None:
                return
                
            frame = frame[:, :, :3]  # Convert to RGB
            
            # Process frame for text
            text = self.text_processor.detect_text(frame)
            if text:
                self.show_detected_text(text)
                
        except Exception as e:
            print(f"Frame processing error: {str(e)}")

    def switch_camera(self, instance):
        """Safely switch between available cameras"""
        if not self.camera:
            return
            
        try:
            import cv2
            # Test next camera index
            next_index = (self.current_camera_index + 1) % 2
            test_cap = cv2.VideoCapture(next_index)
            
            if test_cap.isOpened():
                test_cap.release()
                # Switch camera
                self.camera.index = next_index
                self.current_camera_index = next_index
            else:
                self.status_label.text = "Only one camera available"
                self.layout.add_widget(self.status_label)
                Clock.schedule_once(
                    lambda dt: self.layout.remove_widget(self.status_label), 
                    2
                )
        except Exception as e:
            print(f"Camera switch failed: {str(e)}")

    def show_detected_text(self, text):
        """Display detected text as draggable overlay"""
        text_widget = DraggableText(
            text=text,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(text_widget)

    def show_filter_options(self, instance):
        """Show color filter selection dialog"""
        # TODO: Implement color filter options
        pass

    def on_window_resize(self, instance, width, height):
        """Handle window resize events"""
        if self.camera:
            self.camera.size = (width, height)
            
    def on_leave(self):
        """Cleanup when leaving screen"""
        if hasattr(self, 'cv2_cap'):
            self.cv2_cap.release()
        if self.camera:
            self.camera.play = False