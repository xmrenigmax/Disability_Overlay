from kivy.utils import platform
from kivy.core.window import Window

def request_permissions(callback):
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission
        except ImportError:
            # Handle the case where the android.permissions module is not available
            callback(False)
            return
        
        permissions = [Permission.CAMERA, Permission.RECORD_AUDIO]
        
        def on_permissions_result(permissions, grants):
            if all(grants):
                callback(True)
            else:
                callback(False)
        
        request_permissions(permissions, on_permissions_result)
    elif platform == 'win':
        try:
            import ctypes
            user32 = ctypes.windll.user32
            if user32.MessageBoxW(0, "Allow access to camera and microphone?", "Permissions", 1) == 1:
                callback(True)
            else:
                callback(False)
        except ImportError:
            # Handle the case where ctypes is not available
            callback(False)
    elif platform == 'ios':
        try:
            from pyobjus import autoclass
            AVAuthorizationStatusAuthorized = 3
            AVAuthorizationStatus = autoclass('AVCaptureDevice').authorizationStatusForMediaType_('vide')
            if AVAuthorizationStatus == AVAuthorizationStatusAuthorized:
                callback(True)
            else:
                callback(False)
        except ImportError:
            # Handle the case where pyobjus is not available
            callback(False)
    else:
        # If not on Android, Windows, or iOS, assume permissions are granted
        callback(True)

def on_permissions_granted(granted):
    if granted:
        # Ensure fullscreen is restored
        Window.fullscreen = True
        Window.maximize()
        # Rest of your permission handling code...
