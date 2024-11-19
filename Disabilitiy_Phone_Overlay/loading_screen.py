from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        
        # Create a vertical BoxLayout to hold the label and progress bar
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Create a label to display "Loading..."
        self.label = Label(text="Loading...", font_size='20sp', size_hint=(1, 0.5))
        
        # Create a progress bar with a maximum value of 1000
        self.progress_bar = ProgressBar(max=1000, size_hint=(1, 0.5))
        
        # Add the label and progress bar to the layout
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.progress_bar)
        
        # Add the layout to the screen
        self.add_widget(self.layout)
        
        # Schedule the update of the progress bar
        Clock.schedule_interval(self.update_progress_bar, 0.1)
        
    def update_progress_bar(self, dt):
        # Update the value of the progress bar
        if self.progress_bar.value < self.progress_bar.max:
            self.progress_bar.value += 50  # Increase the increment value to make it faster
        else:
            # Switch to the main screen when loading is complete
            self.manager.current = 'main'
            Clock.unschedule(self.update_progress_bar)