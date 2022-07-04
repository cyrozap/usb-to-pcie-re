# USB to PCIe Reverse Engineering


## Introduction

There are several chips on the market that support translating USB to NVMe/PCIe:

* ASMedia
  * [ASM2362][ASM2362]: USB 3.x Gen 2×1 to PCIe 3.x ×2
  * [ASM2364][ASM2364]: USB 3.x Gen 2×2 to PCIe 3.x ×4
* JMicron
  * [JMS583][JMS583]: USB 3.x Gen 2×1 to PCIe 3.x ×2 (NVMe)
  * [JMS586A][JMS586A]: USB 3.x Gen 2×2 to PCIe 3.x ×2 (NVMe) + PCIe 3.x ×2 (AHCI)
  * [JMS586U][JMS586U]: USB 3.x Gen 2×2 to PCIe 3.x ×2 (NVMe) + PCIe 3.x ×2 (NVMe/AHCI)
* Realtek
  * [RTL9210B-CG][RTL9210B]: USB 3.x Gen 2×1 to PCIe 3.x ×2 / SATA 3

This project will focus on the ASMedia controllers, for now.


## Quick start

### Software dependencies

* Python 3
* [Kaitai Struct Compiler][ksc]
* [Kaitai Struct Python Runtime][kspr]

### Procedure

1. Install dependencies.
2. Run `make` to generate the parser code used by `firmware_tool.py`.
3. Run `./firmware_tool.py` on the `*.hex` firmware update file.


## Reverse engineering notes

See [ASM236x/Notes.md](ASM236x/Notes.md).


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
[JMS583]: https://web.archive.org/web/20201218070451if_/https://www.jmicron.com/file/download/1012/JMS583_Product+Brief.pdf
[JMS586A]: https://web.archive.org/web/20220703210408if_/https://www.jmicron.com/file/download/1171/Product+Brief+of+JMS586A+%28Rev.1.00%29.pdf
[JMS586U]: https://web.archive.org/web/20220703210414if_/https://www.jmicron.com/file/download/1172/Product+Brief+of+JMS586U+%28Rev.1.00%29.pdf
[RTL9210B]: https://web.archive.org/web/20220407194447/https://www.realtek.com/en/products/communications-network-ics/item/rtl9210b-cg
[ksc]: https://github.com/kaitai-io/kaitai_struct_compiler
[kspr]: https://github.com/kaitai-io/kaitai_struct_python_runtime
[gpl]: COPYING.txt
[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
