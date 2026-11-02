#!/usr/bin/env python3
"""Une dos imágenes (antes y después) en un lienzo listo para reel o carrusel.

Uso:
    python componer.py antes.png despues.png --out comparacion.png [--formato reel|carrusel|horizontal]

reel        → 1080x1920, antes arriba y después abajo
carrusel    → 1080x1350, antes arriba y después abajo
horizontal  → lado a lado, alto 1080

Cada imagen se ajusta a su mitad sin deformarse; el sobrante se rellena con el color de --fondo.
Requisito: pip install pillow
"""
import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow: pip install pillow")

FORMATOS = {"reel": (1080, 1920, "v"), "carrusel": (1080, 1350, "v"), "horizontal": (2160, 1080, "h")}


def encajar(im, w, h, fondo):
    im = im.copy()
    im.thumbnail((w, h), Image.LANCZOS)
    lienzo = Image.new("RGB", (w, h), fondo)
    lienzo.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return lienzo


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("antes")
    ap.add_argument("despues")
    ap.add_argument("--out", required=True)
    ap.add_argument("--formato", choices=FORMATOS, default="reel")
    ap.add_argument("--fondo", default="#F4F2F5", help="color de relleno (hex)")
    ap.add_argument("--separacion", type=int, default=12)
    a = ap.parse_args()

    W, H, eje = FORMATOS[a.formato]
    s = a.separacion
    lienzo = Image.new("RGB", (W, H), a.fondo)
    ims = [Image.open(p).convert("RGB") for p in (a.antes, a.despues)]
    if eje == "v":
        mh = (H - s) // 2
        lienzo.paste(encajar(ims[0], W, mh, a.fondo), (0, 0))
        lienzo.paste(encajar(ims[1], W, mh, a.fondo), (0, mh + s))
    else:
        mw = (W - s) // 2
        lienzo.paste(encajar(ims[0], mw, H, a.fondo), (0, 0))
        lienzo.paste(encajar(ims[1], mw, H, a.fondo), (mw + s, 0))
    lienzo.save(a.out)
    print(f"✓ {a.out} ({W}x{H})")


if __name__ == "__main__":
    main()
