#!/bin/bash

# 设置输入和输出目录
input_dir="data/UCF-101/TaiChi"
output_dir="data/UCF-101/TaiChi"

# 检查输出目录是否存在，不存在则创建
mkdir -p "$output_dir"

# 循环处理每个 avi 视频文件
for avi_file in "$input_dir"/*.avi; do
    # 获取文件名（不带路径和扩展名）
    filename=$(basename -- "$avi_file")
    filename_no_ext="${filename%.*}"

    # 设置输出 jpg 文件路径
    output_jpg="$output_dir/$filename_no_ext.jpg"

    # 使用 ffmpeg 将 avi 转换成 jpg
    ffmpeg -i "$avi_file" -vf "fps=25, scale=640:480, format=yuv420p" -q:v 2 "$output_jpg"
done

echo "Conversion completed."
