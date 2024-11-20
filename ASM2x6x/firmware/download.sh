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
	--directory-prefix downloads/ASM236x \
	--content-disposition \
	--user-agent "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36" \
	--input-file urls.txt

# ASM2464
curl -o downloads/ASM246x/JEYI2464_0525.zip https://web.archive.org/web/20231223011853if_/https://cdn.shoplazza.com/3d54d7ae5536d23a120f31065eed2b57.zip
curl -o downloads/ASM246x/JEYI2464_0810_10min.zip https://web.archive.org/web/20231223011833if_/https://cdn.shoplazza.com/4788ee7e011b6f00f2c5f648c802f746.zip
curl -o downloads/ASM246x/JEYI2464_1005_10Min.zip https://web.archive.org/web/20231223011831if_/https://cdn.shoplazza.com/e5816cde2955976ba163965bd067124d.zip
curl -o downloads/ASM246x/ASM2464PD_FW_231218_85_00_00.zip https://web.archive.org/web/20240312061204if_/https://cdn.shoplazza.com/71af6d849f082e2d2e399a33110accb3.zip
curl -o "downloads/ASM246x/JEYI2464_0525(station-drivers.com).zip" "https://web.archive.org/web/20240406174638if_/https://www.station-drivers.com/download/Realtek/JEYI2464_0525(station-drivers.com).zip"
curl -o "downloads/ASM246x/40d1b2d8asmedia_asm2464_230810_85_00_00(station-drivers.com).zip" "https://web.archive.org/web/20240406174651if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/5988/chk,c5c53c1bbb49b8af1fecb852f1ae5926/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/40d1b2d8asmedia_asm2464_230810_85.00.00(station-drivers.com).zip" "https://web.archive.org/web/20240406174902if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/5987/chk,71f4f6db0927fc7fa5fc61c675f489da/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/40d1b2d8asmedia_ASM246x_231005.85.01.06(station-drivers.com).zip" "https://web.archive.org/web/20240406174824if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/6118/chk,70c46f029ff9766599724c3f7342c9f3/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/asmedia_asm2464_231204(station-drivers.com).zip" "https://web.archive.org/web/20240406175016if_/https://www.station-drivers.com/download/asmedia/asmedia_asm2464_231204(station-drivers.com).zip"
curl -o "downloads/ASM246x/40d1b2d8ASM246xMPTool_v1.0.3.8(station-drivers.com).zip" "https://web.archive.org/web/20240406174753if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/5990/chk,60f7f0cdb8d7168ae1ab399447559ff3/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/40d1b2d8Asmedia_ASM2464_240129_84_06_06(station-drivers.com).zip" "https://web.archive.org/web/20240406175025if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/6113/chk,d1ca0194a0226fcd5202a7af3c6af9c2/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/40d1b2d8asmedia_ASM2464PD_FW_240129_85_00_00(station-drivers.com).zip" "https://web.archive.org/web/20240406175112if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/6080/chk,b5e36774fb2b6384488cd5717e7be251/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/40d1b2d8asmedia_ASM2464_240229_85_00_00(station-drivers.com).zip" "https://web.archive.org/web/20240406173459if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/6106/chk,c7393edd3671753eaf5fb109efdd4281/no_html,1/lang,en-gb/"
curl -o "downloads/ASM246x/40d1b2d8asmedia_asm2464_240229_85_00_00bis(station-drivers.zip" "https://web.archive.org/web/20240406174814if_/https://www.station-drivers.com/index.php/en/component/remository/func-download/6117/chk,5f8d9415da037b189d86ed399891eb9b/no_html,1/lang,en-gb/"
wget --directory-prefix downloads/ASM246x https://web.archive.org/web/20241120025326if_/https://www.adt.link/download/ADT_UT3G_ASM246xMPTool.zip
