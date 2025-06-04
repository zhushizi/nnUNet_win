import os
import cv2
import numpy as np
from tqdm import tqdm  # 用于显示进度条


def convert_binary_image(image):
    """将二值图像中的1转换为255"""
    # 创建副本避免修改原始数据
    converted = image.copy()
    converted[converted == 1] = 255
    return converted


def process_folder(input_folder, output_folder):
    """
    批量处理文件夹中的所有PNG图像
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 获取所有PNG文件
    png_files = [f for f in os.listdir(input_folder)
                 if f.lower().endswith('.png')]

    print(f"找到 {len(png_files)} 个PNG文件需要处理")

    # 处理每个文件
    for filename in tqdm(png_files, desc="处理图像"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 读取图像（灰度模式）
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"警告: 无法读取图像 {filename}，跳过")
            continue

        # 转换图像
        converted_img = convert_binary_image(img)

        # 保存结果
        cv2.imwrite(output_path, converted_img)


if __name__ == "__main__":
    # 配置输入和输出文件夹
    input_folder = r"DATASET/nnUNet_raw/Dataset110_TongueSegmentation/labelsTs_pred"  # 替换为你的输入文件夹路径
    output_folder = r"DATASET/nnUNet_raw/Dataset110_TongueSegmentation/labelsTs_pred_255"  # 替换为你的输出文件夹路径

    # 处理文件夹
    process_folder(input_folder, output_folder)

    print(f"\n处理完成！结果已保存到: {output_folder}")