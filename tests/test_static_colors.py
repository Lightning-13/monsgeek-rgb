from time import sleep
from monsgeek_rgb import Keyboard

kb = Keyboard()

kb.set_red()
sleep(1)

kb.set_green()
sleep(1)

kb.set_blue()
sleep(1)

kb.turn_off()

kb.close()