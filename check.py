from PIL import Image
import os

image_dir = "./DATASET/nnUNet_raw/Dataset110_TongueSegmentation/imagesTr"
for filename in os.listdir(image_dir):
    if filename.endswith(".png"):
        img = Image.open(os.path.join(image_dir, filename))
        print(f"{filename}: {img.mode} ({img.size})")