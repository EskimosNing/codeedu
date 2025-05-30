'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 20:30:29
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 20:57:27
 # @ Description:
 '''


from pathlib import Path
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 根目录（从环境变量中获取）
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parent.parent))

# 对话记录存储路径
STORAGE_PATH = Path(os.getenv("STORAGE_PATH", PROJECT_ROOT / "conversations"))
STORAGE_PATH.mkdir(parents=True, exist_ok=True)

# 文件输出目录
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", PROJECT_ROOT / "output"))
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
