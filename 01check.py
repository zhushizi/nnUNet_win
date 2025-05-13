from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def visualize_binary_pixels(image_path):
    """
    可视化二值图像中值为1的像素区域
    返回：(是否有效, 详细信息)
    """
    try:
        with Image.open(image_path) as img:
            # 转换为灰度图处理
            img_gray = img.convert('L')
            arr = np.array(img_gray)

            # 验证像素值
            illegal_pixels = arr[~np.isin(arr, [0, 1])]
            if len(illegal_pixels) > 0:
                illegal_values = np.unique(illegal_pixels)
                return (False, f"包含非法像素值: {illegal_values.tolist()}")

            # 创建可视化画布
            plt.figure(figsize=(12, 6))

            # 原始图像
            plt.subplot(1, 2, 1)
            plt.imshow(img.convert('RGB') if img.mode != 'RGB' else img)
            plt.title('Original Image')
            plt.axis('off')

            # 高亮显示值为1的像素
            plt.subplot(1, 2, 2)
            plt.imshow(arr == 1, cmap='Reds', interpolation='none')
            plt.title('Value=1 Pixels (Red Areas)')
            plt.axis('off')

            plt.tight_layout()
            return (True, "有效二值图像")

    except Exception as e:
        return (False, f"处理失败: {str(e)}")


# 使用示例
if __name__ == "__main__":
    image_path = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\DATASET\nnUNet_raw\Dataset110_TongueSegmentation\labelsTr\2.png"  # 替换为你的图片路径
    is_valid, message = visualize_binary_pixels(image_path)

    print(f"检查结果: {'✓' if is_valid else '✗'}")
    print(f"详细信息: {message}")

    if is_valid:
        plt.show()
    else:
        print("无需可视化显示")