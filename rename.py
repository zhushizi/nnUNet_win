import os
import shutil
from datetime import datetime


def safe_batch_rename(folder_path, prefix="Tongue_"):
    """
    安全批量添加前缀的重命名工具
    :param folder_path: 需要处理的文件夹路径
    :param prefix: 要添加的前缀（默认为Tongue_）
    """
    # ============ 安全验证 ============
    if not os.path.exists(folder_path):
        print(f"错误：文件夹路径不存在 - {folder_path}")
        return

    # 创建备份文件夹（按时间戳命名）
    backup_folder = os.path.join(folder_path, f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    os.makedirs(backup_folder, exist_ok=True)

    # 获取文件列表（排除系统文件）
    valid_files = [f for f in os.listdir(folder_path)
                   if os.path.isfile(os.path.join(folder_path, f))
                   and not f.startswith('.')]

    # 统计信息
    success_count = 0
    skip_count = 0
    error_log = []

    print(f"开始处理文件夹：{folder_path}")
    print(f"共发现 {len(valid_files)} 个文件\n")

    for filename in valid_files:
        old_path = os.path.join(folder_path, filename)

        try:
            # 拆分文件名和扩展名
            name_part, ext = os.path.splitext(filename)

            # 生成新文件名
            new_name = f"{prefix}{name_part}{ext}"
            new_path = os.path.join(folder_path, new_name)

            # 冲突检测
            if os.path.exists(new_path):
                print(f"跳过：{filename} → 目标文件已存在")
                skip_count += 1
                continue

            # 创建备份
            shutil.copy2(old_path, os.path.join(backup_folder, filename))

            # 执行重命名
            os.rename(old_path, new_path)
            print(f"已重命名：{filename} → {new_name}")
            success_count += 1

        except Exception as e:
            error_log.append(f"{filename} - {str(e)}")
            print(f"错误：处理 {filename} 时发生异常 - {str(e)}")

    # 输出统计报告
    print("\n操作完成！统计信息：")
    print(f"成功重命名文件数 : {success_count}")
    print(f"跳过文件数        : {skip_count}")
    print(f"失败文件数        : {len(error_log)}")
    print(f"备份文件位置      : {backup_folder}")

    if error_log:
        print("\n错误日志：")
        for log in error_log:
            print(f"  × {log}")


# ====================== 使用示例 ======================
if __name__ == "__main__":
    target_folder = r"D:\WORK_space\Code_WS\code_workstation\nnUNet-master\tongue_seg_dataset\val\images"  # 修改为您的文件夹路径
    safe_batch_rename(target_folder)