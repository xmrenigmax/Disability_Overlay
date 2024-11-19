from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.utils import platform
from kivy.uix.image import Image
import numpy as np
import cv2
import time

class CameraManager:
    def __init__(self):
        self.capture = None
        self.current_api = None
        self.apis = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "Media Foundation"),
            (0, "Default")
        ]
    
    def initialize(self):
        """Try different APIs to initialize camera"""
        for api, name in self.apis:
            try:
                if isinstance(api, int):
                    self.capture = cv2.VideoCapture(api)
                else:
                    self.capture = cv2.VideoCapture(0 + api)
                
                if self.capture.isOpened():
                    # Test frame capture
                    ret, frame = self.capture.read()
                    if ret and frame is not None:
                        self.current_api = api
                        return True
                    self.capture.release()
            except Exception as e:
                print(f"Failed with {name}: {str(e)}")
                if self.capture:
                    self.capture.release()
                continue
        return False
    
    def get_frame(self):
        """Get frame with validation"""
        if not self.capture or not self.capture.isOpened():
            return None
            
        ret, frame = self.capture.read()
        if not ret or frame is None:
            # Try to recover
            self.capture.release()
            time.sleep(0.1)
            self.initialize()
            return None
        return frame
    
    def release(self):
        """Clean up resources"""
        if self.capture:
            self.capture.release()
            self.capture = None

class FullScreenCamera(Screen):
    def __init__(self, **kwargs):
        super(FullScreenCamera, self).__init__(**kwargs)
        
        # Main layout
        self.layout = FloatLayout()
        
        # Create camera preview widget
        self.preview = Image(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.layout.add_widget(self.preview)
        
        # Status label
        self.status_label = Label(
            text="Initializing camera...",
            pos_hint={'center_x': 0.5, 'top': 0.95},
            size_hint=(None, None)
        )
        self.layout.add_widget(self.status_label)
        
        # Create buttons
        self.create_buttons()
        
        # Add layout
        self.add_widget(self.layout)
        
        # Initialize state
        self.capture = None
        self.camera_active = False
        self.current_camera_index = 0
        self.available_cameras = self.detect_cameras()
        
        # Start camera
        Clock.schedule_once(self.initialize_camera, 0.1)

    def create_buttons(self):
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

    def detect_cameras(self):
        """Detect available cameras"""
        available = []
        for i in range(2):  # Check first two indices
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    available.append(i)
                cap.release()
            except:
                continue
        return available

    def initialize_camera(self, dt):
        """Initialize camera with valid index"""
        if not self.available_cameras:
            self.status_label.text = "No cameras found"
            self.switch_button.disabled = True
            return
            
        try:
            self.capture = cv2.VideoCapture(self.available_cameras[0])
            if self.capture.isOpened():
                self.camera_active = True
                Clock.schedule_interval(self.update_frame, 1.0/30.0)
                self.status_label.text = "Camera ready"
                Clock.schedule_once(
                    lambda dt: setattr(self.status_label, 'opacity', 0), 
                    2
                )
                
                # Update switch button state
                self.switch_button.disabled = len(self.available_cameras) <= 1
                
            else:
                self.status_label.text = "Failed to open camera"
                self.switch_button.disabled = True
                
        except Exception as e:
            self.status_label.text = f"Camera error: {str(e)}"
            self.switch_button.disabled = True

    def check_available_cameras(self):
        """Check number of available cameras"""
        try:
            test_cap = cv2.VideoCapture(1)  # Try second camera
            if test_cap.isOpened():
                self.has_multiple_cameras = True
                test_cap.release()
            else:
                self.has_multiple_cameras = False
                self.switch_button.disabled = True
                self.switch_button.opacity = 0.5
        except:
            self.has_multiple_cameras = False
            self.switch_button.disabled = True
            self.switch_button.opacity = 0.5


    def switch_camera(self, instance):
        """Switch between available cameras"""
        if not self.camera_active or len(self.available_cameras) <= 1:
            return
            
        try:
            # Get next camera index
            current_idx = self.available_cameras.index(self.current_camera_index)
            next_idx = (current_idx + 1) % len(self.available_cameras)
            new_index = self.available_cameras[next_idx]
            
            # Try new camera
            new_capture = cv2.VideoCapture(new_index)
            if new_capture.isOpened():
                if self.capture:
                    self.capture.release()
                self.capture = new_capture
                self.current_camera_index = new_index
            else:
                new_capture.release()
                
        except Exception as e:
            print(f"Camera switch failed: {str(e)}")

    def update_frame(self, dt):
        if not self.capture or not self.camera_active:
            return
            
        try:
            ret, frame = self.capture.read()
            if ret:
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]),
                    colorfmt='bgr'
                )
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.preview.texture = texture
        except Exception as e:
            print(f"Frame update error: {str(e)}")

    def show_filter_options(self, instance):
        """Show color filter options"""
        pass

    def on_leave(self):
        """Cleanup resources"""
        if self.capture:
            self.capture.release()
        Clock.unschedule(self.update_frame)