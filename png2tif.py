import os
from PIL import Image
import time
from datetime import datetime

# ====================== 配置区域 ======================
INPUT_FOLDER = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\DATASET\nnUNet_raw\Dataset110_TongueSegmentation\labelsTr"  # 输入文件夹路径（PNG所在位置）
OUTPUT_FOLDER = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\DATASET\nnUNet_raw\Dataset110_TongueSegmentation\labelsTr_tiff"  # 输出文件夹路径（自动创建）
COMPRESSION = "tiff_lzw"  # 压缩算法：none / tiff_deflate / tiff_lzw
PRESERVE_ALPHA = False  # 是否保留透明度通道（True=保留为RGBA，False=转换为RGB）


# ======================================================

def get_conversion_params(img):
    """智能确定转换参数"""
    params = {
        'compression': COMPRESSION,
        'save_all': False  # 非多页TIFF
    }

    # 处理透明度通道
    if img.mode == 'RGBA':
        params['mode'] = 'RGBA' if PRESERVE_ALPHA else 'RGB'
    elif img.mode == 'LA':
        params['mode'] = 'LA' if PRESERVE_ALPHA else 'L'
    else:
        params['mode'] = img.mode

    return params


def batch_png_to_tiff():
    """批量转换主函数"""
    # 创建输出目录
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 获取文件列表（按名称排序）
    png_files = sorted([f for f in os.listdir(INPUT_FOLDER)
                        if f.lower().endswith('.png')])
    total_files = len(png_files)

    # 初始化统计
    success = 0
    errors = []
    start_time = time.time()

    print(f"开始转换：{INPUT_FOLDER}")
    print(f"共发现 {total_files} 个PNG文件\n")

    for idx, png_file in enumerate(png_files, 1):
        png_path = os.path.join(INPUT_FOLDER, png_file)
        tiff_file = os.path.splitext(png_file)[0] + '.tif'
        tiff_path = os.path.join(OUTPUT_FOLDER, tiff_file)

        try:
            # 打开源文件
            with Image.open(png_path) as img:
                # 保留元数据
                metadata = img.info

                # 获取转换参数
                params = get_conversion_params(img)

                # 执行转换
                img.save(tiff_path,
                         format='TIFF',
                         **params,
                         **metadata)  # 传递原始元数据

            # 打印进度
            print(f"[{idx}/{total_files}] 已转换: {png_file} → {tiff_file}")
            success += 1

        except Exception as e:
            error_msg = f"文件转换失败: {png_file} - {str(e)}"
            print(error_msg)
            errors.append(error_msg)

    # 生成报告
    time_used = time.time() - start_time
    print(f"\n转换完成！用时 {time_used:.1f} 秒")
    print(f"成功转换: {success}/{total_files}")
    print(f"失败文件: {len(errors)}")

    # 保存错误日志
    if errors:
        log_file = os.path.join(OUTPUT_FOLDER, f"conversion_errors_{datetime.now().strftime('%Y%m%d%H%M')}.txt")
        with open(log_file, 'w') as f:
            f.write("\n".join(errors))
        print(f"\n错误日志已保存至: {log_file}")


if __name__ == "__main__":
    batch_png_to_tiff()