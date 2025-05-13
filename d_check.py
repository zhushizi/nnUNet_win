from PIL import Image
import os

# ====================== 用户修改区域 ======================
target_path = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\DATASET\nnUNet_raw\Dataset110_TongueSegmentation\imagesTr\2_0000.png"  # 直接修改这里的目标路径（支持文件或文件夹）
expected_size = (400, 400)  # 预期尺寸 (宽, 高)，设为None则不限制
expected_channels = 3  # 预期通道数（1-灰度，3-RGB，4-RGBA）


# ========================================================

def describe_channels(channels):
    return {1: "灰度", 3: "RGB", 4: "RGBA"}.get(channels, "未知")


def check_single_image(img_path):
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            channels = len(img.getbands())

            # 构建检测结果
            status = "【正常】"
            size_ok = (expected_size is None) or ((width, height) == expected_size)
            channels_ok = (channels == expected_channels)

            if not (size_ok and channels_ok):
                status = "【异常】"

            print(f"文件: {os.path.basename(img_path)}")
            print(f"路径: {img_path}")
            print(f"实际尺寸: {width}x{height}")
            print(f"预期尺寸: {expected_size or '无限制'}")
            print(f"实际通道: {channels} ({describe_channels(channels)})")
            print(f"预期通道: {expected_channels} ({describe_channels(expected_channels)})")
            print(f"检测状态: {status}\n{'=' * 50}")
            return status == "【正常】"

    except Exception as e:
        print(f"文件打开失败: {img_path}\n错误信息: {str(e)}\n{'=' * 50}")
        return False


if __name__ == "__main__":
    # 自动判断路径类型
    if os.path.isfile(target_path):
        print("正在检测单张图片...\n")
        check_single_image(target_path)

    elif os.path.isdir(target_path):
        print(f"开始批量检测文件夹...\n目标目录: {target_path}\n")
        normal_count = 0
        abnormal_files = []

        for filename in os.listdir(target_path):
            if filename.lower().endswith('.png'):
                full_path = os.path.join(target_path, filename)
                if check_single_image(full_path):
                    normal_count += 1
                else:
                    abnormal_files.append(filename)

        # 统计报告
        total = len([f for f in os.listdir(target_path) if f.lower().endswith('.png')])
        print("\n检测完成！")
        print(f"总PNG文件数: {total}")
        print(f"合规文件数: {normal_count} ({normal_count / total * 100:.1f}%)")
        print(f"异常文件数: {len(abnormal_files)}")
        if abnormal_files:
            print("\n异常文件列表:")
            for f in abnormal_files:
                print(f"  × {f}")

    else:
        print(f"路径不存在: {target_path}")