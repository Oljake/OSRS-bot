import cv2
import numpy as np
import pyautogui
import tkinter as tk
import threading
import time

class ImageMatchCounter:
    def __init__(self,
                 template_path="images/plank.png",
                 threshold=0.8,
                 region=(1834, 592, 2406, 1287),
                 overlay_pos=(1498, 883),
                 overlay_size=(200, 50),
                 scan_interval=0.25):

        self.template_path = template_path
        self.threshold = threshold
        self.x1, self.y1, self.x2, self.y2 = region
        self.scan_interval = scan_interval
        self.overlay_x, self.overlay_y = overlay_pos
        self.overlay_w, self.overlay_h = overlay_size

        self.tpl_bgr, self.tpl_mask = self._load_template_with_alpha(template_path)
        self.region_width = self.x2 - self.x1
        self.region_height = self.y2 - self.y1

        self.current_count = 0
        self._stop_event = threading.Event()

        # Start overlay and scanning in background thread
        self._start_overlay_thread()

    # --- Utilities ---
    def _load_template_with_alpha(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img.shape[2] == 4:
            bgr = img[:, :, :3]
            alpha = img[:, :, 3]
            mask = (alpha > 0).astype(np.uint8) * 255
        else:
            bgr = img
            mask = None
        return bgr, mask

    def _screenshot_bgr(self, region=None):
        left, top, width, height = region
        pil = pyautogui.screenshot(region=(left, top, width, height))
        arr = np.array(pil)
        return arr[:, :, ::-1].copy()

    def _find_all_matches(self, screen_bgr, tpl_bgr, tpl_mask=None, threshold=0.8):
        method = cv2.TM_CCOEFF_NORMED
        h, w = tpl_bgr.shape[:2]
        sh, sw = screen_bgr.shape[:2]
        if h > sh or w > sw:
            return []
        if tpl_mask is not None:
            result = cv2.matchTemplate(screen_bgr, tpl_bgr, method, mask=tpl_mask)
        else:
            result = cv2.matchTemplate(screen_bgr, tpl_bgr, method)
        matches = []
        result_copy = result.copy()
        nms_radius = max(w, h) // 2
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_copy)
            if max_val < threshold:
                break
            top_left = max_loc
            matches.append((top_left[0], top_left[1], w, h, float(max_val)))
            x, y = top_left
            x1 = max(0, x - nms_radius)
            y1 = max(0, y - nms_radius)
            x2 = min(result_copy.shape[1] - 1, x + nms_radius)
            y2 = min(result_copy.shape[0] - 1, y + nms_radius)
            result_copy[y1:y2+1, x1:x2+1] = -1.0
        return matches

    # --- Overlay ---
    def _start_overlay_thread(self):
        thread = threading.Thread(target=self._run_overlay, daemon=True)
        thread.start()

    def _run_overlay(self):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        root.geometry(f"{self.overlay_w}x{self.overlay_h}+{self.overlay_x}+{self.overlay_y}")
        root.attributes("-alpha", 0.6)  # 0.0 = fully transparent, 1.0 = fully opaque

        label = tk.Label(root, text="Matches: 0", font=("Arial", 24), fg="white", bg="#444444")
        label.pack(fill="both", expand=True)

        def update_overlay():
            if self._stop_event.is_set():
                root.destroy()
                return

            screen = self._screenshot_bgr(region=(self.x1, self.y1, self.region_width, self.region_height))
            matches = self._find_all_matches(screen, self.tpl_bgr, self.tpl_mask, threshold=self.threshold)
            self.current_count = len(matches)
            label.config(text=f"Matches: {self.current_count}")
            root.after(int(self.scan_interval * 50), update_overlay)

        update_overlay()
        root.mainloop()

    # --- Public API ---
    def get_count(self):
        """Return the most recently detected number of matches."""
        return self.current_count

    def stop(self):
        """Stop the scanning and overlay."""
        self._stop_event.set()

# === Example Usage ===
if __name__ == "__main__":
    counter = ImageMatchCounter()

    # Continuously print how many matches there are
    try:
        while True:
            print("Current count:", counter.get_count())
            time.sleep(0.25)
    except KeyboardInterrupt:
        counter.stop()
        print("Stopped.")
