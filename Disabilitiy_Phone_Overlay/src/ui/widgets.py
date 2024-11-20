# src/ui/widgets.py
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

class SelectableWord(ButtonBehavior, Label):
    """Interactive word label with selection handling"""
    
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.background_color = (0, 0, 0, 0)
        self.bind(size=self._update_background, pos=self._update_background)

    def _update_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)

    def on_press(self):
        self.background_color = (0.2, 0.6, 1, 0.3)
        self._update_background()

    def on_release(self):
        self.background_color = (0, 0, 0, 0)
        self._update_background()