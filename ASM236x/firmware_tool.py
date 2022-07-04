#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

# firmware_tool.py - A tool to parse ASM236x firmware image files.
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
import sys

try:
    import asm236x_fw
except ModuleNotFoundError:
    sys.stderr.write("Error: Failed to import \"asm236x_fw.py\". Please run \"make\" in this directory to generate that file, then try running this script again.\n")
    sys.exit(1)


def extract(filename, fw):
    split = filename.split('.')
    basename = '.'.join(split[:-1])
    f = open("{}.code.bin".format(basename), "wb")
    f.write(fw.body.firmware.code)
    f.close()

    return 0

def info(filename, fw):
    version_string = "{:02X}{:02X}{:02X}_{:02X}_{:02X}_{:02X}".format(*fw.body.firmware.version)
    print("Firmware version: {}".format(version_string))

    usb_ids = fw.header.usb_ids
    print("USB IDs: {:04x}:{:04x}".format(usb_ids.vid, usb_ids.pid))
    print("Image size: {} bytes".format(fw.body.size))

    return 0

def main():
    commands = {
        "extract": extract,
        "info": info,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=commands.keys(), help="Subcommands.")
    parser.add_argument("firmware", type=str, help="The firmware image file.")
    args = parser.parse_args()

    fw = asm236x_fw.Asm236xFw.from_file(args.firmware)
    return commands[args.command](args.firmware, fw)


if __name__ == "__main__":
    sys.exit(main())
