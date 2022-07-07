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


[ASM2362]: https://web.archive.org/web/20220608104342/https://www.asmedia.com.tw/product/Ee1YQF9sX7yyajH5/C5cYq34qpByQ6jm6
[ASM2364]: https://web.archive.org/web/20220703204756/https://www.asmedia.com.tw/product/BD5YqfdsPDqXFqi3/BF2yq24XzDuS5Tr4
