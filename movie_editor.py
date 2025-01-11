from moviepy.editor import *
import os
import re
from PIL import Image
import natsort
import math
import numpy as np

def images_to_video_with_durations(input_image_path, output_video_path, durations, fps, base_name):
    # input_image_path = r'E:\doc2video_byself\material\image\section_1'
    # output_video_path = r'E:\doc2video_byself\material/video'
    # durations = [2, 17.579, 22.593, 15.908, 20.608, 10.357, 17.148, 17.148]
    # fps = 30
    # base_name = 'section_1'

    # 获取所有符合条件的图片，并按文件名中的数字排序
    pattern = r'^' + re.escape(base_name) + r'_(\d+)\.png$'
    image_files = [
        f"{input_image_path}/{file}"
        for file in os.listdir(input_image_path)
        if re.match(pattern, file)
    ]
    image_files = natsort.natsorted(image_files, key=lambda x: int(re.match(pattern, os.path.basename(x)).group(1)))

    # 确定视频的背景尺寸
    target_width, target_height = 1280, 720
    background_size = (target_width, target_height)

    # 为每张图片创建一个单独的剪辑
    clips = []
    print('000')
    for i, file in enumerate(image_files):
        print('111')
        img = Image.open(file)

        print('222')
        width, height = img.size
        ratio = width / height
        print('333')
        if width > target_width or height > target_height:
            print('444')

            if ratio > target_width / target_height:
                new_width = target_width
                new_height = math.floor(new_width / ratio)
            else:
                new_height = target_height
                new_width = math.floor(new_height * ratio)
        else:
            new_width, new_height = width, height
            print('555')

        img = img.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
        img_clip = ImageClip(np.array(img)).set_duration(durations[i])
        # img_clip = img_clip.set_duration('center')

        bg_clip = ColorClip(size=background_size, color=(255,255,255), duration=durations[i])
        composite_clip = CompositeVideoClip([bg_clip, img_clip])
        # 添加转场效果（除了最后一个剪辑）
        # if i < len(image_files) - 1:  # 确保不是最后一个剪辑
        #     composite_clip = composite_clip.fx(vfx.fadein, duration=0.3).fx(vfx.fadeout, duration=0.3)

    
        clips.append(composite_clip)

    # 使用concatenate_videoclips函数将所有剪辑串联起来
    final_clip = concatenate_videoclips(clips, method="compose")


    # 写入视频文件
    output_filename = f"{base_name}.mp4"

    final_clip.write_videofile(os.path.join(output_video_path, output_filename), fps=fps)


