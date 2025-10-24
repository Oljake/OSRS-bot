
# 🪵 Mahogany Table Automation

Automates the build and removal of **mahogany tables** in RuneLite using Python.
Also manages plank inventory and interacts with the in-game butler to retrieve more planks when needed.

---

## Features

- **Plank Detection**  
  Tracks the number of mahogany planks on-screen using template matching with OpenCV.  
  Displays a small overlay showing the current plank count.

- **Table Building and Removing**  
  Automates:
  1. Building a mahogany table using available planks.  
  2. Removing the table after building.  
  3. Repeating the build-remove cycle continuously.

- **Butler Interaction**  
  If plank count is low:
  - Searches for the in-game butler in multiple screen regions.  
  - Automatically clicks the butler to request more planks.  
  - Resumes building once planks are replenished.

- **Safe Stop**  
  Press `ESC` at any time to stop the automation safely.

---

## Project Structure

```
mahogany-automation/
├─ README.md              # This file
├─ inv.py                 # Detects planks on-screen
├─ table.py               # Builds and removes tables
├─ butler_finder.py       # Finds and interacts with the butler
├─ main.py                # Orchestrates the automation
└─ images/                # Screenshot templates (planks, butler)
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/mahogany-automation.git
cd mahogany-automation
```

2. Install dependencies:

```bash
pip install opencv-python pyautogui numpy keyboard pywin32
```

3. Place the template images in the `images/` folder.

---

## Usage

```bash
python main.py
```

- Watch the overlay for the current plank count.  
- The script handles table building and butler interactions automatically.  
- Press `ESC` at any time to stop the automation.

---

## Configuration

- **RuneLite window**: Make sure it's named `"RuneLite - YOUR ACCOUNT NAME"` or update the name in `main.py`.
- **Timing settings** (adjust in `main.py`):
  ```python
  after_building_min = 0.56
  after_building_max = 0.65
  after_removing_min = 0.53
  after_removing_max = 0.63
  ```
- **Template thresholds**: Modify in each module (`inv.py`, `butler_finder.py`) if detection is inaccurate.

---

## Notes

- Works best on a screen resolution matching the template regions.  
- Overlay is semi-transparent and always on top for real-time monitoring.  
- Automation stops automatically if `ESC` is pressed.
