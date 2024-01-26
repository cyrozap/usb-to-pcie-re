meta:
  id: asm2464_fw
  endian: le
  title: ASM2464 firmware image
  license: CC0-1.0
seq:
  - id: body_len
    type: u4
  - id: body
    size: body_len
  - id: magic
    type: u1
    doc: "0xA5: ASM2464"
  - id: checksum
    type: u1
    doc: "8-bit sum of all the bytes in the firmware body."
  - id: crc
    type: u4
    doc: "CRC-32 of the firmware body (Python `zlib.crc32()`)."
