# src/screens/camera_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.logger import Logger
from kivy.graphics.texture import Texture
import cv2

from ..camera.manager import CameraManager
from ..camera.filters import ColorFilters
from ..core.config import AppConfig
from ..ui.popups import WordDetailsPopup

class CameraScreen(Screen):
    """
    Camera interface screen with controls and filters.
    
    Features:
    - Camera preview
    - Camera switching
    - Color filters
    - Brightness/Contrast controls
    - Frame capture
    """
    
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.config = AppConfig()
        
        # Initialize components
        self.camera_manager = CameraManager()
        self.color_filters = ColorFilters()
        
        # Create layouts
        self.layout = FloatLayout()
        
        # Create camera preview
        self.preview = Image(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.preview)
        
        # Add controls
        self.create_controls()
        self.add_widget(self.layout)
        
        # Bind to screen events
        self.bind(on_enter=self._start_camera)
        self.bind(on_leave=self._stop_camera)
        
    def create_ui(self):
        """Create UI elements"""
        # Create preview area
        self.preview = FloatLayout(size_hint=(1, 1))
        self.layout.add_widget(self.preview)
        
        # Create control buttons
        self.create_controls()
        
        # Add status label
        self.status_label = Label(
            text="Initializing camera...",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.layout.add_widget(self.status_label)
        
    def create_controls(self):
        """Create camera control buttons"""
        # Back button
        back_btn = Button(
            text='Back',
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'x': 0.02, 'top': 0.98}
        )
        back_btn.bind(on_release=self.go_back)
        self.layout.add_widget(back_btn)
        
        # Camera switch button
        switch_btn = Button(
            text='Switch Camera',
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            pos_hint={'right': 0.98, 'top': 0.98}
        )
        switch_btn.bind(on_release=self.switch_camera)
        self.layout.add_widget(switch_btn)
        
        # Filter button
        filter_btn = Button(
            text='Filters',
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'right': 0.98, 'top': 0.89}
        )
        filter_btn.bind(on_release=self.show_filter_options)
        self.layout.add_widget(filter_btn)
        
        # Capture button
        capture_btn = Button(
            text='Capture',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5, 'y': 0.02}
        )
        capture_btn.bind(on_release=self.capture_frame)
        self.layout.add_widget(capture_btn)
        
    def _start_camera(self, *args):
        """Initialize and start camera"""
        if self.camera_manager.initialize():
            Clock.schedule_interval(self.update_frame, 1.0/30.0)
        else:
            self.show_error("Camera initialization failed")
            
    def _stop_camera(self, *args):
        """Stop and release camera"""
        Clock.unschedule(self.update_frame)
        self.camera_manager.release()
        
    def update_frame(self, dt):
        """Update camera preview"""
        try:
            frame = self.camera_manager.get_frame()
            if frame is not None:
                # Convert frame to texture
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]),
                    colorfmt='bgr'
                )
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.preview.texture = texture
        except Exception as e:
            Logger.error(f"Frame update failed: {str(e)}")
                
    def switch_camera(self, instance):
        """Safely switch between cameras"""
        try:
            # Stop current camera
            Clock.unschedule(self.update_frame)
            self.camera_manager.release()
            
            # Try next camera index
            new_index = (self.camera_manager.current_index + 1) % 2
            
            # Test camera before switching
            test_cap = cv2.VideoCapture(new_index)
            if test_cap.isOpened():
                test_cap.release()
                # Initialize with new index
                if self.camera_manager.initialize(new_index):
                    Clock.schedule_interval(self.update_frame, 1.0/30.0)
                else:
                    self.show_error("Failed to switch camera")
                    # Restore original camera
                    self.camera_manager.initialize(self.camera_manager.current_index)
                    Clock.schedule_interval(self.update_frame, 1.0/30.0)
            else:
                self.show_error("No additional cameras available")
                # Restore original camera
                self.camera_manager.initialize(self.camera_manager.current_index)
                Clock.schedule_interval(self.update_frame, 1.0/30.0)
                
        except Exception as e:
            Logger.error(f"Camera switch failed: {str(e)}")
            self.show_error("Camera switch failed")
            
    def show_filter_options(self, instance):
        """Show color filter selection popup"""
        # Implementation needed for filter selection UI
        pass
        
    def capture_frame(self, instance):
        """Capture and process current frame"""
        frame = self.camera_manager.get_frame()
        if frame is not None:
            # Process captured frame
            # Implementation needed
            pass
            
    def go_back(self, instance):
        """Return to previous screen"""
        app = App.get_running_app()
        app.go_back()
        
    def show_error(self, message):
        """Show error message"""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
        
    def on_word_selected(self, word: str):
        """Handle word selection"""
        details = self.text_processor.get_word_details(word)
        popup = WordDetailsPopup(word, details)
        popup.open()