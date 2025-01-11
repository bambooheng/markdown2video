import os
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(input_directory):
    # 定义视频文件的模式
    video_pattern = r"section_(\d+)_with_audio_with_subs\.mp4"
    
    # 查找并排序符合模式的文件
    files = sorted(
        (fn for fn in os.listdir(input_directory) if re.match(video_pattern, fn)),
        key=lambda x: int(re.match(video_pattern, x).group(1))
    )
    
    # 读取所有视频片段
    clips = [VideoFileClip(os.path.join(input_directory, file)) for file in files]
    
    # 合并所有视频片段
    final_clip = concatenate_videoclips(clips)
    
    # 输出合并后的视频
    output_path = os.path.join(input_directory, 'output_merge_all_video.mp4')
    final_clip.write_videofile(output_path, audio_codec='aac')

