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
    instances:
      unk0:
        pos: 1
        type: u2
      serial_number:
        pos: 4
        type: str
        encoding: ASCII
        size: 12
      ep0_manufacturer_string:
        pos: 0x18
        type: str
        encoding: ASCII
        size: 7
      t10_manufacturer_string:
        pos: 0x3C
        type: str
        encoding: ASCII
        size: 4
      ep0_product_string:
        pos: 0x44
        type: str
        encoding: ASCII
        size: 14
      t10_product_string:
        pos: 0x64
        type: str
        encoding: ASCII
        size: 12
      usb_info:
        pos: 0x74
        type: usb_info
      unk7:
        pos: 0x7A
        type: u2
        repeat: expr
        repeat-expr: 3
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
