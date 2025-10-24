import random
import time
import pyautogui
import win32gui

class TableEditor:
    def __init__(self, base_x=1052, base_y=867, x_range=(778, 1307), y_range=(1008, 1031)):
        self.base_x = base_x
        self.base_y = base_y
        self.x_range = x_range
        self.y_range = y_range

    def right_click_base(self):
        """Move to the base position and right-click."""
        pyautogui.moveTo(self.base_x, self.base_y)
        pyautogui.rightClick(self.base_x, self.base_y)

    def random_click(self):
        """Click on a random point within the defined x and y range."""
        x = random.randint(*self.x_range)
        y = random.randint(*self.y_range)
        pyautogui.moveTo(x, y)
        pyautogui.leftClick(x, y)

    @staticmethod
    def press_key_repeatedly(key, times=10, delay=0.05):
        """Press a key repeatedly with a short delay between presses."""
        for _ in range(times):
            pyautogui.press(key)
            time.sleep(delay)

    def execute(self, key):
        """Run the full sequence of actions."""
        self.right_click_base()
        self.random_click()
        self.press_key_repeatedly(key)


if __name__ == "__main__":
    window_name = "RuneLite - OIjake"
    hwnd = win32gui.FindWindow(None, window_name)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)

    # After removing the table you have you wait for that amount to start new event
    after_removing_min = 0.53
    after_removing_max = 0.63

    # After building the table you have you wait for that amount to start new event
    after_building_min = 0.56
    after_building_max = 0.65

    editor = TableEditor()
    for i in range(2):
        editor.execute('6')
        time.sleep(random.uniform(after_building_min, after_building_max))
        editor.execute('1')
        time.sleep(random.uniform(after_removing_min, after_removing_max))
