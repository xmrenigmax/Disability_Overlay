# src/screens/main_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App
from kivy.logger import Logger

from ..core.config import AppConfig
from ..ui.popups import TextToolsPopup

class MainScreen(Screen):
    """
    Main application screen with feature buttons and navigation.
    """
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.config = AppConfig()
        
        # Create main layout
        self.main_layout = BoxLayout(
            orientation='vertical',
            padding=self.config.get_ui_metrics()['padding'],
            spacing=self.config.get_ui_metrics()['spacing']
        )
        
        # Add title
        self.add_title()
        
        # Add feature buttons grid
        self.create_feature_grid()
        
        # Add main layout to screen
        self.add_widget(self.main_layout)

    def add_title(self):
        """Add title label to layout"""
        title = Label(
            text='Accessibility Scanner',
            size_hint_y=0.1,
            font_size=dp(24),
            color=self.config.COLORS['text']
        )
        self.main_layout.add_widget(title)

    def create_feature_grid(self):
        """Create grid of feature buttons"""
        grid = GridLayout(
            cols=2,
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=0.8
        )
        
        # Define feature buttons
        features = [
            {
                'text': 'Scanner',
                'color': self.config.COLORS['primary'],
                'callback': self.show_scanner_options
            },
            {
                'text': 'Text Tools',
                'color': self.config.COLORS['secondary'],
                'callback': self.show_text_tools
            },
            {
                'text': 'Settings',
                'color': (0.3, 0.3, 0.3, 1),
                'callback': self.show_settings
            }
        ]
        
        # Create and add buttons
        for feature in features:
            button = Button(
                text=feature['text'],
                background_normal='',
                background_color=feature['color'],
                size_hint_y=None,
                height=self.config.get_ui_metrics()['button_height']
            )
            button.bind(on_release=feature['callback'])
            grid.add_widget(button)
            
        self.main_layout.add_widget(grid)

    def show_scanner_options(self, instance):
        """Show scanner type selection popup"""
        try:
            content = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                padding=dp(20)
            )
            
            # Scanner options
            options = [
                ('Camera Scanner', self.open_camera_scanner),
                ('File Scanner', self.open_file_scanner),
                ('Quick Scanner', self.open_quick_scanner)
            ]
            
            for text, callback in options:
                btn = Button(
                    text=text,
                    size_hint_y=None,
                    height=dp(50)
                )
                btn.bind(on_release=lambda x, cb=callback: self.handle_scanner_selection(cb))
                content.add_widget(btn)
            
            # Create popup
            self._current_popup = Popup(
                title='Select Scanner Type',
                content=content,
                size_hint=(0.8, 0.6),
                auto_dismiss=True
            )
            self._current_popup.open()
            
        except Exception as e:
            Logger.error(f'Scanner options failed: {str(e)}')

    def show_text_tools(self, instance):
        """Show text tools popup"""
        try:
            popup = TextToolsPopup()
            popup.open()
        except Exception as e:
            Logger.error(f'Text tools failed: {str(e)}')

    def show_settings(self, instance):
        """Show settings screen"""
        try:
            app = App.get_running_app()
            app.switch_screen('settings')
        except Exception as e:
            Logger.error(f'Settings navigation failed: {str(e)}')

    def handle_scanner_selection(self, callback):
        """Handle scanner selection with permission check"""
        from ..utils.permissions import request_permissions
        
        def permission_callback(granted):
            if granted:
                if self._current_popup:
                    self._current_popup.dismiss()
                callback()
            else:
                self.show_permission_denied()
                
        request_permissions(permission_callback)

    def show_permission_denied(self):
        """Show permission denied message"""
        popup = Popup(
            title='Permission Denied',
            content=Label(text='Camera permission is required\nfor scanner functionality'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def open_camera_scanner(self):
        """Open camera scanner screen"""
        app = App.get_running_app()
        app.switch_screen('camera')

    def open_file_scanner(self):
        """Open file scanner"""
        # Implementation needed
        pass

    def open_quick_scanner(self):
        """Open quick scanner mode"""
        # Implementation needed
        pass