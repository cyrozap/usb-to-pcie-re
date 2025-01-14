#!/usr/bin/env python3
# SPDX-License-Identifier: 0BSD

# Copyright (C) 2023, 2025 by Forest Crossman <cyrozap@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.


import struct


BRIGHTNESS = 255
HOLD_TIME = 0
TRANSITION_TIME = 2

#LEVELS = (0, 0, 0, 255)
#LEVELS = (0x00, 0x55, 0xaa, 0xff)
#LEVELS = (0, 22, 61, 255)
LEVELS = (0, 28, 113, 255)
#LEVELS = (0, 0, 17, 255)

LEVEL_PATTERNS = (
    (LEVELS[3], LEVELS[2], LEVELS[1], LEVELS[0]),
    (LEVELS[2], LEVELS[3], LEVELS[2], LEVELS[1]),
)


def main():
    for i in range(4):
        if i < 2:
            pattern = LEVEL_PATTERNS[i] + LEVEL_PATTERNS[i][::-1]
        else:
            pattern = LEVEL_PATTERNS[3-i][::-1] + LEVEL_PATTERNS[3-i]

        red = 255
        green = 0
        blue = 0
        pattern = [((red << 24) | (green << 16) | (blue << 8) | brightness) for brightness in pattern]

        # Command format:
        # - Command: 0xD2
        # - Magic: "SetLed"
        # - LED index: 2-5
        # - I2C mode (?): 0x21
        # - Padding byte: 0
        # - Data size: 39 bytes
        # - Padding bytes: Five null bytes
        #
        # Data format:
        # - Mode: Custom (0x04)
        # - Global brightness: 0-255
        # - Number of states for the LED: 1-8
        # - State hold time (tenths of one second): 0-255
        # - Padding byte: 0
        # - State transition time (tenths of one second): 0-255
        # - LED states (1-8):
        #   - Red: 0-255
        #   - Green: 0-255
        #   - Blue: 0-255
        #   - Brightness: 0-255
        print("echo {} | xxd -r -ps | sg_raw -s 39 /dev/sg0 d2 53 65 74 4c 65 64 {:02x} 21 00 27 00 00 00 00 00".format(
            struct.pack('>BBBBxBxIIIIIIII', 4, BRIGHTNESS, 8, HOLD_TIME, TRANSITION_TIME, *pattern).hex(), 2+i))


if __name__ == "__main__":
    main()
