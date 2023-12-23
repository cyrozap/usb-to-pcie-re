#!/bin/bash
# SPDX-License-Identifier: 0BSD

# Copyright (C) 2023 by Forest Crossman <cyrozap@gmail.com>
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


wget \
	--directory-prefix downloads \
	--content-disposition \
	--input-file urls.txt

curl -o downloads/JEYI_TFT-ScreenTFT显示屏-黑豹.zip https://web.archive.org/web/20231223012213if_/https://cdn.shoplazza.com/2dcf436d7b82d3b29b2ba0e1456bf083.zip
curl -o downloads/JEYI_With_Screen带显示屏i9x[1].zip https://web.archive.org/web/20231223013545if_/https://cdn.shoplazza.com/fa7dd28e3727765b4c29e90a9f677d0f.zip
