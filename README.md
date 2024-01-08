# USB to PCIe Reverse Engineering


## Introduction

There are several chips on the market that support translating USB to NVMe/PCIe:

* ASMedia
  * [ASM2362][ASM2362]: USB 3.x Gen 2×1 to PCIe 3.x ×2
  * [ASM2364][ASM2364]: USB 3.x Gen 2×2 to PCIe 3.x ×4
  * [ASM2464PD][ASM2464PD]: USB4 Gen 3×2 / Thunderbolt 3 to PCIe 4.x ×4
* JMicron
  * [JMS581][JMS581]: USB 3.x Gen 2×1 to PCIe 3.x ×2 (NVMe) / SATA 3 / SD Express
  * [JMS583][JMS583]: USB 3.x Gen 2×1 to PCIe 3.x ×2 (NVMe)
  * [JMS586A][JMS586A]: USB 3.x Gen 2×2 to PCIe 3.x ×2 (NVMe) + PCIe 3.x ×2 (AHCI)
  * [JMS586U][JMS586U]: USB 3.x Gen 2×2 to PCIe 3.x ×2 (NVMe) + PCIe 3.x ×2 (NVMe/AHCI)
* Realtek
  * [RTL9210B-CG][RTL9210B]: USB 3.x Gen 2×1 to PCIe 3.x ×2 / SATA 3
  * [RTL9211DS-CG][RTL9211DS]: USB 3.x Gen 2×1 to PCIe 3.x ×2 / SD Express

This project will focus on the ASMedia controllers, for now.


## Sub-projects

* [ASM236x](ASM236x)
* [RTL921x](RTL921x)


## License

Except where otherwise stated:

* All software in this repository (e.g., tools for unpacking and generating
  firmware, etc.) is made available under the
  [GNU General Public License, version 3 or later][gpl].
* All copyrightable content that is not software (e.g., reverse engineering
  notes, this README file, etc.) is licensed under the
  [Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].


[ASM2362]: https://web.archive.org/web/20220608104342/https://www.asmedia.com.tw/product/Ee1YQF9sX7yyajH5/C5cYq34qpByQ6jm6
[ASM2364]: https://web.archive.org/web/20220703204756/https://www.asmedia.com.tw/product/BD5YqfdsPDqXFqi3/BF2yq24XzDuS5Tr4
[ASM2464PD]: https://web.archive.org/web/20231113020255/https://www.asmedia.com.tw/product/802zX91Yw3tsFgm4/C64ZX59yu4sY1GW5
[JMS581]: https://web.archive.org/web/20210511190218if_/https://www.jmicron.com/file/download/1081/Product+Brief+of+JMS581LT.pdf
[JMS583]: https://web.archive.org/web/20201218070451if_/https://www.jmicron.com/file/download/1012/JMS583_Product+Brief.pdf
[JMS586A]: https://web.archive.org/web/20220703210408if_/https://www.jmicron.com/file/download/1171/Product+Brief+of+JMS586A+%28Rev.1.00%29.pdf
[JMS586U]: https://web.archive.org/web/20220703210414if_/https://www.jmicron.com/file/download/1172/Product+Brief+of+JMS586U+%28Rev.1.00%29.pdf
[RTL9210B]: https://web.archive.org/web/20220407194447/https://www.realtek.com/en/products/communications-network-ics/item/rtl9210b-cg
[RTL9211DS]: https://web.archive.org/web/20230414021200/https://www.realtek.com/en/products/communications-network-ics/item/rtl9211ds-cg
[gpl]: COPYING.txt
[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
