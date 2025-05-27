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
        "通过工具file_read_tool阅读python文件，之后将读取到的代码通过工具code_tool执行，要求分析代码的逻辑和语法是否存在问题，"
        "如果读取的python代码中存在错误，则将正确的代码和错误的代码一并输出，"
        "如果读取的python代码中没有示例，则提供示例数据后执行代码：{path}"
    ),
    expected_output=(
        "结果用中文表示："
        "1. 输出代码执行后的结果，2. 对结果的分析，3. 若是代码存在错误，则将正确的代码和错误的代码一并输出，"
        "4. 示例数据和执行示例数据后的结果，5. 对代码语法逻辑的分析结果，6. 如何将代码进行优化，给出示例和理由"
    ),
    agent=executor
)



