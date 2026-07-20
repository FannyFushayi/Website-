from PIL import Image
from pathlib import Path

def make_landscape(image_paths, out_path, target_height=None, bg_color=(255,255,255)):
    imgs = [Image.open(p).convert('RGB') for p in image_paths]
    if target_height is None:
        target_height = min(i.height for i in imgs)
    resized = []
    for im in imgs:
        w, h = im.size
        new_w = int(w * (target_height / h))
        resized.append(im.resize((new_w, target_height), Image.LANCZOS))

    total_w = sum(i.width for i in resized)
    out = Image.new('RGB', (total_w, target_height), color=bg_color)
    x = 0
    for im in resized:
        out.paste(im, (x, 0))
        x += im.width

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path, quality=90)
    print(f"Saved composite to {out_path}")

if __name__ == '__main__':
    base = Path(__file__).resolve().parents[1]
    imgs = [
        base / 'Images' / 'MyWorks' / 'IMG_0693.JPEG',
        base / 'Images' / 'MyWorks' / 'Snapseed.JPEG',
        base / 'Images' / 'MyWorks' / 'IMG_1173.JPEG',
    ]
    out = base / 'Images' / 'MyWorks' / 'landscape_composite.jpg'
    make_landscape(imgs, out, target_height=900)
