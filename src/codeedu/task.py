from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from agent_pool import planner, researcher, reporting_analyst, programmer, educator
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


