'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-28 13:54:04
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-28 14:07:49
 # @ Description:
 '''
import io
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(text):
    return ansi_escape.sub('', text)

class WordStream(io.StringIO):
    def __init__(self):
        super().__init__()
        self.result_buffer = ""
        self.thought_buffer = ""
        self.raw_thought_lines = []

    def write(self, s):
        self.result_buffer += s
        self.thought_buffer += s
        lines = s.splitlines(keepends=True)
        for line in lines:
            if line.strip():
                self.raw_thought_lines.append(line)

    def get_thought(self):
        return "\n".join(self.raw_thought_lines)

    def get_result(self):
        return strip_ansi(self.result_buffer)
    
