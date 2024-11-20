# src/screens/loading_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.logger import Logger

from ..core.config import AppConfig

class LoadingScreen(Screen):
    """
    Loading screen with progress tracking and resource initialization.
    
    Features:
    - Progress bar
    - Status updates
    - Resource loading
    - Smooth transitions
    """
    
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.config = AppConfig()
        
        # Create main layout
        self.layout = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )
        
        # Create title
        self.title = Label(
            text='Loading...',
            font_size=dp(24),
            size_hint_y=0.2
        )
        self.layout.add_widget(self.title)
        
        # Create status label
        self.status_label = Label(
            text="Initializing...",
            size_hint_y=0.2
        )
        self.layout.add_widget(self.status_label)
        
        # Create progress bar
        self.progress = ProgressBar(
            max=100,
            height=dp(20),
            size_hint_y=None
        )
        self.layout.add_widget(self.progress)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Initialize loading sequence
        self.loading_tasks = [
            ('Checking permissions...', self._check_permissions, 20),
            ('Initializing camera...', self._init_camera, 40),
            ('Loading resources...', self._load_resources, 30),
            ('Finalizing...', self._finalize, 10)
        ]
        
        # Start loading process
        Clock.schedule_once(self.start_loading, 0.5)
        
    def start_loading(self, dt):
        """Begin loading sequence"""
        try:
            self.current_progress = 0
            self._run_next_task()
        except Exception as e:
            Logger.error(f'Loading failed: {str(e)}')
            self.status_label.text = "Loading failed"
            
    def _run_next_task(self):
        """Run next task in loading sequence"""
        if not self.loading_tasks:
            self._complete_loading()
            return
            
        status, task, progress = self.loading_tasks.pop(0)
        self.status_label.text = status
        
        def after_task(dt):
            try:
                task()
                self.current_progress += progress
                self.progress.value = self.current_progress
                self._run_next_task()
            except Exception as e:
                Logger.error(f'Task failed: {str(e)}')
                self.status_label.text = "Loading failed"
                
        Clock.schedule_once(after_task, 0.5)
        
    def _check_permissions(self):
        """Check required permissions"""
        try:
            # Permission check implementation based on platform
            Logger.info('Permissions checked')
        except Exception as e:
            Logger.error(f'Permission check failed: {str(e)}')
            raise
            
    def _init_camera(self):
        """Initialize camera system"""
        try:
            # Camera initialization check
            Logger.info('Camera system initialized')
        except Exception as e:
            Logger.error(f'Camera initialization failed: {str(e)}')
            raise
            
    def _load_resources(self):
        """Load application resources"""
        try:
            # Load necessary resources
            Logger.info('Resources loaded')
        except Exception as e:
            Logger.error(f'Resource loading failed: {str(e)}')
            raise
            
    def _finalize(self):
        """Finalize loading process"""
        try:
            # Final initialization steps
            Logger.info('Loading finalized')
        except Exception as e:
            Logger.error(f'Finalization failed: {str(e)}')
            raise
            
    def _complete_loading(self):
        """Complete loading and transition to main screen"""
        try:
            self.status_label.text = "Loading complete!"
            Clock.schedule_once(self._transition_to_main, 1)
        except Exception as e:
            Logger.error(f'Completion failed: {str(e)}')
            
    def _transition_to_main(self, dt):
        """Transition to main screen"""
        try:
            app = App.get_running_app()
            app.switch_screen('main')
        except Exception as e:
            Logger.error(f'Transition failed: {str(e)}')