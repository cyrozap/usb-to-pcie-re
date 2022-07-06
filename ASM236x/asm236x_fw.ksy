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
      - id: unk7
        type: u2
        repeat: expr
        repeat-expr: 2
      - id: magic
        type: u1
        doc: "Must be 0x5A."
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
      - id: crc16_maybe
        type: u2
    types:
      firmware:
        seq:
          - id: code
            size-eos: true
        instances:
          version:
            pos: 0x200
            size: 6
