#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

# rtl921x_tool.py - A tool to interact with RTL921x devices over USB.
# Copyright (C) 2023  Forest Crossman <cyrozap@gmail.com>
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


class Rtl921x:
    def __init__(self, dev_path):
        self._file = os.fdopen(os.open(dev_path, os.O_RDWR | os.O_NONBLOCK))

    def read(self, start_addr, read_len, stride=4096):
        data = bytearray(read_len)

        for i in range(0, read_len, stride):
            remaining = read_len - i
            buf_len = min(stride, remaining)

            cdb = struct.pack('<IIII', 0xe2, 0x92, start_addr + i, buf_len)

            buf = bytearray(buf_len)
            ret = sgio.execute(self._file, cdb, None, buf)
            assert ret == 0

            data[i:i+buf_len] = buf

        return bytes(data)

def info(args, dev):
    data = dev.read(0xac004000, 96)

    major, minor, patch = struct.unpack_from('<III', data, 0x4c)

    fw_date = struct.unpack_from('<I', data, 0x5c)[0]
    fw_day = fw_date % 100
    fw_month = (fw_date // 100) % 100
    fw_year = fw_date // 10000

    print("Firmware version: {:d}.{:d}.{:d}".format(major, minor, patch))
    print("Firmware date: {:04d}-{:02d}-{:02d}".format(fw_year, fw_month, fw_day))

    return 0

def read(args, dev):
    start_addr = int(args.address, 16)
    read_len = args.length
    stride = args.stride
    assert stride > 0

    output = None
    if args.output:
        output = open(args.output, 'wb')

    start_ns = time.perf_counter_ns()
    data = bytearray(read_len)
    for i in range(0, read_len, stride):
        remaining = read_len - i
        buf_len = min(stride, remaining)

        buf = dev.read(start_addr + i, buf_len, stride)

        if output:
            output.write(buf)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Read {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(data), elapsed/1e9, int(len(data)*1e9) // elapsed))

    if not args.quiet:
        print("MEM[0x{:04X}:0x{:04X}]: {} {}".format(start_addr, start_addr+read_len, data.hex(), data))

    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", default="/dev/sg0", help="The RTL921x SCSI/SG_IO device. Default: /dev/sg0")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands.")

    parser_info = subparsers.add_parser("info")
    parser_info.set_defaults(func=info)

    parser_read = subparsers.add_parser("read")
    parser_read.add_argument("-o", "--output", type=str, default=None, help="The file to write the memory to.")
    parser_read.add_argument("-q", "--quiet", action='store_true', default=False, help="Don't print memory contents. Default: False")
    parser_read.add_argument("-s", "--stride", type=int, default=4096, help="The number of bytes to read with each SCSI command. Min: 1, Max: Unknown, Default: 4096")
    parser_read.add_argument("-l", "--length", type=int, default=1, help="The total number of bytes to read. Default: 1")
    parser_read.add_argument("address", type=str, help="The address to start the read from, in hexadecimal.")
    parser_read.set_defaults(func=read)

    args = parser.parse_args()

    # Initialize the device object.
    dev = Rtl921x(args.device)

    return args.func(args, dev)


if __name__ == "__main__":
    sys.exit(main())
