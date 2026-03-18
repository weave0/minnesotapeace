"""
Convert Jamie's profile images to WebP format for better performance
Reduces file size by ~70% while maintaining quality
"""

from PIL import Image
import os


def convert_to_webp(input_path, output_path, quality=85):
    """Convert image to WebP format"""
    try:
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(
                    img, mask=img.split()[-1] if img.mode == "RGBA" else None
                )
                img = background

            # Save as WebP
            img.save(output_path, "WEBP", quality=quality, method=6)

            # Get file sizes
            original_size = os.path.getsize(input_path) / 1024  # KB
            webp_size = os.path.getsize(output_path) / 1024  # KB
            savings = ((original_size - webp_size) / original_size) * 100

            print(f"✓ {os.path.basename(input_path)} → {os.path.basename(output_path)}")
            print(f"  {original_size:.1f}KB → {webp_size:.1f}KB (saved {savings:.1f}%)")

            return True
    except Exception as e:
        print(f"✗ Error converting {input_path}: {e}")
        return False


if __name__ == "__main__":
    images_dir = "assets/images"

    images_to_convert = [
        "Jamie Profile Square.png",
        "Jamie Profile.png",
        "hero-bg.png",
        "process.png",
    ]

    print("Converting images to WebP format...\n")

    success_count = 0
    for img_name in images_to_convert:
        input_path = os.path.join(images_dir, img_name)
        output_path = os.path.join(images_dir, img_name.replace(".png", ".webp"))

        if os.path.exists(input_path):
            if convert_to_webp(input_path, output_path):
                success_count += 1
        else:
            print(f"⚠ Skipping {img_name} (not found)")

    print(f"\n✓ Converted {success_count}/{len(images_to_convert)} images successfully")
