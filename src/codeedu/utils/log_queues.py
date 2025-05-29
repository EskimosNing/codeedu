'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 21:31:42
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 21:31:56
 # @ Description:
 '''

import queue

# 全局日志队列（用于 thought 和 result）
log_queue_thought = queue.Queue()
log_queue_result = queue.Queue()