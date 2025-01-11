import subprocess
import os
def merge_video_and_subtitle(video_and_srt_path, base_name):

    video_and_srt_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material\\video'
    base_name = 'section_1'

    video_ext = ".mp4"
    srt_ext = ".srt"

    video_path = os.path.join(video_and_srt_path, f"{base_name}_with_audio" + video_ext).replace("\\", "/")
    srt_path = os.path.join(video_and_srt_path, base_name + srt_ext).replace("\\", "/")
    output_path = os.path.join(video_and_srt_path, f"{base_name}_with_audio_with_subs" + video_ext).replace("\\", "/")

    # print(video_path)
    # print(srt_path)
    # print(output_path)
    # ============================代码修改============================
    video_path = '.' + (video_path[video_path.find("/material"):])
    srt_path = '.' + (srt_path[srt_path.find("/material"):])
    output_path = '.' + (output_path[output_path.find("/material"):])
    # ============================代码修改============================
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'subtitles={srt_path}',
        # '-c:a', 'copy',
        output_path
    ]

    print(command)

    try:
        # subprocess.run(command, check=True)
        temp1 = ' '.join(command)
        print('temp1', temp1)
        os.system(temp1)
        print('命令执行成功')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while merging video and subtitles: {e}")

