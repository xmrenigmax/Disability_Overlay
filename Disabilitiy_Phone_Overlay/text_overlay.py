# text_overlay.py
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.properties import StringProperty

class DraggableText(DragBehavior, Label):
    text_style = StringProperty('normal')
    
    def __init__(self, **kwargs):
        super(DraggableText, self).__init__(**kwargs)
        self.size_hint = (None, None)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Show text modification options
            self.show_text_options()
        return super().on_touch_down(touch)
    
    def show_text_options(self):
        # Create popup with font/style options
        pass