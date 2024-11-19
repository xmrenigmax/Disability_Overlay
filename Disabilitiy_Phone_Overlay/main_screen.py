from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from permissions import Permissions
from kivy.core.window import Window

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Create the main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Create the UI elements
        self.create_ui()
        
        # Add the main layout to the screen
        self.add_widget(self.main_layout)
    
    def create_ui(self):
        # Create an AnchorLayout to position buttons
        self.anchor_layout = AnchorLayout(anchor_x='right', anchor_y='top')
        
        # Create a vertical BoxLayout for the buttons
        self.buttons_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=('150dp', '300dp'), spacing=10)
        
        # Create the "Select Scanner" button and add it to the buttons layout
        self.create_scanner_button()
        
        # Create the options button and add it to the buttons layout
        self.options_button = Button(text='Options', size_hint=(None, None), size=('150dp', '48dp'))
        self.buttons_layout.add_widget(self.options_button)
        
        # Create the quit button and add it to the buttons layout
        self.quit_button = Button(text='Quit', size_hint=(None, None), size=('150dp', '48dp'))
        self.quit_button.bind(on_release=self.quit_program)
        self.buttons_layout.add_widget(self.quit_button)
        
        # Add the buttons layout to the anchor layout
        self.anchor_layout.add_widget(self.buttons_layout)
        
        # Add the anchor layout to the main layout
        self.main_layout.add_widget(self.anchor_layout)
    
    def create_scanner_button(self):
        # Create a main button to trigger the overlay
        self.main_button = Button(text='Select Scanner', size_hint=(None, None), size=('150dp', '48dp'))
        self.main_button.bind(on_release=self.show_scanner_overlay)
        
        # Add the main button to the buttons layout
        self.buttons_layout.add_widget(self.main_button)
    
    def show_scanner_overlay(self, instance):
        # Create the overlay layout
        overlay_layout = FloatLayout()
        
        # Create a vertical BoxLayout for the scanner options
        scanner_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=('200dp', '300dp'), pos_hint={'x': 0, 'center_y': 0.5}, spacing=10)
        
        # Add scanner options to the layout
        for option in ["Camera Assistance", "Image Assistance", "Saved History"]:
            btn = Button(text=option, size_hint_y=None, height=44)
            if option == "Camera Assistance":
                btn.bind(on_release=lambda x: self.handle_camera_assistance(popup))
            scanner_layout.add_widget(btn)
        
        # Add a close button to the overlay
        close_button = Button(text='Close', size_hint=(None, None), size=('100dp', '48dp'), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_release=lambda x: self.close_scanner_overlay(popup))
        
        # Add the scanner layout and close button to the overlay layout
        overlay_layout.add_widget(scanner_layout)
        overlay_layout.add_widget(close_button)
        
        # Create a popup to display the overlay
        popup = Popup(title='Scanner Overlay', content=overlay_layout, size_hint=(0.8, 0.8))
        popup.open()

    def close_scanner_overlay(self, popup):
        # Close the popup
        popup.dismiss()

    def handle_camera_assistance(self, popup):
        # Close the current popup
        self.close_scanner_overlay(popup)
        
        # Check if permissions are already granted
        permission_status = Permissions.load_permission_status()
        if permission_status is True:
            # Open the full-screen camera
            self.open_full_screen_camera()
        else:
            # Open the camera overlay to request permissions
            from camera_overlay import CameraOverlay
            camera_overlay = CameraOverlay()
            camera_overlay.open()

    def open_full_screen_camera(self):
        # Open the full-screen camera
        app = App.get_running_app()
        app.root.current = 'full_screen_camera'
    
    def return_to_main_menu(self):
        # Return to the main menu
        app = App.get_running_app()
        app.root.current = 'main_screen'
    
    def quit_program(self, instance):
        # Stop the Kivy application and close the window
        App.get_running_app().stop()
        Window.close()