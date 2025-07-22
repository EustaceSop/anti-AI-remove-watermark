import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import hashlib
from tkinter import Tk, filedialog
import os

def add_protective_watermark(
    image_path,
    output_path,
    watermark_text="© GayBottle",
    font_path="arial.ttf",
    font_size=80,
    alpha=0.2,
    hash_id="CustomID-001"
):
    base = Image.open(image_path).convert("RGBA")
    width, height = base.size
    
    watermark = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    for i in range(-height, width, int(text_width * 2)):
        draw.text((i, i), watermark_text, font=font, fill=(255, 255, 255, int(255 * alpha)))

    watermarked = Image.alpha_composite(base, watermark)

    sha256 = hashlib.sha256(hash_id.encode()).digest()
    img_np = np.array(watermarked.convert("RGB"))
    for i in range(len(sha256)):
        y = i % height
        x = (i * 37) % width
        img_np[y, x, 2] ^= sha256[i]

    noise = np.random.randint(0, 10, (height, width), dtype='uint8')
    for c in range(3):
        img_np[:, :, c] = cv2.add(img_np[:, :, c], noise)

    Image.fromarray(img_np).save(output_path)
    print(f"saved to：{output_path}")

if __name__ == "__main__":
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="choose one（JPG/PNG）")

    if not file_path:
        print("nigger just choose one")
    else:
        out_path = os.path.join(os.path.dirname(__file__), "protected.png")
        add_protective_watermark(
            image_path=file_path,
            output_path=out_path,
            watermark_text="by GayBottle",
            font_path="arial.ttf",
            font_size=100,
            alpha=0.18,
            hash_id="GayBottle-v2"
        )