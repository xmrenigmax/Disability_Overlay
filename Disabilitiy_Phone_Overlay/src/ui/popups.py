# src/ui/popups.py
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

class WordDetailsPopup(Popup):
    """Popup for displaying word definitions and synonyms"""
    
    def __init__(self, word: str, details: dict, **kwargs):
        super().__init__(**kwargs)
        self.title = f'Details for "{word}"'
        self.size_hint = (0.8, 0.8)
        
        # Create content layout
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Add definitions section
        if details['definitions']:
            content.add_widget(Label(
                text='Definitions:',
                size_hint_y=None,
                height=dp(30),
                bold=True
            ))
            
            for definition in details['definitions']:
                content.add_widget(Label(
                    text=f"• {definition}",
                    text_size=(self.width * 0.9, None),
                    size_hint_y=None,
                    halign='left'
                ))
        
        # Add synonyms section
        if details['synonyms']:
            content.add_widget(Label(
                text='Synonyms:',
                size_hint_y=None,
                height=dp(30),
                bold=True
            ))
            
            synonyms_text = ", ".join(details['synonyms'])
            content.add_widget(Label(
                text=synonyms_text,
                text_size=(self.width * 0.9, None),
                size_hint_y=None,
                halign='left'
            ))
        
        # Add examples section
        if details['examples']:
            content.add_widget(Label(
                text='Examples:',
                size_hint_y=None,
                height=dp(30),
                bold=True
            ))
            
            for example in details['examples']:
                content.add_widget(Label(
                    text=f"• {example}",
                    text_size=(self.width * 0.9, None),
                    size_hint_y=None,
                    halign='left'
                ))
        
        # Add close button
        close_button = Button(
            text='Close',
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5}
        )
        close_button.bind(on_release=self.dismiss)
        content.add_widget(close_button)
        
        # Add scrollview
        scroll = ScrollView()
        scroll.add_widget(content)
        self.content = scroll