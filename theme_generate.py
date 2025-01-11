from http import HTTPStatus
import dashscope
import re

def theme_generate_with_qwen_plus(input_filepath, title):
    """
    使用通义千问-Plus生成摘要标题。

    本函数读取指定文件的内容，并基于该内容和给定的主题生成一个精确、概括性的摘要标题。
    
    参数:
    - input_filepath: 输入文件的路径。该文件的内容将用于生成摘要标题。
    - title: 生成摘要标题需围绕的主题。确保生成的标题与该主题紧密相关。

    返回:
    - response_content: 生成的摘要标题。

    注意:
    - 该函数以流式传输的方式请求生成标题，仅当响应状态码为HTTPStatus.OK时，累加响应内容。
    - 如果发生错误，函数会打印请求的相关错误信息。
    """
    # 读取输入文件内容
    with open(input_filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # 构建提示信息，指导模型生成与主题紧密相关的标题
    prompt = f"""
                请为以下输入文档创建一个精确的、具备概括性的摘要标题，能够反映文档核心内容，忽略所有链接，仅聚焦文字信息。
                需要紧紧地围绕主题“{title}”。
                直接呈现标题成果，勿附加其他文本，不超过10个汉字，用中文回答。
                以下是输入文档的内容：
              """

    # 构建消息格式
    messages = [{
        'role': 'user',
        'content': f"""
                    "{prompt}"
                    "{content}"
                   """
    }]

    # 初始化响应内容
    response_content = ''

    # 以流式传输的方式获取生成的结果
    responses = dashscope.Generation.call("qwen-plus",
                                          messages=messages,
                                          result_format='message',
                                          stream=True,
                                          incremental_output=True)

    # 遍历响应，累加生成的标题内容
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            response_content += response.output.choices[0]['message']['content']
        else:
            # 打印错误信息
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))

    # 移除标题中的双引号（如果存在）
    response_content = re.sub(r'^"|"$', '', response_content)

    # 返回生成的标题内容
    return response_content