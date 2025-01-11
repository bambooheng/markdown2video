import asyncio

import os
from http import HTTPStatus
import dashscope

def call_with_stream(content):
    prompt2 = """
                    请提取下列文字的主要要点，并将这些要点以Markdown格式输出，请输出中文。
                    如果文字内容为链接，请直接以Markdown格式输出该链接。
                    请严格按照Markdown格式输出代码段，避免输出其他内容，避免出现'''之类的符号。
                    但是Markdown文字内容简洁。
                    Markdown代码段中，每一个小标题下的的内容行数禁止超过3行。
                    “- 内容”之后不要再分段落描述。

                    示例输入：你有过使用搜索引擎搜索问题却怎么也找不到有效信息的时候吗？
                    示例输出：- 使用搜索引擎遇到的问题：难以找到有效信息

                    示例输入：https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/54Lq3RNeD78gn7Ed/img/6f9f3049-78a2-46b3-a052-88792052890d.png
                    示例输出：https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/54Lq3RNeD78gn7Ed/img/6f9f3049-78a2-46b3-a052-88792052890d.png

                    以下是待提炼的文字内容：
                    

              """


    messages = [{
        'role': 'user',
        'content': f"""
                    "{prompt2}"
                    "{content}"
                   """
    }]

    response_content = ''
    responses = dashscope.Generation.call("qwen-plus",
                                          messages=messages,
                                          result_format='message',
                                          stream=True,
                                          incremental_output=True)

    for response in responses:
        if response.status_code == HTTPStatus.OK:
            response_content += response.output.choices[0]['message']['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))

    return response_content
