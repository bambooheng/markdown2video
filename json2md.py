import json
import os
import re
from qwen_plus_marp import call_with_stream
from pathlib import Path

def is_link(text):
    """检查给定的文本是否为链接。"""
    return text.startswith("http://") or text.startswith("https://")

def parse_json_list_to_markdown(json_list, theme_url):
    """
    将 JSON 对象列表转换为 Markdown 格式，并通过 call_with_stream 处理 'content'。
    
    参数:
    - json_list (list): 字典列表，每个字典都包含 'title' 和 'content' 键。
    
    返回:
    - str: Markdown 格式的字符串。
    """
    theme = "![bg 110% opacity:.80](./{theme_filename})\n\n"
    theme_filename = Path(theme_url).name
    markdown_content = ""
    for item in json_list:
        title = item.get('title', '未命名')
        processed_content = call_with_stream(item.get('content', ''))
        
        if is_link(processed_content):
            markdown_content += f"---\n\n![bg right 70%]({processed_content})\n\n---"
        else:
            markdown_content += f"\n\n# {title}\n\n{processed_content}\n\n---"
    return markdown_content


def parse_json_list_to_markdown_new(json_list, theme_url):
    """
    将 JSON 对象列表转换为 Markdown 格式，并通过 call_with_stream 处理 'content'。
    
    参数:
    - json_list (list): 字典列表，每个字典都包含 'title' 和 'content' 键。
    
    返回:
    - str: Markdown 格式的字符串。
    """
    theme_filename = Path(theme_url).name
    theme = f"![bg 110% opacity:.80](./{theme_filename})\n\n"

    markdown_content = ""

    for i, item in enumerate(json_list):
        title = item.get('title', '未命名')
        processed_content = call_with_stream(item.get('content', ''))
        if processed_content.startswith("```") and processed_content.endswith("```"):
            processed_content = processed_content[11:-3].strip()

        if not is_link(json_list[i].get('content')):
            # 如果是列表中的最后一个元素
            if i == len(json_list) - 1:
                markdown_content += f"\n\n## {title}\n\n{processed_content}\n\n{theme}\n\n---"
            else:
                if not is_link(json_list[i + 1].get('content')):
                    # 当前不是链接且下一个也不是链接
                    markdown_content += f"\n\n## {title}\n\n{processed_content}\n\n{theme}\n\n---"
                else:
                    # 当前不是链接但下一个是链接
                    markdown_content += f"\n\n## {title}\n\n{processed_content}\n\n---"
        else:
            # 当前是链接
            markdown_content += f"---\n\n![bg right 70%]({json_list[i].get('content')})\n\n---"

    return markdown_content


def convert_json_file_to_md(json_file_path, output_dir, theme_url):
    """
    读取 JSON 文件，通过 call_with_stream 转换其内容，然后保存为 Markdown 文件。
    
    参数:
    - json_file_path (str): JSON 文件的路径。
    - output_dir (str): Markdown 文件将被保存的目录。
    """
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    markdown_content = parse_json_list_to_markdown_new(json_data, theme_url)
    
    base_name = os.path.splitext(os.path.basename(json_file_path))[0]
    md_file_name = f"{base_name}.md"
    output_path = os.path.join(output_dir, md_file_name)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

def save_markdown_to_file(content, filename):
    """ 保存Markdown内容到文件 """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def process_markdown(input_file):
    """ 处理Markdown文本，按要求分割并保存 """
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # 使用正则表达式确保每个部分都包含 "---"
    parts = re.split(r'(?<=---\n)', input_text)

    # 移除空字符串部分
    parts = [part.strip() for part in parts if part.strip()]

    filenames = []
    base_path = os.path.dirname(input_file)  # 获取基础文件的路径
    
    for i, part in enumerate(parts):
        # 生成文件名
        filename = f'{os.path.splitext(os.path.basename(input_file))[0]}_{i}.md'
        # 构建完整路径
        full_filename = os.path.join(base_path, filename)
        save_markdown_to_file(f'{part}', full_filename)
        filenames.append(full_filename)


