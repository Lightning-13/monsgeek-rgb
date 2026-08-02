import hid

from .devices import SUPPORTED_DEVICES
from .protocol import (
    create_brightness_packet,
    create_static_color_packet,
)


class Keyboard:
    """Interface for controlling supported MonsGeek RGB keyboards."""

    def __init__(self):
        """Connect to the first compatible keyboard."""
        self.device = hid.device()

        self.path = self._find_device()

        if self.path is None:
            raise RuntimeError("Compatible MonsGeek keyboard not found.")

        self.device.open_path(self.path)

    def _find_device(self):
        """Locate a supported keyboard and return its HID path."""

        for hid_device in hid.enumerate():
            for supported in SUPPORTED_DEVICES:
                if (
                    hid_device["vendor_id"] == supported["vendor_id"]
                    and hid_device["product_id"] == supported["product_id"]
                    and hid_device["usage_page"] == supported["usage_page"]
                    and hid_device["usage"] == supported["usage"]
                ):
                    return hid_device["path"]

        return None

    def set_color(self, r: int, g: int, b: int):
        """Set the keyboard to a static RGB color."""

        packet = create_static_color_packet(r, g, b)
        self.device.send_feature_report(packet)

    def set_red(self):
        """Set the keyboard color to red."""

        self.set_color(255, 0, 0)

    def set_green(self):
        """Set the keyboard color to green."""

        self.set_color(0, 255, 0)

    def set_blue(self):
        """Set the keyboard color to blue."""

        self.set_color(0, 0, 255)

    def turn_off(self):
        """Turn off all keyboard LEDs."""

        self.set_color(0, 0, 0)

    def set_brightness(self, level: int):
        """Set keyboard brightness (0-200)."""

        packet = create_brightness_packet(level)
        self.device.send_feature_report(packet)

    def close(self):
        """Close the HID connection."""

        self.device.close()