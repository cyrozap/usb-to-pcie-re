#!/bin/bash
# SPDX-License-Identifier: 0BSD

# Copyright (C) 2022-2024 by Forest Crossman <cyrozap@gmail.com>
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


# ASM236x
wget \
	--directory-prefix downloads \
	--content-disposition \
	--user-agent "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36" \
	--input-file urls.txt

# ASM2464
curl -o downloads/JEYI2464_0525.zip https://web.archive.org/web/20231223011853if_/https://cdn.shoplazza.com/3d54d7ae5536d23a120f31065eed2b57.zip
curl -o downloads/JEYI2464_0810_10min.zip https://web.archive.org/web/20231223011833if_/https://cdn.shoplazza.com/4788ee7e011b6f00f2c5f648c802f746.zip
curl -o downloads/JEYI2464_1005_10Min.zip https://web.archive.org/web/20231223011831if_/https://cdn.shoplazza.com/e5816cde2955976ba163965bd067124d.zip
curl -o downloads/ASM2464PD_FW_231218_85_00_00.zip https://web.archive.org/web/20240312061204if_/https://cdn.shoplazza.com/71af6d849f082e2d2e399a33110accb3.zip
curl -o "downloads/40d1b2d8asmedia_ASM2464PD_FW_240129_85_00_00(station-drivers.com).zip" "https://web.archive.org/web/20240312061826if_/https://www.station-drivers.com/index.php/en-us/component/remository/func-download/6080/chk,8713266a78315cc8f0f436a69ad14eb5/no_html,1/lang,en-us/"
