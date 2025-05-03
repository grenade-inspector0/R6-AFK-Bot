import time
import ctypes
import random
import keyboard
import pydirectinput
from src.active import ActiveManager
from src.randomness import get_random_time
from src.screen import get_res_scale_x, get_res_scale_y

win32 = ctypes.windll.user32
pydirectinput.FAILSAFE = False

class MouseAndKeyboard:
    """Control Mouse And Keyboard"""
    def __init__(self) -> None:
        self.__actions = []
        self.__running = False

    def __run(self, active: ActiveManager):
        while len(self.__actions) > 0:
            action = self.__actions.pop(0)
            if active.is_active():
                fn = action[0]
                kwargs = action[1]
                fn(active=active, **kwargs)
        self.__running = False

    def __action(self, active: ActiveManager, function, **kwargs):
        self.__actions.insert(0, (function, kwargs))

        if not self.__running:
            self.__running = True
            self.__run(active)
    
    def select_button(self, active, x_coord, y_coord, sleep_range=(2, 3.5)):
        for _ in range(5):
            x = x_coord + random.choice([1, -1])
            y = y_coord + random.choice([1, -1])
            self.__action(active, self.move_mouse, x=x, y=y)
        self.__action(active, self.move_mouse, x=x_coord, y=y_coord)
        self.__action(active, self.click, x=x_coord, y=y_coord, sleep_range=sleep_range)

    def click(self, active, **kwargs):
        """ Clicks mouse at current postion or at provided x and y.
        Usage - click(active, x = "x", y = "y", sleep_range=(min_time, max_time))
        """
        self.__action(active, self.__click, **kwargs)
        
    def __click(self, **kwargs):
        sleep_range = kwargs.get('sleep_range')

        win32.mouse_event(0x0002, 0, 0, 0, 0) # Left click press
        time.sleep(get_random_time(0.1, 0.15))
        win32.mouse_event(0x0004, 0, 0, 0, 0) # Left click release

        if any(sleep_range):
            time.sleep(get_random_time(*sleep_range))

    def keypress(self, active, **kwargs):
        """ Presses given key.
        Usage - keypress(active, key = "key")
        """
        self.__action(active, self.__keypress, **kwargs)

    def __keypress(self, **kwargs):
        key = kwargs.get('key')
        hold_shift = kwargs.get('hold_shift')

        keyboard.press("shift") if hold_shift else ""
        
        if key is not None:
            keyboard.press(key)
            time.sleep(get_random_time(0.75, 1.5)) if kwargs.get('duration') == 0 else kwargs.get('duration')
            keyboard.release(key)
        
        keyboard.release("shift") if hold_shift else ""

    def send_text(self, active, **kwargs):
        """Sends text"""
        self.__action(active, self.__send_text, **kwargs)

    def __send_text(self, **kwargs):
        text = kwargs.get('text')
        all_chat_key = kwargs.get('all_chat_key')

        if text is not None:
            keyboard.press(all_chat_key)
            time.sleep(get_random_time(0.1, 0.15))
            keyboard.release(all_chat_key)

            keyboard.press("backspace")
            time.sleep(get_random_time(0.1, 0.15))
            keyboard.release("backspace")

            keyboard.write(text, get_random_time(0.1, 0.15))

            keyboard.press("enter")
            time.sleep(get_random_time(0.1, 0.15))
            keyboard.release("enter")

            keyboard.press("enter")
            time.sleep(get_random_time(0.1, 0.15))
            keyboard.release("enter")
    
    def write_text(self, active, **kwargs):
        """Writes text"""
        self.__action(active, self.__write_text, **kwargs)

    def __write_text(self, **kwargs):
        keyboard.write(kwargs.get('text'), get_random_time(0.1, 0.15))

    def drag_mouse(self, target_x, target_y):
        win32.mouse_event(0x0002, 0, 0, 0, 0) # Left click press
        pydirectinput.moveTo(target_x, target_y, duration=get_random_time(0.5, 1.5))
        time.sleep(get_random_time(0.1, 0.15))
        win32.mouse_event(0x0004, 0, 0, 0, 0) # Left click release

    def move_mouse(self, active, **kwargs):
        """Move mouse"""
        self.__action(active, self.__move_mouse, **kwargs)

    def __move_mouse(self, **kwargs):
        x = kwargs.get('x')
        y = kwargs.get('y')

        time.sleep(get_random_time(0.1, 0.15))

        if x is not None and y is not None:
            pydirectinput.moveTo(get_res_scale_x(x), get_res_scale_y(y))
