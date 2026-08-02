# Static Color Packet

Report ID: 0x00

Byte 1: 0x07
Byte 2: 0x01
Byte 3: 0x04
Byte 4: 0x04
Byte 5: 0x08 (Static RGB command)
Byte 6: Red
Byte 7: Green
Byte 8: Blue
Byte 9: Checksum = 0xFF - (sum(bytes 1-8) & 0xFF)

## Known USB Device IDs

Vendor ID: 0x3151

### MonsGeek FUN60 Pro HE

| Connection | Product ID |
|------------|-----------:|
| Wired | 0x502F |
| 2.4 GHz | 0x5026 |

Both interfaces use:

- Usage Page: 0xFFFF
- Usage: 0x02
- HID Feature Reports
- Identical RGB packet format (verified)