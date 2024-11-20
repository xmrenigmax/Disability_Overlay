# src/features/text_processor.py
import cv2
import numpy as np
import pytesseract
from typing import List, Dict, Tuple, Optional
from ..utils.logger import app_logger as logger
from ..core.config import AppConfig
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from ..ui.popups import WordDetailsPopup
from kivy.core.clipboard import Clipboard
import re

class TextProcessor:
    """
    Handles text detection, extraction and processing from camera frames.
    Provides real-time text detection and selection capabilities.
    """
    
    def __init__(self):
        self.config = AppConfig()
        # Configure pytesseract path for Windows
        if self.config.platform == 'win':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        self.selected_text = None
        self.detected_regions = []
        
        # Initialize NLTK first time
        try:
            import nltk
            nltk.download('wordnet')
            nltk.download('punkt')
        except Exception as e:
            logger.error(f"NLTK initialization failed: {str(e)}")
    
    def detect_text(self, frame: np.ndarray) -> List[Dict[str, any]]:
        """
        Detect text regions in frame
        Returns list of detected text regions with coordinates
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Get OCR data including bounding boxes
            ocr_data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
            
            # Process detected regions
            regions = []
            for i in range(len(ocr_data['text'])):
                if int(ocr_data['conf'][i]) > 60:  # Confidence threshold
                    text = ocr_data['text'][i].strip()
                    if text:
                        region = {
                            'text': text,
                            'confidence': int(ocr_data['conf'][i]),
                            'bbox': (
                                ocr_data['left'][i],
                                ocr_data['top'][i],
                                ocr_data['width'][i],
                                ocr_data['height'][i]
                            )
                        }
                        regions.append(region)
            
            self.detected_regions = regions
            return regions
            
        except Exception as e:
            logger.error(f"Text detection failed: {str(e)}")
            return []
    
    def select_text(self, touch_pos: Tuple[int, int]) -> Optional[str]:
        """Select text at touched position"""
        try:
            x, y = touch_pos
            for region in self.detected_regions:
                left, top, width, height = region['bbox']
                if (left <= x <= left + width and 
                    top <= y <= top + height):
                    self.selected_text = region['text']
                    return region['text']
            return None
            
        except Exception as e:
            logger.error(f"Text selection failed: {str(e)}")
            return None
    
    def enhance_text(self, text: str) -> str:
        """Apply text enhancements"""
        try:
            # Remove noise
            text = text.strip()
            
            # Fix common OCR errors
            replacements = {
                '|': 'I',
                '0': 'O',
                '1': 'l',
                '@': 'a'
            }
            
            for old, new in replacements.items():
                text = text.replace(old, new)
                
            return text
            
        except Exception as e:
            logger.error(f"Text enhancement failed: {str(e)}")
            return text
    
    def get_text_regions(self) -> List[Dict[str, any]]:
        """Get currently detected text regions"""
        return self.detected_regions
    
    def clear_selection(self) -> None:
        """Clear current text selection"""
        self.selected_text = None

    def get_word_details(self, word: str) -> Dict[str, List[str]]:
        """Get word definitions and synonyms"""
        try:
            details = {
                'definitions': [],
                'synonyms': set(),
                'examples': []
            }
            
            # Get synsets for word
            synsets = wordnet.synsets(word)
            
            for synset in synsets:
                # Add definition
                details['definitions'].append(synset.definition())
                
                # Add examples
                details['examples'].extend(synset.examples())
                
                # Add synonyms
                for lemma in synset.lemmas():
                    if lemma.name() != word:
                        details['synonyms'].add(lemma.name())
            
            # Convert to list and sort
            details['synonyms'] = sorted(list(details['synonyms']))
            
            return details
            
        except Exception as e:
            logger.error(f"Word lookup failed: {str(e)}")
            return {'definitions': [], 'synonyms': [], 'examples': []}

    def process_text(self, text: str) -> List[str]:
        """Split text into processable words"""
        # Remove special characters and split
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to system clipboard"""
        Clipboard.copy(text)

    def get_selected_word_context(self, text: str, word: str, 
                                context_words: int = 3) -> str:
        """Get surrounding context for selected word"""
        words = text.split()
        try:
            word_index = words.index(word)
            start = max(0, word_index - context_words)
            end = min(len(words), word_index + context_words + 1)
            return ' '.join(words[start:end])
        except ValueError:
            return word

# Global text processor instance
text_processor = TextProcessor()