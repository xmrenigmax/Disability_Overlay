# src/camera/manager.py
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.utils import platform
from kivy.logger import Logger
import cv2
import numpy as np
import time
from typing import Optional, Tuple, List, Any

class CameraManager:
    """
    Handles camera initialization, frame capture, and device management
    across different platforms.
    
    Features:
    - Multi-platform camera support
    - Auto-recovery from errors
    - Frame processing
    - Multiple camera switching
    """
    
    def __init__(self):
        # Camera state
        self.capture = None
        self.current_api = None
        self.current_index = 0
        self.is_active = False
        
        # Recovery settings
        self.retry_count = 0
        self.max_retries = 3
        
        # Available APIs by platform
        self.apis = self._get_platform_apis()
        
    def _get_platform_apis(self) -> List[Tuple[Any, str]]:
        """Get platform-specific camera APIs"""
        if platform == 'win':
            return [
                (cv2.CAP_DSHOW, "DirectShow"),
                (cv2.CAP_MSMF, "Media Foundation"),
                (0, "Default")
            ]
        else:
            return [(0, "Default")]  # Mobile platforms use default

    def initialize(self, camera_index: int = 0) -> bool:
        """
        Initialize camera with platform-specific settings
        
        Args:
            camera_index: Index of camera to initialize
        """
        try:
            self.current_index = camera_index
            
            for api, name in self.apis:
                try:
                    if isinstance(api, int):
                        self.capture = cv2.VideoCapture(camera_index + api)
                    else:
                        self.capture = cv2.VideoCapture(camera_index)
                        
                    if self.capture.isOpened():
                        ret, frame = self.capture.read()
                        if ret and frame is not None:
                            self.current_api = api
                            self.is_active = True
                            Logger.info(f'Camera initialized with {name}')
                            return True
                            
                        self.capture.release()
                        
                except Exception as e:
                    Logger.warning(f'Failed with {name}: {str(e)}')
                    if self.capture:
                        self.capture.release()
                    continue
                    
            Logger.error('Failed to initialize camera with any API')
            return False
            
        except Exception as e:
            Logger.error(f'Camera initialization failed: {str(e)}')
            return False

    def get_frame(self) -> Optional[np.ndarray]:
        """Get frame with error recovery"""
        if not self.is_active or not self.capture or not self.capture.isOpened():
            return None
            
        try:
            ret, frame = self.capture.read()
            if ret and frame is not None:
                self.retry_count = 0
                return frame
                
            # Handle frame capture failure
            self.retry_count += 1
            if self.retry_count <= self.max_retries:
                Logger.warning(f'Frame capture failed, attempt {self.retry_count}/{self.max_retries}')
                time.sleep(0.1)
                return None
                
            # Reset camera after max retries
            Logger.error('Frame capture failed, resetting camera')
            self.release()
            self.initialize(self.current_index)
            return None
            
        except Exception as e:
            Logger.error(f'Frame capture error: {str(e)}')
            return None

    def switch_camera(self) -> bool:
        """Switch to next available camera"""
        try:
            next_index = (self.current_index + 1) % 2
            
            # Test next camera
            test_cap = cv2.VideoCapture(next_index)
            if test_cap.isOpened():
                test_cap.release()
                self.release()
                return self.initialize(next_index)
                
            Logger.info('No additional cameras found')
            return False
            
        except Exception as e:
            Logger.error(f'Camera switch failed: {str(e)}')
            return False

    def release(self) -> None:
        """Clean up camera resources"""
        try:
            if self.capture:
                self.capture.release()
                self.capture = None
            self.is_active = False
            Logger.info('Camera released')
        except Exception as e:
            Logger.error(f'Camera release failed: {str(e)}')

    def get_frame_size(self) -> Tuple[int, int]:
        """Get current frame dimensions"""
        if self.capture:
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)
        return (0, 0)

    def is_initialized(self) -> bool:
        """Check if camera is properly initialized"""
        return self.is_active and self.capture is not None