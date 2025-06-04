import os
from PIL import Image


def convert_images(folder_path):
    """
    检测并转换文件夹中的图片：
    1. 将4通道RGBA图片转换为RGB三通道
    2. 将非PNG格式图片转换为PNG格式
    """
    # 支持的图片格式
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')

    print("开始检测图片转换需求...\n")
    conversion_log = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # 跳过子目录和非图片文件
        if not os.path.isfile(filepath):
            continue
        if not filename.lower().endswith(image_extensions):
            continue

        try:
            with Image.open(filepath) as img:
                reasons = []
                output_path = filepath

                # 检测并处理4通道图片
                if img.mode == 'RGBA':
                    reasons.append("4通道RGBA图片")
                    img = img.convert('RGB')

                # 检测并处理非PNG格式
                base_name, ext = os.path.splitext(filename)
                if ext.lower() != '.png':
                    reasons.append(f"非PNG格式({ext})")
                    output_path = os.path.join(folder_path, base_name + '.png')

                # 如果需要转换
                if reasons:
                    # 保存转换后的图片
                    img.save(output_path)

                    # 删除原始非PNG文件（如果是格式转换）
                    if output_path != filepath:
                        os.remove(filepath)

                    # 记录转换信息
                    conversion_log.append({
                        'filename': filename,
                        'reasons': reasons,
                        'new_name': os.path.basename(output_path) if output_path != filepath else None
                    })

        except Exception as e:
            print(f"处理图片 {filename} 时出错: {str(e)}")

    # 打印转换结果
    if conversion_log:
        print("\n转换完成！以下图片已被处理：")
        for item in conversion_log:
            new_name_info = f" -> 重命名为: {item['new_name']}" if item['new_name'] else ""
            print(f"- {item['filename']}: {', '.join(item['reasons'])}{new_name_info}")
    else:
        print("\n没有需要转换的图片")


if __name__ == "__main__":
    # 设置要检测的文件夹路径
    target_folder = "./DATASET/nnUNet_raw/Dataset110_TongueSegmentation/imagesTs"  # 替换为你的图片文件夹路径

    if not os.path.exists(target_folder):
        print(f"错误：文件夹 '{target_folder}' 不存在")
    else:
        convert_images(target_folder)