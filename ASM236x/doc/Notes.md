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
  - 921600 8N1
  - Pins:
    - ASM2362
      - RX: IC pin ?
      - TX: IC pin ?
    - ASM2364
      - RX: IC pin 87
      - TX: IC pin 86

- Memory maps
  - ASM2364
    - Regions
      - `0x0000-0x5FFF`: 24 kB XRAM
      - `0x6000-0x6FFF`: 4 kB of unused address space (zero-filled, read-only)
      - `0x7000-0x7FFF`: 4 kB XRAM (SPI flash controller read/write buffer)
      - `0x8000-0x8FFF`: 4 kB XRAM (USB/SCSI buffers?)
      - `0x9000-0x9DFF`: MMIO peripherals (USB?)
      - `0x9E00-0x9FFF`: 512 B XRAM (USB control transfer buffer)
      - `0xA000-0xAFFF`: 4 kB XRAM
      - `0xB000-0xB7FF`: MMIO peripherals (PCIe?)
      - `0xB800-0xBFFF`: 2 kB XRAM
      - `0xC000-0xCFFF`: MMIO peripherals (UART, flash controller, timers, etc.)
      - `0xD000-0xD3FF`: 1 kB XRAM
      - `0xD400-0xD7FF`: Mirror of XRAM `0xD000-0xD3FF`
      - `0xD800-0xDFFF`: 2 kB XRAM (USB/SCSI buffers?)
      - `0xE000-0xE2FF`: Mirror of XRAM `0xD800-0xDAFF`
      - `0xE300-0xE7FF`: MMIO peripherals
      - `0xE800-0xE9FF`: 512 B XRAM
      - `0xEA00-0xEBFF`: Mirror of XRAM `0xE800-0xE9FF`
      - `0xEC00-0xEDFF`: Mirror of XRAM `0xE800-0xE9FF`
      - `0xEE00-0xEFFF`: Mirror of XRAM `0xE800-0xE9FF`
      - `0xF000-0xFFFF`: 4 kB XRAM (USB/PCIe buffer?)
    - Peripherals
      - `0xC000`: UART.
        - Same memory map as [the one in ASMedia's USB host controllers][uart-regs].
        - Changing the divisor doesn't appear to work.


### IOCrest SY-ENC40231 (ASM2364)

- UART
  - TX can be accessed at resistor R10 on the pad nearest the ASM2364 IC.
  - RX can only be accessed on the ASM2364 IC itself.


### ORICO M2PVC3-G20 (ASM2364)

- UART
  - TX can be accessed at resistor R18 on the pad nearest the ASM2364 IC.
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

- `0xE0`: Read configuration data.
  - `B`: Image index, can be either 0 or 1.
  - `4x`: Four bytes of padding.
  - Returns: 128 bytes of the configuration data.
  - Examples:
    - `e0 00 00 00 00 00`: Read image 0
    - `e0 01 00 00 00 00`: Read image 1
- `0xE1`: Write configuration data.
- `0xE2`: Flash read.
  - `B`: Unknown.
  - `>I`: Number of bytes to read from flash.
  - Returns: N bytes of flash data starting from address zero.
- `0xE3`: Firmware write.
  - `B`: Unknown.
  - `>I`: Number of bytes to write to flash.
  - Payload: The data to write to flash starting at address 0x80.
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
- `0xE6`: Send NVMe Admin Command
  - `B`: "Opcode (OPC)": 2 or 6 (only "Get Log Page" and "Identify" are supported)
  - `x`: Padding byte.
  - "Get Log Page" only:
    - `B`: "Log Page Identifier (LID)"
    - `2x`: 2 bytes of padding.
    - `>H`: "Number of Dwords Lower (NUMDL)"
    - `>Q`: "Log Page Offset"
  - "Identify" only:
    - `B`: "Controller or Namespace Structure (CNS)"
- `0xE8`: Reset
  - `B`: The type of reset to perform. `0x00` for CPU reset, `0x01` for some
    kind of "soft"/PCIe reset?
  - `10x`: 10 bytes of padding.
  - Returns: Nothing.
  - Examples:
    - `e8 00 00 00 00 00 00 00 00 00 00 00`
    - `e8 01 00 00 00 00 00 00 00 00 00 00`


[ASM2362]: https://web.archive.org/web/20220608104342/https://www.asmedia.com.tw/product/Ee1YQF9sX7yyajH5/C5cYq34qpByQ6jm6
[ASM2364]: https://web.archive.org/web/20220703204756/https://www.asmedia.com.tw/product/BD5YqfdsPDqXFqi3/BF2yq24XzDuS5Tr4
[uart-regs]: https://github.com/cyrozap/asmedia-xhc-re/blob/22fd32c53f7f34f50d659372334a384e269f5458/data/regs-asm1142.yaml#L700-L900
