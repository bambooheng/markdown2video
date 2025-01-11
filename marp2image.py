import os
import re
import subprocess

def convert_md_files_to_png(md_file_path, output_base_dir="./Marp/"):
    """
    顺序读取和输入与 md_file_path 文件相同路径中的所有命名格式为 {base_name}_{index}.md 的文件，
    并按 index 的数字大小顺序遍历所有文件，使用 Marp 直接生成 PNG 格式的图片。

    :param md_file_path: MD 文件的完整路径。
    :param output_base_dir: 输出目录的基路径，将在此目录下创建子目录以保存输出文件。
    """
    print('md_file_path',md_file_path)
    print('output_base_dir',output_base_dir)

    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    print('3.5.1__执行到这儿了，未报错')
    # 获取MD文件名（去掉.md后缀）
    base_name = os.path.splitext(os.path.basename(md_file_path))[0]
    print('base_name',base_name)
    print('3.5.2__执行到这儿了，未报错')
    directory = os.path.dirname(md_file_path)
    print('directory',directory)
    print('3.5.3__执行到这儿了，未报错')

    # 获取所有符合条件的文件名
    md_files = [f for f in os.listdir(directory) if f.startswith(base_name + '_') and f.endswith('.md')]
    md_files.sort()  # 按文件名排序
    print('md_files',md_files)
    print('3.5.4__执行到这儿了，未报错')

    # 创建输出目录，目录名与MD文件名相同
    output_dir = os.path.join(output_base_dir, base_name)
    os.makedirs(output_dir, exist_ok=True)  # 如果目录已存在，则不会抛出异常
    print('3.5.5__执行到这儿了，未报错')

    for md_file in md_files:
        print('md_file',md_file)
        md_file_path = os.path.join(directory, md_file)
        print('md_file_path',md_file_path)
        base = os.path.splitext(os.path.basename(md_file_path))[0]
        print('base',base)

        match = re.match(rf"{re.escape(base_name)}_(\d+)", base)
        if match:
            index = int(match.group(1))  # 提取索引

            print('output_dir',output_dir)
            print('md_file_path',md_file_path)

            # 构建Marp CLI命令
            command = ["marp", "--html", "--allow-local-files",
                       "--output", os.path.join(output_dir, f"{base_name}_{index}.png"),
                       "--format", "png",
                       md_file_path]

            try:
                # 执行命令，将MD文件转换为PNG
                print('000')
                print('command',command)
                # subprocess.run(command, check=True)
                temp1 = ' '.join(command)
                print('temp1',temp1)
                os.system(temp1)
                print('111')
                print(f"成功将 '{md_file_path}' 转换为PNG并保存至 '{output_dir}'。")
            except subprocess.CalledProcessError as e:
                print(f"转换 '{md_file_path}' 时发生错误: {e}")
    print('3.5.6__执行到这儿了，未报错')



# import subprocess
#
#
# command = ['marp', '--html', '--allow-local-files', '--output', 'E:\\doc2video_byself\\material\\image\\section_1\\section_1_0.png', '--format', 'png', 'E:\\doc2video_byself\\material\\markdown\\section_1_0.md']
# command = ['wsl',"ls"]  # 示例命令
# subprocess.run(command, check=True)
#
# subprocess.run("echo Hello", shell=True, check=True)
