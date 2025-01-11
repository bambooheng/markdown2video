import argparse
import datetime
import os
import shutil


from doc_split import doc_split_with_qwen_plus
from json2md import convert_json_file_to_md, process_markdown
from markdown_gather import merge_style_with_md_files, remove_trailing_dashes, insert_logo, remove_empty_lines, title_to_md
from marp2image import convert_md_files_to_png
from audio_generate_each_sentence import process_json_file, synthesize_md_to_speech
from srt_generate_for_each_sentence import generate_srt_from_audio
from calculate_durations_for_each_image import calculate_audio_durations
from movie_editor import images_to_video_with_durations
from audio2video import merge_audio_and_add_to_video
from srt2video import merge_video_and_subtitle
from theme_generate import theme_generate_with_qwen_plus

from merge_all_videos import merge_videos
from pathlib import Path
import re



def main(args):
    # 记录开始时间
    start_time = datetime.datetime.now()

    # 创建输出保存路径，将渲染素材复制到指定路径下
    input_base_name = os.path.splitext(os.path.basename(args.input_txt_path))[0]

    if not os.path.exists(args.markdown_path):
        os.makedirs(args.markdown_path)  
    for filename in os.listdir(args.input_style_path):
        full_path = os.path.join(args.input_style_path, filename)
        if os.path.isfile(full_path):
            shutil.copy2(full_path, args.markdown_path) 

    # 原始输入为json,先转成markdown

    # input_txt_path='E:\\11.sigmate_report_pdf_json_to_video\\input\\section_1.md'
    #           input_style_path='E:\\11.sigmate_report_pdf_json_to_video\\style'
    #           markdown_style_path='E:\\11.sigmate_report_pdf_json_to_video\\style\\style.md'
    #           logo_path='E:\\11.sigmate_report_pdf_json_to_video\\style\\logo.png'
    #           theme_path='E:\\11.sigmate_report_pdf_json_to_video\\style / theme.png'
    #           title_path='E:\\11.sigmate_report_pdf_json_to_video\\style / title.png'
    #           json_path='E:\\11.sigmate_report_pdf_json_to_video\\material\\json'
    #           image_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material\\image'
    #           audio_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material/audio'
    #           markdown_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material\\markdown'
    #           srt_and_video_path='E:\\11.sigmate_report_pdf_json_to_video\\material / video'
    #           fps=30
    #           title='支小宝AI生活管家的产品战略与商业化落地分析报告'

    # theme = theme_generate_with_qwen_plus(input_txt_path, title)
    #
    # doc_split_with_qwen_plus(input_txt_path, os.path.join(json_path))

    # 通过API调用通义千问-Plus为输入文档生成文档标题
    theme = theme_generate_with_qwen_plus(args.input_txt_path, args.title)

    print(theme)
    print('1__执行到这儿了，未报错')
    # 通过API调用通义千问-Plus为输入文档划分段落，并为每一个段落生成一个段落标题
    doc_split_with_qwen_plus(args.input_txt_path, os.path.join(args.json_path))

    # 总结各段落内容，保存为Markdown格式，并设置背景图片，可自行将style文件夹下的theme.png替换为自定义背景
    for filename in os.listdir(args.json_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(args.json_path, filename)
            convert_json_file_to_md(json_file_path, args.markdown_path, args.theme_path)


    # 将文档标题添加到Markdown文件开头作为标题页，并设置标题页背景，可自行将style文件夹下的title.png替换为自定义标题页背景
    title_to_md(os.path.join(args.markdown_path,f'{input_base_name}.md'), theme, args.title_path)
    print('2__执行到这儿了，未报错')

    # 删除空行，符合Marp格式
    remove_empty_lines(os.path.join(args.markdown_path,f'{input_base_name}.md'))

    # 添加阿里云logo。可自行替换为其他logo：将logo图片命名为logo.png，放到style文件夹下
    insert_logo(os.path.join(args.markdown_path,f'{input_base_name}.md'), os.path.join(args.logo_path))

    process_markdown(os.path.join(args.markdown_path,f'{input_base_name}.md'))

    # 定义并添加Marp样式文件。可查阅Marp官方文档自定义样式：将样式文件命名为style.md，放到style文件夹下
    merge_style_with_md_files(args.markdown_path, args.markdown_style_path)
    print('3__执行到这儿了，未报错')

    # 删除Markdown文件末尾的“---”，避免生成空白图片
    remove_trailing_dashes(args.markdown_path)
    
    print('3.5__执行到这儿了，未报错')

    # 使用Marp生成演示文稿图片
    convert_md_files_to_png(os.path.join(args.markdown_path,f'{input_base_name}.md'), args.image_path)

    print('4__执行到这儿了，未报错')

    # 将各段落文档划分为若干句子，并通过API调用CosyVoice合成语音 
    process_json_file(os.path.join(args.json_path,f'{input_base_name}.json'), args.audio_path)
    synthesize_md_to_speech(os.path.join(args.audio_path, input_base_name))
    print('5__执行到这儿了，未报错')

    # 生成srt字幕文件
    generate_srt_from_audio(os.path.join(args.audio_path, input_base_name), args.srt_and_video_path, os.path.join(args.srt_and_video_path, input_base_name))
    print('6__执行到这儿了，未报错')

    # 计算各段落的所有音频时长
    durations = calculate_audio_durations(os.path.join(args.audio_path, input_base_name))
    print('7__执行到这儿了，未报错')

    print('7.1__执行到这儿了，未报错')



    # 将所有图片剪辑为视频
    # images_to_video_with_durations(r'E:\doc2video_byself\material\image\section_1'
    #                                ,'E:\doc2video_byself\material/video'
    #                                ,durations = [2, 17.579, 22.593, 15.908, 20.608, 10.357, 17.148, 17.148]
    #                                ,30
    #                                ,'section_1'
    #                                )
    images_to_video_with_durations(os.path.join(args.image_path,f'{input_base_name}'), args.srt_and_video_path, durations, args.fps, input_base_name)
    print('8__执行到这儿了，未报错')

    print(os.path.join(args.srt_and_video_path,f'{input_base_name}.mp4'))
    print(os.path.join(args.audio_path,f'{input_base_name}'))
    print(os.path.join(args.srt_and_video_path))
    print(f'{input_base_name}_with_audio.mp4')
    print(input_base_name)

    # 将音频文件嵌入视频
    merge_audio_and_add_to_video(os.path.join(args.srt_and_video_path,f'{input_base_name}.mp4'), os.path.join(args.audio_path,f'{input_base_name}'), os.path.join(args.srt_and_video_path,f'{input_base_name}_with_audio.mp4'))
    print('9__执行到这儿了，未报错')

    # input_txt_path='E:\\11.sigmate_report_pdf_json_to_video\\input\\section_1.md'
    #           input_style_path='E:\\11.sigmate_report_pdf_json_to_video\\style'
    #           markdown_style_path='E:\\11.sigmate_report_pdf_json_to_video\\style\\style.md'
    #           logo_path='E:\\11.sigmate_report_pdf_json_to_video\\style\\logo.png'
    #           theme_path='E:\\11.sigmate_report_pdf_json_to_video\\style / theme.png'
    #           title_path='E:\\11.sigmate_report_pdf_json_to_video\\style / title.png'
    #           json_path='E:\\11.sigmate_report_pdf_json_to_video\\material\\json'
    #           image_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material\\image'
    #           audio_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material/audio'
    #           markdown_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material\\markdown'
    #           srt_and_video_path='E:\\11.sigmate_report_pdf_json_to_video\\material / video'
    #           fps=30
    #           title='支小宝AI生活管家的产品战略与商业化落地分析报告'

    # video_and_srt_path = 'E:\\11.sigmate_report_pdf_json_to_video\\material\\video'
    # base_name = 'section_1'

    # 将字幕文件嵌入视频
    merge_video_and_subtitle(args.srt_and_video_path, input_base_name)
    print('10__执行到这儿了，未报错')

    # 记录结束时间
    end_time = datetime.datetime.now() 
    print('11__执行到这儿了，未报错')

    # 计算总时间
    elapsed_time = end_time - start_time  
    elapsed_hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
    print('12__执行到这儿了，未报错')

    start_time_str = start_time.strftime("%Y年%m月%d日 %H时%M分%S秒")
    end_time_str = end_time.strftime("%Y年%m月%d日 %H时%M分%S秒")
    elapsed_time_str = f"{int(elapsed_hours)}时{int(elapsed_minutes)}分{int(elapsed_seconds)}秒"
    
    print(f"开始时间: {start_time_str}")
    print(f"结束时间: {end_time_str}")
    print(f"总时间: {elapsed_time_str}")
    print('13__执行到这儿了，未报错')


if __name__ == "__main__":
    path = r'E:\11.sigmate_report_pdf_json_to_video_bk'
    parser = argparse.ArgumentParser(description=path+'文档生成视频')
 
    # 添加命令行参数 --input_txt_path，默认值为 './input/section_1.md'，表示输入文本的路径
    parser.add_argument('--input_txt_path', type=str, default=path+'\input\section_1.md', help='输入文本的路径')

    # 添加命令行参数 --input_style_path，默认值为 './style'，表示输入样式文件夹的路径
    parser.add_argument('--input_style_path', type=str, default=path+'\style', help='输入样式文件夹的路径')

    # 添加命令行参数 --markdown_style_path，默认值为 './style/style.md'，表示 Markdown 样式的路径
    parser.add_argument('--markdown_style_path', type=str, default=path+'\style\style.md', help='Markdown 样式的路径')

    # 添加命令行参数 --logo_path，默认值为 './style/logo.png'，表示 Logo 图片的路径
    parser.add_argument('--logo_path', type=str, default=path+'\style\logo.png', help='Logo 图片的路径')

    # 添加命令行参数 --theme_path，默认值为 './style/theme.png'，表示主题图片的路径
    parser.add_argument('--theme_path', type=str, default=path+'\style/theme.png', help='主题图片的路径')

    # 添加命令行参数 --title_path，默认值为 './style/title.png'，表示标题图片的路径
    parser.add_argument('--title_path', type=str, default=path+'\style/title.png', help='标题图片的路径')

    # 添加命令行参数 --json_path，默认值为 './material/json'，表示 JSON 文件的路径
    parser.add_argument('--json_path', type=str, default=path+'\material\json', help='JSON 文件的路径')

    # 添加命令行参数 --image_path，默认值为 './material/image'，表示图像文件夹的路径
    parser.add_argument('--image_path', type=str, default=path+'\material\image', help='图像文件夹的路径')

    # 添加命令行参数 --audio_path，默认值为 './material/audio'，表示音频文件夹的路径
    parser.add_argument('--audio_path', type=str, default=path+'\material/audio', help='音频文件夹的路径')

    # 添加命令行参数 --markdown_path，默认值为 './material/markdown'，表示 Markdown 文件夹的路径
    parser.add_argument('--markdown_path', type=str, default=path+'\material\markdown', help='Markdown 文件夹的路径')

    # 添加命令行参数 --srt_and_video_path，默认值为 './material/video'，表示字幕和视频文件夹的路径
    parser.add_argument('--srt_and_video_path', type=str, default=path+'\material/video', help='字幕和视频文件夹的路径')

    # 添加命令行参数 --fps，默认值为 30，表示帧率
    parser.add_argument('--fps', type=int, default=30, help='帧率')

    # 添加命令行参数 --title，默认值为 "认识大模型"，表示视频标题
    parser.add_argument('--title', type=str, default="支小宝 AI 生活管家的产品战略与商业化落地分析报告", help='文档主题')

    args = parser.parse_args()
    main(args)


