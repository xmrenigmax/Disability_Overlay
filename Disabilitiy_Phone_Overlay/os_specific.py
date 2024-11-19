import platform

class OSSpecificLogic:
    def __init__(self):
        self.os_name = platform.system()
        self.is_windows = self.os_name == 'Windows'

    def perform_os_specific_task(self):
        if self.os_name == 'Android':
            self.android_task()
        elif self.os_name == 'iOS':
            self.ios_task()
        elif self.os_name == 'Windows':
            self.windows_task()
        else:
            print("Unsupported OS")

    def android_task(self):
        print("Performing Android-specific task")
        # Add Android-specific logic here

    def ios_task(self):
        print("Performing iOS-specific task")
        # Add iOS-specific logic here

    def windows_task(self):
        print("Performing Windows-specific task")
        # Add Windows-specific logic here