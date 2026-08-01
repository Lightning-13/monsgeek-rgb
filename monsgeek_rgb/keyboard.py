import hid

from .protocol import create_static_color_packet


class Keyboard:
    """MonsGeek RGB keyboard."""

    VENDOR_ID = 0x3151
    PRODUCT_ID = 0x5026
    USAGE_PAGE = 0xFFFF
    USAGE = 0x02

    def __init__(self):
        self.device = hid.device()

        self.path = self._find_device()

        if self.path is None:
            raise RuntimeError("Compatible MonsGeek keyboard not found.")

        self.device.open_path(self.path)

    def _find_device(self):
        for d in hid.enumerate():
            if (
                d["vendor_id"] == self.VENDOR_ID
                and d["product_id"] == self.PRODUCT_ID
                and d["usage_page"] == self.USAGE_PAGE
                and d["usage"] == self.USAGE
            ):
                return d["path"]

        return None

    def set_color(self, r, g, b):
        packet = create_static_color_packet(r, g, b)
        self.device.send_feature_report(packet)

    def close(self):
        self.device.close()