'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 19:25:33
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 19:27:10
 # @ Description:流式输出拦截和日志清洗工具
 '''
import io
import re
import queue



# 匹配 ANSI 转义序列的正则
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clear_queue(q: queue.Queue):
    while not q.empty():
        try:
            q.get_nowait()
        except queue.Empty:
            break


#box_drawing = re.compile(r'[─╮╯╰│╭╮╯╰]+')
# 清除颜色控制字符
def strip_ansi(text):
    return ansi_escape.sub('', text)
class WordStream(io.StringIO):
    def __init__(self):
        super().__init__()
        self.result_buffer = ""
        self.raw_thought_lines = []  # 👈 保存每行日志

    def write(self, s):
        self.result_buffer += s
        # 实时收集，但不推送
        lines = s.splitlines(keepends=True)
        for line in lines:
            if line.strip():
                self.raw_thought_lines.append(line)

    def get_thought(self):
        return "\n".join(self.raw_thought_lines)

    def get_result(self):
        return strip_ansi(self.result_buffer)
    

