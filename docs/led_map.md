# LED Map

This document describes the relationship between the MonsGeek FUN60 Pro's internal LED indices and the keyboard's physical keys.

The RGB framebuffer contains space for **126 LED slots**, but only **61** are connected to physical keys on this keyboard.

During reverse engineering, all active LED slots were identified by observing which framebuffer locations affected the keyboard's lighting. However, only a small number of those slots have been individually confirmed against specific physical keys.

This document separates **verified mappings** from **known active indices** to avoid presenting assumptions as facts.

---

# Framebuffer Layout

Each LED occupies three consecutive bytes in the framebuffer.

```text
Offset = LED Index × 3

Byte 0 = Red
Byte 1 = Green
Byte 2 = Blue
```

Example:

```text
LED 9

Offset:
27

Bytes:
27 = Red
28 = Green
29 = Blue
```

---

# Verified Key Mappings

The following mappings have been confirmed directly through USB capture comparison and individual per-key testing.

| LED Index | Physical Key | Status     |
| --------- | ------------ | ---------- |
| 9         | A            | ✅ Verified |
| 40        | B            | ✅ Verified |

---

# Active LED Indices

The following LED indices correspond to physical keys on the MonsGeek FUN60 Pro.

Although each index has been confirmed to illuminate a real key, most have **not yet been individually identified**.

```text
1,2,3,4,5,7,8,9,13,14,15,16,17,19,20,21,22,23,25,26,
27,28,31,32,33,34,37,38,39,40,41,43,44,45,46,49,50,
51,52,55,56,57,58,61,62,63,64,65,67,68,69,70,71,73,
74,76,77,79,80,81,83
```

Total active LEDs:

```text
61
```

---

# Unused LED Slots

The framebuffer reserves space for **126 RGB entries**.

Only 61 are connected to physical keys.

The remaining entries appear to be unused padding.

These unused slots have no observable effect when written.

---

# Mapping Methodology

Key mappings were established using the following process:

1. Capture the USB traffic while changing the color of a single key in the official software.
2. Compare the modified framebuffer with a baseline capture.
3. Identify the RGB bytes that changed.
4. Convert the framebuffer offset into an LED index.
5. Verify the mapping by reproducing the change through direct HID communication.

Only mappings confirmed using this method are listed as **Verified**.

---

# Future Work

The remaining active LED indices can be mapped using the same process.

Once additional keys have been verified, this document can be expanded into a complete LED-to-key reference table suitable for OpenRGB, SignalRGB, or other RGB control software.

Contributions are welcome if you have verified mappings for additional keys.
