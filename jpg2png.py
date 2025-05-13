import os
from PIL import Image


def convert_jpg_to_png(source_dir, output_dir):
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 遍历源目录中的所有文件
    for filename in os.listdir(source_dir):
        # 检查文件是否为JPG格式（不区分大小写）
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(source_dir, filename)

            try:
                # 打开图片文件（使用with语句确保正确关闭）
                with Image.open(file_path) as img:
                    # 构造输出路径
                    base_name = os.path.splitext(filename)[0]
                    output_path = os.path.join(output_dir, f"{base_name}.png")

                    # 转换为PNG并保存
                    img.save(output_path, "PNG")
                    print(f"转换成功: {filename} -> {base_name}.png")

            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")


if __name__ == "__main__":
    # 配置路径（按需修改）
    source_dir = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\tongue_seg_dataset\val\images"  # 源目录
    output_dir = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\tongue_seg_dataset\val\images_png"  # 输出目录

    convert_jpg_to_png(source_dir, output_dir)