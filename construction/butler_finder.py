import time

import cv2
import pyautogui
import numpy as np


class ButlerFinder:
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.templates = {
            "left": {
                "path": "images/butler_left.png",
                "region": (566, 613, 605 - 566, 651 - 613),
                "click": (624, 535),
            },
            "top": {
                "path": "images/butler_top.png",
                "region": (771, 346, 822 - 771, 396 - 346),
                "click": (856, 272),
            },
            "right": {
                "path": "images/butler_right.png",
                "region": (1111, 514, 1143 - 1111, 560 - 514),
                "click": (1189, 516),
            },
        }

    def _screenshot_bgr(self, region):
        """Take a screenshot and convert to OpenCV BGR."""
        img = pyautogui.screenshot(region=region)
        arr = np.array(img)
        return arr[:, :, ::-1]  # RGB → BGR

    def _load_template(self, path):
        tpl = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if tpl is None:
            raise FileNotFoundError(f"Template not found: {path}")
        if tpl.shape[2] == 4:
            tpl = tpl[:, :, :3]
        return tpl

    def find_and_click(self):
        """Try all butler locations and right-click the first found one."""
        for name, info in self.templates.items():
            region = info["region"]
            tpl_bgr = self._load_template(info["path"])
            screen_bgr = self._screenshot_bgr(region)

            result = cv2.matchTemplate(screen_bgr, tpl_bgr, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            if max_val >= self.threshold:
                click_x, click_y = info["click"]
                print(f"Butler found ({name}) with match {max_val:.2f} → right-clicking {click_x}, {click_y}")
                pyautogui.moveTo(click_x, click_y)
                pyautogui.leftClick(click_x, click_y)

                time.sleep(0.5)
                pyautogui.moveTo(click_x, click_y)
                pyautogui.leftClick(click_x, click_y)

                for _ in range(10):
                    pyautogui.press("1")
                    time.sleep(0.07)

                return True

        print("No butler found in any region.")
        return False
