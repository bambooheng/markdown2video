import os
import re
from pathlib import Path
import os


def merge_style_with_md_files(md_file_path, style_file_path):
    # 检查样式文件是否存在
    if not os.path.isfile(style_file_path):
        raise FileNotFoundError(f"样式文件 {style_file_path} 不存在。")
    
    # 读取样式文件内容
    with open(style_file_path, 'r', encoding='utf-8') as f:
        style_content = f.read()
    
    # 遍历指定目录下的所有文件
    for filename in os.listdir(md_file_path):
        if filename.startswith('section') and filename.endswith('.md'):
            file_path = os.path.join(md_file_path, filename)
            # 合并样式内容与 .md 文件内容
            if os.path.exists(file_path):
                with open(file_path, 'r+', encoding='utf-8') as f:
                    original_content = f.read()
                    # 将指针移动到文件开头以覆盖原有内容
                    f.seek(0)
                    f.write(style_content + '\n\n' + original_content)
                    # 清除输出缓冲区以确保所有数据都已写入文件
                    f.truncate()


def remove_trailing_dashes(directory):
    """
    从 Markdown 文件中移除位于文件末尾且后面没有其他内容（除了可能的换行符）的连续破折号（---）。
    """
    for filename in os.listdir(directory):
        # 检查文件是否以 section 开头且为 .md 文件
        if filename.startswith('section') and filename.endswith('.md'):
            filepath = os.path.join(directory, filename)

            # 读取文件内容
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # 检查文件末尾是否有连续的破折号（---），并且之后没有其他内容（除了可能的换行符）
            if content.rstrip().endswith('---') and content.rstrip('---').endswith('\n'):
                # 移除末尾的连续破折号（---）及其后面的换行符
                content = content.rstrip('---\n')

            # 替换文件中的所有 "------" 为空字符串
            content = content.replace("------", "")
            content = re.sub(r'\n{3,}', '\n\n', content)

            # 写入更新后的内容
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)


def remove_empty_lines(filename):
    # 读取文件内容
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    # 替换文件中的所有 "------" 为空字符串
    content = content.replace("------", "")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def append_string_to_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 在文件末尾追加字符串 '---'
    new_content = content + '---'

    # 写入新内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)


def insert_logo(file_path, logo_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 获取 Logo 文件名
    logo_filename = Path(logo_path).name

    # 定义要插入的字符串
    insert_str = f"""<!--\nbackgroundImage: url("./{logo_filename}");\nbackgroundSize: 10% ;\nbackgroundPosition: 98% 3% ;\n-->
                    """

    # 使用正则表达式替换
    # 只替换独立出现的 "---"，不包括被其他破折号包围的情况
    new_content = re.sub(r'(?<!-)---(?!-)', f'\n{insert_str}\n---', content, flags=re.DOTALL)

    # 写入新内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)


def insert_bg_if_no_link(filename, theme_url):
    # 用于存储最终结果的列表
    result = []

    # 读取文件内容
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 获取 Logo 文件名
    theme_filename = Path(theme_url).name

    # 使用正则表达式分割文本
    sections = re.split(r'---+', content)

    # 遍历每个部分
    for i, section in enumerate(sections):
        # 查找 "# {字符串内容}" 的模式
        header_match = re.search(r'# \{(.+?)\}', section)
        if header_match:
            # 提取 "# {字符串内容}" 后面的内容
            header_content = section[header_match.end():].strip()

            # 检查这部分内容是否包含 ![parameter](url) 格式的链接
            if not re.search(r'!\[[^\]]*\]\([^\)]*\)', header_content):
                # 如果没有链接也没有背景图片，在 "# {字符串内容}" 之后添加指定文本
                section = f'{section[:header_match.end()]}![bg 110% opacity:.80](./{theme_filename})\n{section[header_match.end():]}\n---'

        # 将处理后的部分添加到结果列表中
        result.append(section)

        # 如果不是最后一个部分，保留原始的分隔符
        if i < len(sections) - 1:
            result.append('---')

    # 将结果写回文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(''.join(result))


def title_to_md(file_path, content, title_url):
    # 读取原文件内容
    title_filename = Path(title_url).name
    with open(file_path, 'r', encoding='utf-8') as file:
        original_content = file.read()
    content = f"![bg right:60% ](./{title_filename})\n# {content}\n---"
    # 在开头添加新内容
    new_content = content + '\n' + original_content

    # 写入新内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)