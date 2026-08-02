"""
monsgeek_rgb

Python library for controlling RGB lighting on MonsGeek keyboards.
"""

from .keyboard import Keyboard
from .protocol import create_static_color_packet

__version__ = "1.0.0"

__all__ = [
    "Keyboard",
    "create_static_color_packet",
]