# loading_screen.py
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.progress = ProgressBar(max=100)
        self.status_label = Label(text="Initializing...")
        
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.progress)
        self.add_widget(self.layout)
        
        # Start initialization process
        Clock.schedule_once(self.start_loading, 0)
        
    def start_loading(self, dt):
        """Start the loading process"""
        self.progress.value = 0
        Clock.schedule_interval(self.update_progress, 0.1)
        # Initialize camera with proper dt parameter
        Clock.schedule_once(self.initialize_camera, 0)
        
    def initialize_camera(self, dt):
        """Initialize the camera screen"""
        app = App.get_running_app()
        camera_screen = app.screen_manager.get_screen('full_screen_camera')
        if camera_screen:
            Clock.schedule_once(camera_screen.initialize_camera, 0)
        
    def update_progress(self, dt):
        """Update progress bar and switch screens when done"""
        self.progress.value += 5
        if self.progress.value >= 100:
            app = App.get_running_app()
            app.screen_manager.current = 'main'
            return False  # Stop the interval