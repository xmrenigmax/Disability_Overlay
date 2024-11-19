from kivy.utils import platform
from kivy.core.window import Window

def request_permissions(callback):
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission # type: ignore
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
            import win32gui
            import win32con
             # Get current window handle
            hwnd = win32gui.GetForegroundWindow()
            
            # Set window always on top
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            
            # Show permission dialog
            result = ctypes.windll.user32.MessageBoxW(
                hwnd,
                "Allow access to camera and microphone?",
                "Permissions",
                1 | win32con.MB_TOPMOST  # Make dialog topmost
            )
            
            # Reset window state
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            
            callback(result == 1)
            
        except ImportError:
        # If not on Android, Windows, or iOS, assume permissions are granted
            callback(True)

def on_permissions_granted(granted):
    if granted:
        # Ensure fullscreen is restored
        Window.fullscreen = True
        Window.maximize()
        # Rest of your permission handling code...
