# RTL921x Reverse Engineering Notes


## Hardware information

- CPU is some variant of MIPS.
- UART
  - Runs at 9600 baud by default.
  - 25 MHz clock.
- Memory map
  - `0x8C000000-0x8C1FFFFF`: 2 MB Mask ROM?
  - `0x8C200000-0x8C3FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8C400000-0x8C5FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8C600000-0x8C7FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8C800000-0x8C9FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8CA00000-0x8CBFFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8CC00000-0x8CDFFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8CE00000-0x8CFFFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8D000000-0x8D1FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8D200000-0x8D3FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8D400000-0x8D5FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8D600000-0x8D7FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8D800000-0x8D9FFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8DA00000-0x8DBFFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8DC00000-0x8DDFFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`
  - `0x8DE00000-0x8DFFFFFF`: Mirror of `0x8C000000-0x8C1FFFFF`


## Firmware information

- Firmware is based on µC/OS-II.
- Some of the firmware exists in mask ROM.
- The firmware on flash is either loaded into RAM or executed in place (XIP).
  - Need to confirm with SPI trace.


## USB protocol

Vendor SCSI commands.

- `e2 00 00 00 a2 00 00 00 c8 00 50 b3 04 00 00 00`
  - Get "IC Ver"
  - 4B response: `01 00 01 a0 (0xa0010001)`
- `e2 00 00 00 92 00 00 00 c4 00 50 b3 04 00 00 00`
  - 4B response: `00 00 00 00`
- `e2 00 00 00 a2 00 00 00 5c 00 50 b3 04 00 00 00`
  - 4B response: `b0 65 d9 03 (0x03d965b0)`
- `e2 00 00 00 92 00 00 00 00 40 00 ac 60 00 00 00`
  - Get NVDATA?
  - 96B response
- `e2 00 00 00 92 00 00 00 00 40 00 ac 00 10 00 00`
  - Get NVDATA?
  - 4096B response
- `e2 00 00 00 a2 00 00 00 0c c7 00 b3 04 00 00 00`
  - 4B response: `8c ae 82 00 (0x0082ae8c)`
- `e2 00 00 00 a2 00 00 00 f8 00 50 b3 01 00 00 00`
  - 1B response: `00`
- `e2 00 00 00 a6 00 00 00 00 00 00 00 01 00 00 00`
  - 1B response: `01`
- `e2 00 00 00 96 00 00 00 00 00 00 00 c0 00 00 00`
  - Get EFUSE
  - 192B response
