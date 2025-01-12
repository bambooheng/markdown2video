#!/bin/bash

# 日志文件路径
log_file= r"E:\doc2video\result.log"


# 记录脚本开始时间
start_time=$(date +%s)

# 定义Python脚本路径
python_main_script_path="main.py"
python_merge_script_path="merge_all_videos.py"

# 定义视频输出路径
video_path=“./material/video/”
# 获取所有符合条件的文件名，并按数字排序
files=$(find ./input -maxdepth 1 -type f -name "section_*.md" | sort -V)

# 遍历文件列表
index=0
for file in $files; do
    index_part=$(basename "$file" .md | cut -d '_' -f 2)
    echo "正在处理第${index_part}部分" >> "$log_file"
    python "$python_main_script_path" --input_txt_path "$file" >> "$log_file" 2>&1
    if [ $? -ne 0 ]; then
        echo "Error processing $file" >> "$log_file"
        exit 1
    fi
    ((index++))
done

# 合并视频
python "$python_merge_script_path" --input_directory video_path >> "$log_file" 2>&1

# 记录脚本结束时间
end_time=$(date +%s)

# 计算脚本运行时间
runtime=$((end_time - start_time))

# 格式化运行时间为 xx时xx分xx秒
hours=$((runtime / 3600))
minutes=$(((runtime % 3600) / 60))
seconds=$((runtime % 60))

# 输出提示信息
echo "视频已生成完毕" >> "$log_file"
echo "总计时间: $hours 时 $minutes 分 $seconds 秒" >> "$log_file"

# 输出日志信息
cat "$log_file"