# ASM2x6x Reverse Engineering Notes


## Feature comparison

| IC | USB VID:PID | USB SuperSpeed Generation × Lanes | USB4 / Thunderbolt 3 | PCIe Version × Lanes | IC Package |
| --- | --- | --- | --- | --- | --- |
| [ASM2362][ASM2362] | 174c:2362 | Gen 2×1 | No | PCIe 3.x ×2 | QFN-64 |
| [ASM2364][ASM2364] | 174c:236? | Gen 2×2 | No | PCIe 3.x ×4 | QFN-88 |
| [ASM2464PD][ASM2464PD] | 174c:246? | Gen 3×2 | Yes | PCIe 4.x ×4 | FCCSP |
| [ASM2464PDX][ASM2464PDX] | 174c:246? | Gen 3×2 | Yes | PCIe 4.x ×4 | FCCSP |


## Hardware information

- CPU
  - Compatible with the MCS-51 (8051) instruction set.
  - One clock cycle per machine cycle ("1T").
    - Instruction cycle counts match the STCmicro STC15 series with the STC-Y5
      8051 core, with the exception of the MOVX instructions, which each seem
      to take between 2 and 5 clock cycles. See the instruction set summary
      starting on page 340 of [this PDF][stc] for a list of instructions and
      their cycle counts.
  - Operating frequency: ~114.285714 MHz
    - TODO: Confirm frequency of ASM2464PD(X) CPU.
- UART
  - 3V3
  - 921600 8N1
  - Pins:
    - ASM2362
      - RX: IC pin 63
      - TX: IC pin 62
    - ASM2364
      - RX: IC pin 87
      - TX: IC pin 86
    - ASM2464PD(X)
      - RX: IC ball A21
      - TX: IC ball B21
- I2C
  - Pins:
    - ASM2362
      - Data: IC pin 2
      - Clock: IC pin 3
    - ASM2364
      - Data: IC pin 5
      - Clock: IC pin 6

- Memory maps
  - ASM2364
    - Regions
      - `0x0000-0x5FFF`: 24 kB XRAM
      - `0x6000-0x6FFF`: 4 kB of unused address space (zero-filled, read-only)
      - `0x7000-0x7FFF`: 4 kB XRAM (SPI flash controller read/write buffer)
      - `0x8000-0x8FFF`: 4 kB XRAM (USB/SCSI buffers?)
      - `0x9000-0x93FF`: MMIO peripherals (USB?)
      - `0x9400-0x97FF`: Mirror of MMIO `0x9000-0x93FF`?
      - `0x9800-0x9BFF`: Mirror of MMIO `0x9000-0x93FF`?
      - `0x9C00-0x9DFF`: Mirror of MMIO `0x9000-0x91FF`?
      - `0x9E00-0x9FFF`: 512 B XRAM (USB control transfer buffer)
      - `0xA000-0xAFFF`: 4 kB XRAM, PCIe DMA address: `0x00820000` (NVMe I/O Submission Queue)
      - `0xB000-0xB1FF`: 512 B XRAM, PCIe DMA address: `0x00800000` (NVMe Admin Submission Queue)
      - `0xB200-0xB7FF`: MMIO peripherals (PCIe?)
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
      - `0xF000-0xFFFF`: 4 kB XRAM, PCIe DMA address: `0x00200000` (NVMe generic data buffer)
    - Peripherals
      - `0xC000`: UART.
        - Same memory map as [the one in ASMedia's USB host controllers][uart-regs].
        - Changing the divisor doesn't appear to work.


### IOCrest SY-ENC40231 (ASM2364)

- 25 MHz crystal oscillator.
- UART
  - TX can be accessed at resistor R10 on the pad nearest the ASM2364 IC.
  - RX can only be accessed on the ASM2364 IC itself.


### ORICO M2PVC3-G20 (ASM2364)

- 25 MHz crystal oscillator.
- UART
  - TX can be accessed at resistor R18 on the pad nearest the ASM2364 IC.
  - RX can only be accessed on the ASM2364 IC itself.


### Seagate FireCuda Gaming SSD (ASM2364)

- I2C bus is connected to an LED controller ([source][seagate-faze]).


### Blueendless M280U4A (ASM2464PD)

- 25 MHz crystal oscillator.
- UART header
  - Pin 1: Unknown
  - Pin 2: Ground
  - Pin 3: TX
  - Pin 4: Unknown


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


#### Seagate FireCuda Gaming SSD Commands

- `0xD1`: Get LED
  - `6B`: Magic: "GetLed"
  - `B`: LED index. Written to `0xE800`. Seen: 0, 1, 2, 3, 4, 5
    - 0: Unknown
    - 1: Status LED
    - 2: RGB LED 0 (the LED furthest from the Seagate logo)
    - 3: RGB LED 1
    - 4: RGB LED 2
    - 5: RGB LED 3 (the LED closest to the Seagate logo)
  - `B`: I2C mode? Written to `0xC871`. Seen: `0x03`, `0x20`, `0xff`
  - `x`: Padding byte.
  - `B`: Read length. Written to `0xE801` and `0xC874`.
  - `5x`: 5 bytes of padding.
  - Returns: "Read length" bytes of data.
- `0xD2`: Set LED
  - `6B`: Magic: "SetLed"
  - `B`: LED index. Written to `0xE800`.
  - `B`: I2C mode? `0x21`. Written to `0xC871`.
  - `x`: Padding byte.
  - `B`: Write length. Written to `0xE801`.
  - `5x`: 5 bytes of padding.
  - Payload: "Write length" bytes of data.
  - Returns: Nothing.


[stc]: https://web.archive.org/web/20200305112930/http://stcmicro.com/datasheet/STC15F2K60S2-en.pdf
[ASM2362]: https://web.archive.org/web/20220608104342/https://www.asmedia.com.tw/product/Ee1YQF9sX7yyajH5/C5cYq34qpByQ6jm6
[ASM2364]: https://web.archive.org/web/20220703204756/https://www.asmedia.com.tw/product/BD5YqfdsPDqXFqi3/BF2yq24XzDuS5Tr4
[ASM2464PD]: https://web.archive.org/web/20231113020255/https://www.asmedia.com.tw/product/802zX91Yw3tsFgm4/C64ZX59yu4sY1GW5
[ASM2464PDX]: https://web.archive.org/web/20231113020241/https://www.asmedia.com.tw/product/bDFzXa0ip1YI7Wj1/C64ZX59yu4sY1GW5
[uart-regs]: https://github.com/cyrozap/asmedia-xhc-re/blob/22fd32c53f7f34f50d659372334a384e269f5458/data/regs-asm1142.yaml#L700-L900
[seagate-faze]: https://web.archive.org/web/20241120033537/https://docs.zephyrproject.org/latest/boards/seagate/faze/doc/index.html
