# src/utils/permissions.py
from kivy.utils import platform
from kivy.logger import Logger
from typing import Callable, Optional

class PermissionManager:
    """
    Handles platform-specific permission requests and management.
    
    Features:
    - Platform detection
    - Permission status tracking
    - Permission request handling
    - Callback management
    """
    
    def __init__(self):
        self.permissions_granted = False
        self._permission_callback: Optional[Callable] = None
    
    def request_permissions(self, callback: Callable[[bool], None]) -> None:
        """
        Request required permissions based on platform
        
        Args:
            callback: Function to call with permission result
        """
        try:
            self._permission_callback = callback
            
            if platform == 'android':
                self._request_android_permissions()
            elif platform == 'ios':
                self._check_ios_permissions()
            else:
                # Windows/Desktop platforms
                self._handle_desktop_permissions()
                
        except Exception as e:
            Logger.error(f'Permission request failed: {str(e)}')
            if callback:
                callback(False)
                
    def _request_android_permissions(self) -> None:
        """Handle Android permission requests"""
        try:
            from android.permissions import request_permissions, Permission #type: ignore
            
            def permission_callback(permissions: list, grants: list) -> None:
                # All permissions must be granted
                granted = all(grants)
                self.permissions_granted = granted
                
                if self._permission_callback:
                    self._permission_callback(granted)
                    
            # Request required permissions
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ], permission_callback)
            
        except Exception as e:
            Logger.error(f'Android permission request failed: {str(e)}')
            if self._permission_callback:
                self._permission_callback(False)
                
    def _check_ios_permissions(self) -> None:
        """Handle iOS permission checks"""
        try:
            # iOS permissions are handled through Info.plist
            # We just verify camera availability here
            from pyobjus import autoclass # type: ignore
            
            AVCaptureDevice = autoclass('AVCaptureDevice')
            auth_status = AVCaptureDevice.authorizationStatusForMediaType_('vide')
            
            granted = (auth_status == 3)  # 3 = Authorized
            self.permissions_granted = granted
            
            if self._permission_callback:
                self._permission_callback(granted)
                
        except Exception as e:
            Logger.error(f'iOS permission check failed: {str(e)}')
            if self._permission_callback:
                self._permission_callback(False)
                
    def _handle_desktop_permissions(self) -> None:
        """Handle desktop platform permissions"""
        try:
            # Check camera access on Windows
            import cv2
            camera = cv2.VideoCapture(0)
            
            if camera.isOpened():
                granted = True
                camera.release()
            else:
                granted = False
                
            self.permissions_granted = granted
            
            if self._permission_callback:
                self._permission_callback(granted)
                
        except Exception as e:
            Logger.error(f'Desktop permission check failed: {str(e)}')
            if self._permission_callback:
                self._permission_callback(False)

# Global permission manager instance
_permission_manager = PermissionManager()

def request_permissions(callback: Callable[[bool], None]) -> None:
    """
    Request application permissions
    
    Args:
        callback: Function to call with permission result
    """
    _permission_manager.request_permissions(callback)