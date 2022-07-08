#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

# asm236x_tool.py - A tool to interact with ASM236x devices over USB.
# Copyright (C) 2022  Forest Crossman <cyrozap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import os
import struct
import sys
import time

try:
    import sgio
except ModuleNotFoundError:
    sys.stderr.write("Error: Failed to import \"sgio\". Please install \"cython-sgio\", then try running this script again.\n")
    sys.exit(1)


class Asm236x:
    def __init__(self, dev_path):
        self._file = os.fdopen(os.open(dev_path, os.O_RDWR | os.O_NONBLOCK))

    def read(self, start_addr, read_len, stride=255):
        data = bytearray(read_len)

        for i in range(0, read_len, stride):
            remaining = read_len - i
            buf_len = min(stride, remaining)

            cdb = struct.pack('>BBBHB', 0xe4, buf_len, 0x00, start_addr + i, 0x00)

            buf = bytearray(buf_len)
            ret = sgio.execute(self._file, cdb, None, buf)
            assert ret == 0

            data[i:i+buf_len] = buf

        return bytes(data)

    def write(self, start_addr, data):
        for offset, value in enumerate(data):
            cdb = struct.pack('>BBBHB', 0xe5, value, 0x00, start_addr + offset, 0x00)
            ret = sgio.execute(self._file, cdb, None, None)
            assert ret == 0

    def get_fw_version_data(self):
        return self.read(0x07f0, 6)


def fw_version_bytes_to_string(version):
    return "{:02X}{:02X}{:02X}_{:02X}_{:02X}_{:02X}".format(*version)

def dump(args, dev):
    start_addr = 0x0000
    read_len = 1 << 16
    stride = 128

    start_ns = time.perf_counter_ns()
    data = dev.read(start_addr, read_len, stride)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Read {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(data), elapsed/1e9, int(len(data)*1e9) // elapsed))

    open(args.dump_file, 'wb').write(data)

    return 0

def info(args, dev):
    print("Firmware version: {}".format(fw_version_bytes_to_string(dev.get_fw_version_data())))

    return 0

def read(args, dev):
    start_addr = int(args.address, 16)
    read_len = args.length
    stride = args.stride
    assert stride > 0
    assert stride < 256

    start_ns = time.perf_counter_ns()
    data = dev.read(start_addr, read_len, stride)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Read {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(data), elapsed/1e9, int(len(data)*1e9) // elapsed))

    print("XDATA[0x{:04X}:0x{:04X}]: {} {}".format(start_addr, start_addr+read_len, data.hex(), data))

    return 0

def write(args, dev):
    start_addr = int(args.address, 16)
    data = bytes.fromhex("".join(args.data).replace(" ", ""))

    start_ns = time.perf_counter_ns()
    dev.write(start_addr, data)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Wrote {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(data), elapsed/1e9, int(len(data)*1e9) // elapsed))

    print("XDATA[0x{:04X}:0x{:04X}]: {} {}".format(start_addr, start_addr+len(data), data.hex(), data))

    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", default="/dev/sg0", help="The SCSI/SG_IO device. Default: /dev/sg0")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands.")

    parser_dump = subparsers.add_parser("dump")
    parser_dump.add_argument("dump_file", help="The file to write the memory dump output to.")
    parser_dump.set_defaults(func=dump)

    parser_info = subparsers.add_parser("info")
    parser_info.set_defaults(func=info)

    parser_read = subparsers.add_parser("read")
    parser_read.add_argument("-s", "--stride", type=int, default=255, help="The number of bytes to read with each SCSI command. Min: 1, Max: 255, Default: 255")
    parser_read.add_argument("-l", "--length", type=int, default=1, help="The total number of bytes to read. Default: 1")
    parser_read.add_argument("address", type=str, help="The address to start the read from, in hexadecimal.")
    parser_read.set_defaults(func=read)

    parser_write = subparsers.add_parser("write")
    parser_write.add_argument("address", type=str, help="The address to start the write to, in hexadecimal.")
    parser_write.add_argument("data", type=str, nargs="+", help="The data bytes to be written, in hexadecimal.")
    parser_write.set_defaults(func=write)

    args = parser.parse_args()

    # Initialize the device object.
    dev = Asm236x(args.device)

    return args.func(args, dev)


if __name__ == "__main__":
    sys.exit(main())
