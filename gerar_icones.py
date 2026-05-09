import os
from PIL import Image, ImageDraw, ImageFont

def criar_icone(size):
    img  = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    navy   = (10, 26, 47, 255)
    ciano  = (0, 229, 255, 255)
    branco = (255, 255, 255, 255)
    cx, cy = size // 2, size // 2
    r = int(size * 0.48)

    # Círculo fundo + borda
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=navy)
    bw = max(2, size//80)
    draw.ellipse([cx-r-bw, cy-r-bw, cx+r+bw, cy+r+bw], outline=ciano, width=bw)

    # Fonte
    fs = max(10, int(size * 0.38))
    try:    font = ImageFont.truetype("arialbd.ttf", fs)
    except:
        try: font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", fs)
        except: font = ImageFont.load_default()

    # Separador
    sep_y = cy + int(size * 0.03)
    draw.line([cx-int(r*0.68), sep_y, cx+int(r*0.68), sep_y], fill=ciano, width=max(1, size//150))

    # GEL acima do separador
    b1  = draw.textbbox((0,0), "GEL", font=font)
    tw1 = b1[2]-b1[0]; th1 = b1[3]-b1[1]
    or_ = int(th1 * 0.44)
    gap = int(size * 0.03)
    total_w = tw1 + gap + or_*2
    tx1 = cx - total_w//2
    ty1 = sep_y - th1 - int(size*0.05)
    draw.text((tx1, ty1), "GEL", font=font, fill=branco)

    # Floco O
    ox = tx1 + tw1 + gap + or_
    oy = ty1 + th1//2
    lw = max(1, size//100)
    draw.ellipse([ox-or_, oy-or_, ox+or_, oy+or_], outline=branco, width=max(2, size//90))
    draw.line([ox, oy-or_+2, ox, oy+or_-2], fill=ciano, width=lw)
    draw.line([ox-or_+2, oy, ox+or_-2, oy], fill=ciano, width=lw)
    d = int(or_*0.64)
    draw.line([ox-d, oy-d, ox+d, oy+d], fill=ciano, width=lw)
    draw.line([ox+d, oy-d, ox-d, oy+d], fill=ciano, width=lw)
    pr = max(2, size//100)
    draw.ellipse([ox-pr, oy-pr, ox+pr, oy+pr], fill=ciano)

    # CRIM abaixo do separador
    b2  = draw.textbbox((0,0), "CRIM", font=font)
    tw2 = b2[2]-b2[0]; th2 = b2[3]-b2[1]
    ty2 = sep_y + int(size*0.04)
    tx2 = cx - tw2//2
    draw.text((tx2, ty2), "CRIM", font=font, fill=branco)

    return img

sizes = [
    (192, r'C:\gelocrim-motorista\android\app\src\main\res\mipmap-xxxhdpi'),
    (144, r'C:\gelocrim-motorista\android\app\src\main\res\mipmap-xxhdpi'),
    (96,  r'C:\gelocrim-motorista\android\app\src\main\res\mipmap-xhdpi'),
    (72,  r'C:\gelocrim-motorista\android\app\src\main\res\mipmap-hdpi'),
    (48,  r'C:\gelocrim-motorista\android\app\src\main\res\mipmap-mdpi'),
]

for size, folder in sizes:
    os.makedirs(folder, exist_ok=True)
    img = criar_icone(size)
    img.save(os.path.join(folder, 'ic_launcher.png'))
    img.save(os.path.join(folder, 'ic_launcher_round.png'))
    print(f'OK {size}x{size}')

print('\nIcones gerados! Recompile o APK.')
