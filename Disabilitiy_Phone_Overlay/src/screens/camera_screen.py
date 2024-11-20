# src/screens/camera_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.logger import Logger

from ..camera.manager import CameraManager
from ..camera.filters import ColorFilters
from ..core.config import AppConfig

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
        self.create_ui()
        self.add_widget(self.layout)
        
        # Bind events
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
            self.status_label.opacity = 0
        else:
            self.status_label.text = "Camera initialization failed"
            self.status_label.opacity = 1
            
    def _stop_camera(self, *args):
        """Stop and release camera"""
        Clock.unschedule(self.update_frame)
        self.camera_manager.release()
        
    def update_frame(self, dt):
        """Update camera frame with filters"""
        frame = self.camera_manager.get_frame()
        if frame is not None:
            # Apply active filter if any
            if self.color_filters.current_filter:
                frame = self.color_filters.apply_filter(
                    frame,
                    self.color_filters.current_filter
                )
            
            # Update preview
            self.preview.canvas.clear()
            with self.preview.canvas:
                # Convert frame to texture and display
                pass  # Implementation needed
                
    def switch_camera(self, instance):
        """Switch between available cameras"""
        if self.camera_manager.switch_camera():
            self.status_label.text = "Camera switched"
            self.status_label.opacity = 1
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'opacity', 0), 2)
        else:
            self.status_label.text = "No other cameras available"
            self.status_label.opacity = 1
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'opacity', 0), 2)
            
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