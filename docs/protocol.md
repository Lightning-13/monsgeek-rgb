# MonsGeek FUN60 Pro RGB Protocol Specification

This document describes the USB HID protocol used by the MonsGeek FUN60 Pro for RGB lighting control.

The protocol described here was reverse engineered from USB captures of the official MonsGeek software and verified through direct communication using `hidapi`.

---

# Transport

## USB Interface

Lighting commands are sent using **USB HID Feature Reports** over the keyboard's vendor-specific HID interface.

| Property      | Value       |
| ------------- | ----------- |
| Vendor ID     | `0x3151`    |
| Wireless PID  | `0x5026`    |
| Wired PID     | `0x502F`    |
| Interface     | `2 (MI_02)` |
| Report Length | `65 bytes`  |

Feature Reports always consist of:

* Report ID (`0x00`)
* 64-byte payload

Communication uses standard HID `SET_REPORT` and `GET_REPORT` requests over Endpoint 0.

---

# Checksum

Every packet observed during reverse engineering uses the same checksum algorithm.

```
checksum = (255 - (sum(header_bytes) & 0xFF)) & 0xFF
```

The checksum byte is appended to the end of the packet header.

This checksum has been verified across the following opcode families:

* `0x07`
* `0x0C`
* `0x0D`
* `0xF7`

---

# Mode Selection

Before writing a Custom Layer, the keyboard must be switched into Custom Picture mode.

Packet:

```
07 0D 04 04 00 00 C8 C8 53
```

Observed behavior:

* Enables display of the Custom Layer framebuffer.
* Allows uploaded RGB data to persist.
* Must be sent before framebuffer writes.

The purpose of the trailing `C8 C8` bytes has not been determined.

---

# Framebuffer

The keyboard stores RGB data inside a framebuffer consisting of:

* 378 bytes total
* 126 RGB slots
* 3 bytes per slot

```
126 LEDs × 3 bytes = 378 bytes
```

Only **61 slots** correspond to physical keys on the FUN60 Pro.

The remaining slots appear unused.

---

# Framebuffer Layout

Each LED occupies three consecutive bytes:

```
Red
Green
Blue
```

Buffer offsets are calculated as:

```
offset = led_index × 3
```

For example:

```
LED 9

Offset:
27

Bytes:
27 = Red
28 = Green
29 = Blue
```

---

# Frame Transfer

A complete framebuffer update is transferred using **seven packets**.

## Header Format

```
0C 00 FF chunk length apply 00 checksum
```

Fields:

| Byte | Meaning           |
| ---- | ----------------- |
| 0    | Opcode (`0x0C`)   |
| 1    | Reserved (`0x00`) |
| 2    | Constant (`0xFF`) |
| 3    | Chunk Index       |
| 4    | Data Length       |
| 5    | Apply Bit         |
| 6    | Reserved          |
| 7    | Checksum          |

---

## Chunk Sizes

| Chunk | RGB Data |
| ----- | -------- |
| 0     | 56 bytes |
| 1     | 56 bytes |
| 2     | 56 bytes |
| 3     | 56 bytes |
| 4     | 56 bytes |
| 5     | 56 bytes |
| 6     | 42 bytes |

Total:

```
56 × 6 + 42 = 378 bytes
```

---

# Apply Bit

Only the final packet triggers an LED redraw.

| Chunk | Apply Bit |
| ----- | --------- |
| 0–5   | `0x00`    |
| 6     | `0x01`    |

---

# Handshake

The keyboard implements a busy/ready handshake to prevent data overruns.

For every chunk:

1. Send query packet.
2. Read feature report.
3. Wait until the device reports Ready.
4. Send the next framebuffer chunk.

---

## Query Packet

```
F7
```

---

## Ready Status

After calling `GET_REPORT`, inspect payload byte **5**.

| Value  | Meaning |
| ------ | ------- |
| `0x01` | Ready   |
| `0x00` | Busy    |

A fresh query packet must be sent before every poll attempt.

Repeated `GET_REPORT` requests without another query return stale state.

---

# Active LED Slots

The framebuffer contains 126 possible LED positions.

Only the following 61 indices are active on the FUN60 Pro:

```
1,2,3,4,5,7,8,9,13,14,15,16,17,19,20,21,22,23,25,26,
27,28,31,32,33,34,37,38,39,40,41,43,44,45,46,49,50,
51,52,55,56,57,58,61,62,63,64,65,67,68,69,70,71,73,
74,76,77,79,80,81,83
```

Verified key mappings:

| LED Index | Key |
| --------- | --- |
| 9         | A   |
| 40        | B   |

Additional mappings remain to be verified.

---

# Observed Limitations

The protocol supports persistent writes to the keyboard's onboard Custom Layer.

No general-purpose RAM-based RGB streaming mechanism was identified during this investigation.

The official MonsGeek software follows the same workflow by committing Custom Layer changes rather than previewing them live.

As a result, the protocol is well suited for:

* Static layouts
* Per-key profiles
* Configuration utilities

It is not suitable for continuous high-frame-rate RGB animation without additional undocumented functionality.

---

# Revision History

| Version | Notes                                              |
| ------- | -------------------------------------------------- |
| 1.0     | Initial reverse-engineered protocol specification. |
