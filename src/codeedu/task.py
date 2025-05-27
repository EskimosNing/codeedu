from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from agent_pool import planner, researcher, reporting_analyst, programmer, educator,executor
# from crewai.project import load_yaml_config
from pathlib import Path
# tasks_config = load_yaml_config('config/tasks.yaml')

import yaml
   
TASKS_PATH = Path(__file__).parent / "config" / "tasks.yaml"
tasks_config=None

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)
tasks_config = load_yaml(TASKS_PATH)    

distribute_task = Task(
    config=tasks_config["distribute_task"],
    agent=planner,
    
)

research_task = Task(
    config=tasks_config['research_task'],
    agent=researcher # type: ignore[index]
)

reporting_task = Task(
    config=tasks_config['reporting_task'],

    #output_file='report_test.md',
    agent=reporting_analyst # type: ignore[index]
)
education_task = Task(
    config=tasks_config['education_task'],
    agent=educator # type: ignore[index]
)

code_task = Task(
    config=tasks_config['code_task'],
    agent=programmer,

)
code_analysis_task = Task(
    description=(
        "请使用工具 FileReadTool 读取路径为 `{path}` 的 Python 代码文件，"
        "读取成功后请将完整代码通过 CodeInterpreterTool 工具执行，并完成以下分析任务：\n\n"
        "1. 判断代码是否能正常运行，若存在错误请详细输出错误类型和错误位置；\n"
        "2. 对于不能运行的代码，请给出修复建议，并提供修复后的完整代码；\n"
        "3. 如果原始代码中缺乏示例数据，请自动补充数据并运行，展示执行结果；\n"
        "4. 分析代码的结构与逻辑，判断是否存在潜在问题或不规范写法；\n"
        "5. 提出合理的优化建议，并给出优化后的代码版本与优化理由。"
    ),
    expected_output=(
        "你必须输出一份结构清晰的 Markdown 报告，包含以下部分：\n"
        "- ✅ 原始代码执行结果（或错误信息）\n"
        "- ❌ 错误分析与修复建议（如适用）\n"
        "- 🧪 示例数据与执行结果（如缺失需补全）\n"
        "- 🧠 逻辑与语法结构分析\n"
        "- 🚀 优化建议与优化后代码\n\n"
        "请使用中文撰写报告，保证结构清晰、术语准确。"
    ),
    agent=executor
)



