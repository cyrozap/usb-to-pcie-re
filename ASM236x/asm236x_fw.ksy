meta:
  id: asm236x_fw
  endian: le
  title: ASM236x firmware image
  license: CC0-1.0
seq:
  - id: header
    type: header
    size: 0x80
  - id: body
    type: body
types:
  usb_info:
    seq:
      - id: id_vendor
        type: u2
      - id: id_product
        type: u2
      - id: bcd_device
        type: u2
  header:
    seq:
      - id: unk0
        size: 4
      - id: serial_number
        size: 20
      - id: ep0_manufacturer_string
        size: 36
      - id: t10_manufacturer_string
        size: 8
      - id: ep0_product_string
        size: 32
      - id: t10_product_string
        size: 16
      - id: usb_info
        type: usb_info
      # Offset 0x7a
      - id: lp_if_u3
        type: b2
      - id: lp_if_idle
        type: b2
      - id: idle_timer
        type: b4
      # Offset 0x7b
      - id: unk7b_76
        type: b2
      - id: pcie_lane
        type: b2
      - id: pcie_speed
        type: b2
      - id: pcie_aspm
        type: b2
      # Offset 0x7c
      - id: unk7c
        type: u1
      # Offset 0x7d
      - id: disable_slow_enumeration
        type: b1
      - id: disable_2tb
        type: b1
      - id: disable_low_power_mode
        type: b1
      - id: disable_u1u2
        type: b1
      - id: disable_wtg
        type: b1
      - id: disable_two_leds
        type: b1
      - id: disable_eup
        type: b1
      - id: disable_usb_removable
        type: b1
      # Offset 0x7e
      - id: magic
        type: u1
        doc: "Must be 0x5A."
      # Offset 0x7f
      - id: checksum
        type: u1
        doc: "8-bit sum of all the bytes from offset 0x04 through 0x7E, inclusive."
  body:
    seq:
      - id: size
        type: u2
      - id: firmware
        type: firmware
        size: size
      - id: unk
        type: u1
      - id: checksum
        type: u1
        doc: "8-bit sum of all the code bytes."
    types:
      firmware:
        seq:
          - id: code
            size-eos: true
        instances:
          version:
            pos: 0x200
            size: 6
