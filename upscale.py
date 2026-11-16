#!/usr/bin/env python3
# Upscale 1024x1024 FLUX output to 3072x3072 (9.4MP) JPEG q95 300dpi for stock minimums.
import sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
im = im.resize((3072, 3072), Image.LANCZOS)
im.save(dst, "JPEG", quality=95, dpi=(300, 300))
print(dst, im.size)
