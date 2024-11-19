# text_processor.py
from PIL import Image
import pytesseract
from googletrans import Translator
from nltk.corpus import wordnet
import cv2
import numpy as np

class TextProcessor:
    def __init__(self):
        self.translator = Translator()
        self.saved_preferences = {}
        
    def detect_text(self, frame):
        # Convert frame to PIL Image
        image = Image.fromarray(frame)
        # Extract text
        text = pytesseract.image_to_string(image)
        return text
    
    def get_synonyms(self, word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        return list(set(synonyms))
    
    def translate_text(self, text, target_lang='en'):
        try:
            translation = self.translator.translate(text, dest=target_lang)
            return translation.text
        except:
            return text