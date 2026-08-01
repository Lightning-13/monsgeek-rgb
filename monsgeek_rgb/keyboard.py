import hid

from .protocol import create_static_color_packet
from .devices import SUPPORTED_DEVICES


class Keyboard:
    """MonsGeek RGB keyboard."""

    def __init__(self):
        self.device = hid.device()

        self.path = self._find_device()

        if self.path is None:
            raise RuntimeError("Compatible MonsGeek keyboard not found.")

        self.device.open_path(self.path)

    def _find_device(self):
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

    def set_color(self, r, g, b):
        packet = create_static_color_packet(r, g, b)
        self.device.send_feature_report(packet)

    def set_red(self):
        self.set_color(255, 0, 0)

    def set_green(self):
        self.set_color(0, 255, 0)

    def set_blue(self):
        self.set_color(0, 0, 255)

    def turn_off(self):
        self.set_color(0, 0, 0)

    def close(self):
        self.device.close()