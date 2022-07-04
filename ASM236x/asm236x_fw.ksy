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
  usb_ids:
    seq:
      - id: vid
        type: u2
      - id: pid
        type: u2
  header:
    instances:
      unk0:
        pos: 1
        type: u2
      unk1:
        pos: 4
        type: str
        encoding: ASCII
        size: 12
      unk2:
        pos: 0x18
        type: str
        encoding: ASCII
        size: 7
      unk3:
        pos: 0x3C
        type: str
        encoding: ASCII
        size: 4
      unk4:
        pos: 0x44
        type: str
        encoding: ASCII
        size: 14
      unk5:
        pos: 0x64
        type: str
        encoding: ASCII
        size: 12
      usb_ids:
        pos: 0x74
        type: usb_ids
      unk7:
        pos: 0x78
        type: u2
        repeat: expr
        repeat-expr: 4
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
