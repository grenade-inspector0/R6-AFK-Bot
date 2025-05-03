import ctypes

USER32 = ctypes.windll.user32
SIEGE_WINDOW_NAMES = ["Rainbow Six"]

class ActiveManager:
    def __init__(self):
        self.__user_active = False

    @staticmethod
    def __window_in_focus():
        hwnd = USER32.GetForegroundWindow()
        length = USER32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        USER32.GetWindowTextW(hwnd, buf, length + 1)

        window = buf.value if buf.value else None
        in_focus = window in SIEGE_WINDOW_NAMES
        return in_focus

    def user_active(self):
        return self.__user_active

    def is_active(self):
        if not self.__user_active:
            return False

        return ActiveManager.__window_in_focus()

    def switch_active(self):
        self.__user_active = not self.__user_active