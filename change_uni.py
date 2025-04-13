#!/usr/bin/python3
import os

# 硬编码的原始文件夹路径
original_folder = "fav-20250405-173918"

# 自动创建对应的新文件夹名
decoded_folder = f"{original_folder}-decoded"

# 创建新文件夹（如果不存在）
os.makedirs(decoded_folder, exist_ok=True)

def decode_unicode_file(src_path, dst_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        decoded_content = content.encode('utf-8').decode('unicode_escape')
    except UnicodeDecodeError as e:
        print(f"[跳过] 解码失败: {src_path}, 错误: {e}")
        return

    with open(dst_path, 'w', encoding='utf-8', errors='replace') as f:
        f.write(decoded_content)

    print(f"[已写入] {dst_path}")

# 遍历原始文件夹
for filename in os.listdir(original_folder):
    src_file_path = os.path.join(original_folder, filename)
    dst_file_path = os.path.join(decoded_folder, filename)

    if os.path.isfile(src_file_path):
        decode_unicode_file(src_file_path, dst_file_path)

print("✅ 全部文件已处理完成。")