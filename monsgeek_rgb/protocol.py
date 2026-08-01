"""
Packet generation for MonsGeek RGB keyboards.
"""

from .checksum import calculate_checksum


def create_static_color_packet(r: int, g: int, b: int) -> bytes:
    """
    Create a 65-byte HID Feature Report for a static RGB color.
    """

    if not all(0 <= x <= 255 for x in (r, g, b)):
        raise ValueError("RGB values must be between 0 and 255.")

    packet = bytearray(65)

    packet[1] = 0x07
    packet[2] = 0x01
    packet[3] = 0x04
    packet[4] = 0x04
    packet[5] = 0x08

    packet[6] = r
    packet[7] = g
    packet[8] = b

    packet[9] = calculate_checksum(packet[1:9])

    return bytes(packet)