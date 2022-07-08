# ASM236x Reverse Engineering Notes


## Feature comparison

| IC | USB VID:PID | USB 3 Generation × Lanes | PCIe Version × Lanes | IC Package |
| --- | --- | --- | --- | --- |
| [ASM2362][ASM2362] | 174c:2362 | Gen 2×1 | PCIe 3.x ×2 | QFN-64 |
| [ASM2364][ASM2364] | 174c:236? | Gen 2×2 | PCIe 3.x ×4 | QFN-88 |


## Hardware information

- CPU
  - Compatible with the MCS-51 (8051) instruction set.
- UART
  - 3V3
  - 921600(?) 8N1
  - Pins:
    - ASM2362
      - RX: IC pin ?
      - TX: IC pin ?
    - ASM2364
      - RX: IC pin 87
      - TX: IC pin 86


### IOCrest SY-ENC40231 (ASM2364)

- UART
  - TX can be accessed at resistor R10 on the pad nearest the ASM2364 IC.
  - RX can only be accessed on the ASM2364 IC itself.


## USB protocol

Everything is done over custom SCSI commands. Commands are documented in the
following format:

- `0xXX`: Command description.
  - `T`: Parameter description.
  - Returns: Nothing.

Where `0xXX` is the command byte and `T` is the Python type format character
of the first parameter. So, to send a command with the following format:

- `0xC0`: Example command.
  - `B`: Byte parameter.
  - `>H`: Big-endian 16-bit unsigned integer parameter.
  - `2x`: Two bytes of padding.
  - Returns: One byte of example data.

Where you want the byte parameter set to `0x01` and the big-endian u16 set to
`0xcafe`, you would use the following `sg_raw` command (replace `/dev/sg0`
with the path of your device's SG\_IO device file):

```
sg_raw -r 1 /dev/sg0 c0 01 ca fe 00 00
```


### Commands

- `0xE0`: Read configuration data?
  - `B`: Image index, can be either 0 or 1.
  - `4x`: Four bytes of padding.
  - Returns: 128 bytes of the configuration data.
  - Examples:
    - `e0 00 00 00 00 00`: Read image 0
    - `e0 01 00 00 00 00`: Read image 1
- `0xE1`: Write configuration data?
- `0xE4`: XDATA read.
  - `B`: The number of bytes to read, max 255.
  - `x`: Padding byte.
  - `>H`: XDATA address.
  - `x`: Padding byte.
  - Returns: N bytes of XDATA from the address you requested to read from.
  - Examples:
    - `e4 06 00 07 f0 00`: Read the 6-byte firmware version starting at
      address `0x07F0`.
- `0xE5`: XDATA write.
  - `B`: The byte of data to write.
  - `x`: Padding byte.
  - `>H`: XDATA address.
  - `x`: Padding byte.
  - Returns: Nothing.
  - Examples:
    - `e5 ff 00 07 f0 00`: Write `0xFF` to XDATA at address `0x07F0`.
- `0xE8`: Reload/restart firmware?
  - `11x`: 11 bytes of padding.
  - Returns: Nothing.
  - Examples:
    - `e8 00 00 00 00 00 00 00 00 00 00 00`


[ASM2362]: https://web.archive.org/web/20220608104342/https://www.asmedia.com.tw/product/Ee1YQF9sX7yyajH5/C5cYq34qpByQ6jm6
[ASM2364]: https://web.archive.org/web/20220703204756/https://www.asmedia.com.tw/product/BD5YqfdsPDqXFqi3/BF2yq24XzDuS5Tr4
