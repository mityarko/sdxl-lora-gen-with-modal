import os
import sys

from PIL import Image

def resize_images_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as img:
                # いったん 1024x1024 に入るように変換
                # この時点では縦横比が変わらないため、余白があるので埋める
                img.thumbnail((1024, 1024))

                # 新しい空の画像を作成して、中央に画像を貼り付ける
                w, h = img.size
                if w == h:
                    img.save(image_path)
                elif w > h:
                    new_img = Image.new(img.mode, (w, w))
                    new_img.paste(img, (0, (w - h) // 2))
                    new_img.save(image_path)
                else:
                    new_img = Image.new(img.mode, (h, h))
                    new_img.paste(img, ((h - w) // 2, 0))
                    new_img.save(image_path)
                print(f"Resized {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resizer.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    resize_images_in_folder(folder_path)
