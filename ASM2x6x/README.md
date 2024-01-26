# ASM236x Reverse Engineering


## Quick start


### Software dependencies

* Python 3
* Firmware image parser:
  * [Kaitai Struct Compiler][ksc]
  * [Kaitai Struct Python Runtime][kspr]
* `tools/asm236x_tool.py`:
  * [cython-sgio][cython-sgio]


### Procedure

1. `cd` to the `tools` directory.
2. Install dependencies.
3. Run `make` to generate the parser code used by `firmware_tool.py`.
4. Run `./firmware_tool.py` on the `*.bin` firmware binary.


## Reverse engineering notes

See [doc/Notes.md](doc/Notes.md).


[ksc]: https://github.com/kaitai-io/kaitai_struct_compiler
[kspr]: https://github.com/kaitai-io/kaitai_struct_python_runtime
[cython-sgio]: https://pypi.org/project/cython-sgio/
