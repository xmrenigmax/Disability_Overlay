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

class TextToolsPopup(Popup):
    """Popup menu for text enhancement tools"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Text Tools'
        self.size_hint = (0.8, 0.9)
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(10))
        
        # Tools list
        tools = [
            {
                'text': 'Word Definitions',
                'description': 'Look up word meanings and usage',
                'icon': 'book',
                'color': (0.2, 0.6, 1, 1),
                'callback': self.show_definitions
            },
            {
                'text': 'Synonyms Finder',
                'description': 'Find alternative words and meanings',
                'icon': 'text',
                'color': (0.3, 0.8, 0.4, 1),
                'callback': self.show_synonyms
            },
            {
                'text': 'Dyslexia Mode',
                'description': 'Enable dyslexia-friendly text display',
                'icon': 'eye',
                'color': (0.9, 0.5, 0.2, 1),
                'callback': self.toggle_dyslexia_mode
            },
            {
                'text': 'Font Settings',
                'description': 'Adjust text size and style',
                'icon': 'format',
                'color': (0.6, 0.4, 0.8, 1),
                'callback': self.show_font_settings
            }
        ]
        
        # Create tool buttons
        for tool in tools:
            # Tool container
            container = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                padding=dp(10)
            )
            
            # Tool info
            info_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=0.7
            )
            
            # Title
            title = Label(
                text=tool['text'],
                font_size=dp(16),
                bold=True,
                halign='left',
                size_hint_y=0.6
            )
            info_layout.add_widget(title)
            
            # Description
            desc = Label(
                text=tool['description'],
                font_size=dp(12),
                color=(0.7, 0.7, 0.7, 1),
                halign='left',
                size_hint_y=0.4
            )
            info_layout.add_widget(desc)
            
            container.add_widget(info_layout)
            
            # Button
            btn = Button(
                text='Open',
                size_hint=(0.3, 0.8),
                background_normal='',
                background_color=tool['color'],
                pos_hint={'center_y': 0.5}
            )
            btn.bind(on_release=tool['callback'])
            container.add_widget(btn)
            
            layout.add_widget(container)
        
        # Close button
        close_btn = Button(
            text='Close',
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5}
        )
        close_btn.bind(on_release=self.dismiss)
        layout.add_widget(close_btn)
        
        self.content = layout
    
    def show_definitions(self, instance):
        """Open word definitions tool"""
        self.dismiss()
        # Implementation needed
        
    def show_synonyms(self, instance):
        """Open synonyms finder"""
        self.dismiss()
        # Implementation needed
        
    def toggle_dyslexia_mode(self, instance):
        """Toggle dyslexia-friendly mode"""
        self.dismiss()
        # Implementation needed
        
    def show_font_settings(self, instance):
        """Show font adjustment settings"""
        self.dismiss()
        # Implementation needed