# src/features/translation.py
from googletrans import Translator, LANGUAGES
from typing import Dict, Optional, List
from ..utils.logger import app_logger as logger
from ..core.config import AppConfig

class TranslationManager:
    """
    Handles text translation and language detection.
    Supports multiple languages and translation caching.
    """
    
    def __init__(self):
        self.config = AppConfig()
        self.translator = Translator()
        self.cached_translations: Dict[str, Dict[str, str]] = {}
        self.preferred_language = 'en'
        
        # Common languages for quick access
        self.common_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'zh-cn': 'Chinese (Simplified)',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic'
        }
    
    def translate_text(self, text: str, target_lang: str) -> Optional[str]:
        """Translate text to target language"""
        try:
            # Check cache first
            cache_key = f"{text}:{target_lang}"
            if cache_key in self.cached_translations:
                return self.cached_translations[cache_key]
            
            # Perform translation
            translation = self.translator.translate(text, dest=target_lang)
            
            # Cache result
            self.cached_translations[cache_key] = translation.text
            
            return translation.text
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return None
    
    def detect_language(self, text: str) -> Optional[str]:
        """Detect text language"""
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return None
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available translation languages"""
        return self.common_languages
    
    def get_all_languages(self) -> Dict[str, str]:
        """Get all supported languages"""
        return LANGUAGES
    
    def set_preferred_language(self, lang_code: str) -> bool:
        """Set preferred translation language"""
        try:
            if lang_code in LANGUAGES:
                self.preferred_language = lang_code
                logger.info(f"Set preferred language: {lang_code}")
                return True
            return False
        except Exception as e:
            logger.error(f"Setting preferred language failed: {str(e)}")
            return False
    
    def translate_to_preferred(self, text: str) -> Optional[str]:
        """Translate text to preferred language"""
        return self.translate_text(text, self.preferred_language)
    
    def clear_cache(self) -> None:
        """Clear translation cache"""
        self.cached_translations.clear()
        logger.info("Translation cache cleared")

# Global translation manager instance
translation_manager = TranslationManager()