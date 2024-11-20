# src/features/text_processor.py
import cv2
import numpy as np
import pytesseract
from typing import List, Dict, Tuple, Optional
from ..utils.logger import app_logger as logger
from ..core.config import AppConfig

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

# Global text processor instance
text_processor = TextProcessor()