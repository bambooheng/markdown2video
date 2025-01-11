import os
from moviepy.editor import *
from glob import glob
import re
def merge_audio_and_add_to_video(video_path, audio_base_dir, output_path):
    """
    合并多个音频文件并添加到视频中。

    :param video_path: 视频文件的路径。
    :param audio_base_dir: 包含音频文件夹的基目录。
    :param output_path: 输出视频的路径。
    """
    # 加载视频文件
    video_clip = VideoFileClip(video_path)
    
    # 初始化音频列表
    audio_clips = []

    silent_audio_start = AudioClip(lambda t: [0,0], duration=2)
    audio_clips.append(silent_audio_start)
    
    # 遍历所有子目录，按数字大小排序
    audio_dirs = glob(os.path.join(audio_base_dir, "audio_for_paragraph_*"))
    audio_dirs.sort(key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))

    # 遍历所有子目录
    for audio_dir in audio_dirs:
        # 获取当前目录的index
        index = int(os.path.basename(audio_dir).split("_")[-1])
        
        # 遍历目录中的所有mp3文件
        mp3_files = glob(os.path.join(audio_dir, f"paragraph_{index}_sentence_*.mp3"))
        mp3_files.sort(key=lambda x: int(re.search(r'_sentence_(\d+)', os.path.basename(x)).group(1)))

        # 遍历排序后的mp3文件列表
        for mp3_file in mp3_files:
            # 加载音频文件
            audio_clip = AudioFileClip(mp3_file)
            
            # 添加到音频列表
            if audio_clips:
                # 如果不是第一个音频，则在前一个音频之后添加0.5秒的静音
                # 替换原有的 AudioNullClip 代码
                silent_audio = AudioClip(lambda t: [0,0], duration=0.3)
                audio_clips.append(silent_audio)
            audio_clips.append(audio_clip)
    
    # 合并所有音频片段
    final_audio = concatenate_audioclips(audio_clips)
    
    # 将音频添加到视频中
    video_with_audio = video_clip.set_audio(final_audio)
    
    # 输出带有新音频的视频文件
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    # 关闭剪辑对象，释放资源
    video_clip.close()