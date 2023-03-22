#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

# asm236x_tool.py - A tool to interact with ASM236x devices over USB.
# Copyright (C) 2022-2023  Forest Crossman <cyrozap@gmail.com>
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

    def flash_dump(self, read_len):
        data = bytearray(read_len)

        cdb = struct.pack('>BBI', 0xe2, 0x00, read_len)

        ret = sgio.execute(self._file, cdb, None, data)
        assert ret == 0

        return bytes(data)

    def fw_write(self, fw_data):
        cdb = struct.pack('>BBI', 0xe3, 0x00, len(fw_data))

        ret = sgio.execute(self._file, cdb, fw_data, None)
        assert ret == 0

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

    def reload(self):
        cdb = bytes.fromhex("e8 00 00 00 00 00 00 00 00 00 00 00")
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

def flash_dump(args, dev):
    read_len = args.length

    start_ns = time.perf_counter_ns()
    data = dev.flash_dump(read_len)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Read {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(data), elapsed/1e9, int(len(data)*1e9) // elapsed))

    open(args.flash_dump_file, 'wb').write(data)

    return 0

def fw_write(args, dev):
    fw_file = open(args.fw_file, 'rb').read()

    fw_data = fw_file
    if not args.raw:
        fw_data = fw_file[0x80:]

    fw_size = struct.unpack_from('<H', fw_data, 0)[0]
    fw_data = fw_data[:fw_size+8]
    fw_magic = fw_data[2+fw_size+0]
    if fw_magic not in (0x4b, 0x5a):
        print("Error: Bad FW magic. Expected 0x4b or 0x5a, got 0x{:02x}.".format(fw_magic))
        return 1
    fw_checksum_calc = sum(fw_data[2:2+fw_size]) & 0xff
    fw_checksum = fw_data[2+fw_size+1]
    if fw_checksum_calc != fw_checksum:
        print("Error: Bad FW checksum. Expected 0x{:02x}, calculated 0x{:02x}.".format(fw_checksum, fw_checksum_calc))
        return 1

    start_ns = time.perf_counter_ns()
    data = dev.fw_write(fw_data)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Wrote {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(fw_data), elapsed/1e9, int(len(fw_data)*1e9) // elapsed))

    start_ns = time.perf_counter_ns()
    rb_data = dev.flash_dump(0x80 + len(fw_data))
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Read back {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(rb_data), elapsed/1e9, int(len(rb_data)*1e9) // elapsed))

    errors = 0
    for i in range(len(fw_data)):
        rb_byte = rb_data[0x80:][i]
        fw_byte = fw_data[i]
        if rb_byte != fw_byte:
            errors += 1
            print("Error: Bad data at flash address 0x{:08x} (firmware offset 0x{:08x}): Expected 0x{:02x}, read 0x{:02x}.".format(0x80 + i, i, fw_byte, rb_byte))

    if errors > 0:
        print("Error: Verification failed with {} errors!".format(errors))
        return 1

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
    data = b"".join([bytes.fromhex(x) for x in args.data])

    if args.read_before:
        read_len = len(data)
        stride = min(read_len, 255)
        start_ns = time.perf_counter_ns()
        read_data = dev.read(start_addr, read_len, stride)
        end_ns = time.perf_counter_ns()
        elapsed = end_ns - start_ns
        print("Read {} bytes in {:.6f} seconds ({} bytes per second).".format(
            len(read_data), elapsed/1e9, int(len(read_data)*1e9) // elapsed))

        print("XDATA[0x{:04X}:0x{:04X}]: {} {}".format(
            start_addr, start_addr+read_len, read_data.hex(), read_data))

    start_ns = time.perf_counter_ns()
    dev.write(start_addr, data)
    end_ns = time.perf_counter_ns()
    elapsed = end_ns - start_ns
    print("Wrote {} bytes in {:.6f} seconds ({} bytes per second).".format(
        len(data), elapsed/1e9, int(len(data)*1e9) // elapsed))

    print("XDATA[0x{:04X}:0x{:04X}]: {} {}".format(start_addr, start_addr+len(data), data.hex(), data))

    if args.read_after:
        read_len = len(data)
        stride = min(read_len, 255)
        start_ns = time.perf_counter_ns()
        read_data = dev.read(start_addr, read_len, stride)
        end_ns = time.perf_counter_ns()
        elapsed = end_ns - start_ns
        print("Read {} bytes in {:.6f} seconds ({} bytes per second).".format(
            len(read_data), elapsed/1e9, int(len(read_data)*1e9) // elapsed))

        print("XDATA[0x{:04X}:0x{:04X}]: {} {}".format(
            start_addr, start_addr+read_len, read_data.hex(), read_data))

    return 0

def reload(args, dev):
    dev.reload()

    return 0

def memtest(args, dev):
    start_addr = int(args.address, 16)
    test_len = args.length
    stride = args.stride

    print("Testing data from 0x{:04x} to 0x{:04x}, inclusive...".format(start_addr, start_addr+test_len-1))

    zeros = bytes(test_len)

    tests = (
        ("Random 1", os.urandom(test_len)),
        ("Zeros 1", zeros),
        ("Random 2", os.urandom(test_len)),
        ("Zeros 2", zeros),
    )

    for test_name, test_data in tests:
        print("Running test \"{}\"...".format(test_name))

        before = dev.read(start_addr, test_len, stride)
        dev.write(start_addr, test_data)
        after = dev.read(start_addr, test_len, stride)

        if after != test_data:
            print("Error: Failed test \"{}\"!".format(test_name))
            for i in range(test_len):
                if after[i] != test_data[i]:
                    print(" + Mismatch at address 0x{:04x}: Expected 0x{:02x}, got 0x{:02x} instead.".format(
                        start_addr + i, test_data[i], after[i]))
                    break

            if after == before:
                print(" + Write had no effect--this is likely read-only memory.")

            return 1

    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", default="/dev/sg0", help="The SCSI/SG_IO device. Default: /dev/sg0")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands.")

    parser_dump = subparsers.add_parser("dump")
    parser_dump.add_argument("dump_file", help="The file to write the memory dump output to.")
    parser_dump.set_defaults(func=dump)

    parser_flash_dump = subparsers.add_parser("flash_dump")
    parser_flash_dump.add_argument("-l", "--length", type=int, default=512*1024, help="The total number of bytes to read from flash. Default: 524288")
    parser_flash_dump.add_argument("flash_dump_file", help="The file to write the flash dump output to.")
    parser_flash_dump.set_defaults(func=flash_dump)

    parser_fw_write = subparsers.add_parser("fw_write")
    parser_fw_write.add_argument("-r", "--raw", action='store_true', default=False, help="Write raw flash data, not a parsed firmware image. Default: False")
    parser_fw_write.add_argument("fw_file", help="The firmware file to write to flash.")
    parser_fw_write.set_defaults(func=fw_write)

    parser_info = subparsers.add_parser("info")
    parser_info.set_defaults(func=info)

    parser_read = subparsers.add_parser("read")
    parser_read.add_argument("-s", "--stride", type=int, default=255, help="The number of bytes to read with each SCSI command. Min: 1, Max: 255, Default: 255")
    parser_read.add_argument("-l", "--length", type=int, default=1, help="The total number of bytes to read. Default: 1")
    parser_read.add_argument("address", type=str, help="The address to start the read from, in hexadecimal.")
    parser_read.set_defaults(func=read)

    parser_write = subparsers.add_parser("write")
    parser_write.add_argument("-b", "--read-before", action='store_true', default=False, help="Perform a read before writing. Default: False")
    parser_write.add_argument("-a", "--read-after", action='store_true', default=False, help="Perform a read after writing. Default: False")
    parser_write.add_argument("address", type=str, help="The address to start the write to, in hexadecimal.")
    parser_write.add_argument("data", type=str, nargs="+", help="The data bytes to be written, in hexadecimal.")
    parser_write.set_defaults(func=write)

    parser_reload = subparsers.add_parser("reload")
    parser_reload.set_defaults(func=reload)

    parser_memtest = subparsers.add_parser("memtest")
    parser_memtest.add_argument("-s", "--stride", type=int, default=1, help="The number of bytes to read with each SCSI command. Min: 1, Max: 255, Default: 1")
    parser_memtest.add_argument("address", type=str, help="The address to start the test from, in hexadecimal.")
    parser_memtest.add_argument("length", type=int, default=1, help="The total number of bytes to test. Default: 1")
    parser_memtest.set_defaults(func=memtest)

    args = parser.parse_args()

    # Initialize the device object.
    dev = Asm236x(args.device)

    return args.func(args, dev)


if __name__ == "__main__":
    sys.exit(main())
