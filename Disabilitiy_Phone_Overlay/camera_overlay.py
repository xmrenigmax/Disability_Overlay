from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from permissions import Permissions
from kivy.app import App

class CameraOverlay:
    def open(self):
        # Create the overlay layout
        overlay_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Add a label to ask for device permissions
        permission_label = Label(text='Please grant camera permissions to proceed.')
        overlay_layout.add_widget(permission_label)
        
        # Create a horizontal BoxLayout for the buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='48dp', spacing=10)
        
        # Add a button to request permissions
        grant_button = Button(text='Grant', size_hint=(0.5, 1))
        grant_button.bind(on_release=self.request_permissions)
        button_layout.add_widget(grant_button)
        
        # Add a button to deny permissions
        deny_button = Button(text='Deny', size_hint=(0.5, 1))
        deny_button.bind(on_release=self.deny_permissions)
        button_layout.add_widget(deny_button)
        
        # Add the button layout to the overlay layout
        overlay_layout.add_widget(button_layout)
        
        # Create a popup to display the overlay
        self.popup = Popup(title='Camera Assistance', content=overlay_layout, size_hint=(0.5, 0.5))
        self.popup.open()
    
    def request_permissions(self, instance):
        # Check and request camera permissions
        if Permissions.request_camera_permission():
            # Save permission status to cache
            Permissions.save_permission_status(True)
            
            # Close the current popup
            self.popup.dismiss()
            
            # Open the full-screen camera
            app = App.get_running_app()
            app.root.current = 'full_screen_camera'
    
    def deny_permissions(self, instance):
        # Save permission status to cache
        Permissions.save_permission_status(False)
        
        # Close the popup if permissions are denied
        self.popup.dismiss()
        
        # Return to the main menu
        app = App.get_running_app()
        app.root.current = 'main_screen'