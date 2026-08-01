"""
Checksum calculation for MonsGeek RGB packets.
"""


def calculate_checksum(data: bytes) -> int:
    """
    Calculate the MonsGeek packet checksum.

    The checksum is:
        checksum = (0xFF - (sum(data) & 0xFF)) & 0xFF

    Args:
        data: Bytes participating in the checksum.

    Returns:
        Checksum byte.
    """
    return (0xFF - (sum(data) & 0xFF)) & 0xFF