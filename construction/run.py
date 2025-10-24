import time
import random
import win32gui
import keyboard  # pip install keyboard

from inv import ImageMatchCounter
from table import TableEditor
from butler_finder import ButlerFinder


if __name__ == "__main__":
    # Focus RuneLite window
    window_name = "RuneLite - OIjake"
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        raise Exception(f"Window '{window_name}' not found.")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)

    # Timing configuration
    after_removing_min = 0.53
    after_removing_max = 0.63
    after_building_min = 0.56
    after_building_max = 0.65

    # Initialize systems
    counter = ImageMatchCounter()
    editor = TableEditor()
    butler = ButlerFinder()

    print("Automation started. Press ESC to stop at any time.")
    stop_flag = False

    # Setup ESC listener
    def stop_listener(e):
        nonlocal stop_flag
        print("ESC pressed — stopping automation.")
        stop_flag = True

    keyboard.on_press_key("esc", stop_listener)

    # Wait until detection stabilizes
    while counter.get_count() == 0 and not stop_flag:
        time.sleep(0.2)
    if stop_flag:
        counter.stop()
        exit()

    print("Detection active.")

    try:
        while not stop_flag:
            current_count = counter.get_count()
            print(f"Current planks: {current_count}")

            if current_count >= 6:
                # Do table build/remove loop
                editor.execute('6')
                if stop_flag: break
                time.sleep(random.uniform(after_building_min, after_building_max))
                editor.execute('1')
                if stop_flag: break
                time.sleep(random.uniform(after_removing_min, after_removing_max))

            else:
                print("Less than 6 planks — trying to interact with butler...")
                found = butler.find_and_click()

                if stop_flag: break

                if not found:
                    # No butler and no planks → idle until planks replenish
                    print("No butler and no planks — idling...")
                    while counter.get_count() < 6 and not stop_flag:
                        time.sleep(0.1)
                    if stop_flag: break
                    print("Planks replenished — resuming work.")
                else:
                    # Butler was clicked → wait and check again
                    print("Butler interaction complete, checking plank count...")
                    time.sleep(1)

            time.sleep(0.25)

    except KeyboardInterrupt:
        print("Stopped manually.")

    finally:
        counter.stop()
        print("Exiting cleanly.")
