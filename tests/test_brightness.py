import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
from monsgeek_rgb.keyboard import Keyboard


keyboard = Keyboard()

try:
    for level in range(4):
        print(f"Setting brightness level: {level}")
        keyboard.set_brightness(level)
        time.sleep(1)

finally:
    keyboard.close()
    print("Done")