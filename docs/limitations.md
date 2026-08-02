# Known Limitations

This document summarizes the current limitations of the MonsGeek FUN60 Pro RGB protocol based on the reverse engineering work performed for this project.

The limitations listed here are based on observed device behavior, USB captures of the official software, and direct experimentation. They should be considered the current state of knowledge rather than proof that alternative undocumented functionality cannot exist.

---

# No General-Purpose RGB Streaming

The primary objective of this project was to determine whether the keyboard supports arbitrary host-driven per-key RGB streaming similar to OpenRGB or SignalRGB.

No such protocol was identified.

Throughout the investigation:

* The official MonsGeek software never transmitted continuous RGB framebuffer updates.
* No RAM-backed RGB transfer opcode was observed.
* No undocumented streaming interface was discovered.
* All successful custom RGB writes used the same persistent framebuffer mechanism.

At the time of writing, there is no evidence that the keyboard exposes a protocol suitable for continuous high-frame-rate RGB animation.

---

# Custom Layer Uses Persistent Storage

Custom Layer updates are written to persistent onboard storage.

Observed evidence includes:

* Colors remain after disconnecting and reconnecting the keyboard.
* The official software applies changes only after **Save to Layer** is selected.
* Continuous writes produce behavior consistent with repeated flash programming rather than volatile RAM updates.

Applications should therefore treat Custom Layer writes as configuration changes rather than animation frames.

---

# Flash Wear

Because Custom Layer updates appear to be stored in non-volatile memory, continuously rewriting the framebuffer is not recommended.

Modern flash memory is designed for many write cycles, but it is not intended for dozens of writes per second over extended periods.

Reasonable use cases include:

* Static layouts
* Per-key profiles
* Configuration utilities
* Occasional color updates

High-frequency animation loops should be avoided.

---

# Audio Visualizer Is Not RGB Streaming

One protocol family (`0x0D`) initially appeared to provide continuous host-to-keyboard communication.

Further investigation showed that these packets contain compact intensity values rather than RGB colors.

The keyboard firmware renders the visualizer effect internally.

This channel cannot be used to upload arbitrary per-key RGB data.

---

# Partial LED Mapping

The keyboard framebuffer contains 126 possible RGB slots.

Only 61 correspond to physical keys.

At the time of writing:

* All active LED indices have been identified.
* Two LED positions have been directly verified:

  * LED 9 → A
  * LED 40 → B
* The remaining active positions have not yet been individually mapped to physical key names.

This does not affect RGB functionality but limits the ability to reference keys symbolically.

---

# Device Compatibility

This project has been verified only with the MonsGeek FUN60 Pro.

Although other MonsGeek and Yichip-based keyboards may share parts of the protocol, compatibility has not been confirmed.

Additional devices should be treated as separate reverse engineering targets until verified.

---

# Firmware Revisions

The protocol described by this repository reflects the firmware version available during the investigation.

Future firmware updates could:

* Add new commands
* Remove existing commands
* Modify packet formats
* Introduce live-preview functionality

If MonsGeek releases software supporting new RGB capabilities, new USB captures may reveal additional protocol features.

---

# Future Possibilities

Several areas remain open for future investigation.

These include:

* Complete physical key mapping.
* Firmware analysis of the AT32F405 microcontroller.
* Investigation of undocumented HID commands.
* Comparison with additional MonsGeek and Yichip devices.
* Monitoring future software releases for protocol changes.

Any future discoveries should be considered additions to the protocol rather than corrections to the work documented here.

---

# Summary

Current verified capabilities include:

* ✅ Direct HID communication
* ✅ Static RGB
* ✅ Persistent per-key RGB
* ✅ Wired mode
* ✅ 2.4 GHz mode
* ✅ Custom Layer programming

The following capabilities were **not identified** during this investigation:

* ❌ General-purpose RAM-based RGB streaming
* ❌ High-frame-rate per-key animation
* ❌ Live RGB preview through the observed protocol

This repository documents the protocol as it was observed and verified. Future work may expand upon these findings if new evidence becomes available.
