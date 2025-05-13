from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.codeedu.agent_pool import planner, researcher, reporting_analyst, programmer, educator
# from crewai.project import load_yaml_config

# tasks_config = load_yaml_config('config/tasks.yaml')

import yaml
   
tasks_config=None
with open("src/codeedu/config/tasks.yaml") as file:
    tasks_config = yaml.safe_load(file)

distribute_task = Task(
    description=(
        "Selects suitable agents and tasks according to {request}, using the agent and task details from {agents} and {tasks}."
    ),
    expected_output=("The manager returns a distribution_config dictionary that includes the corresponding dictionary values (from agents_dict and tasks_dict given in the input) for each selected agent and task."
                     '''respoense format should like this{
                    "distribution_config": {
                        "agents": [<agent_object>, ...],
                        "tasks": [<task_object>, ...]
                    }
                    Each <agent_object> is an entry from {agents}, and each <task_object> is from input{tasks}.
                    '''
                     ),
    agent=planner,
    
)

research_task = Task(
    config=tasks_config['research_task'],
    agent=researcher # type: ignore[index]
)

reporting_task = Task(
    config=tasks_config['reporting_task'],
    output_file='report_test.md',
    agent=reporting_analyst # type: ignore[index]
)
education_task = Task(
    config=tasks_config['education_task'],
    agent=educator # type: ignore[index]
)

code_task = Task(
    description=(
        "User has asked:\n\n"
        "{question}\n\n"
        "Generate the Python code to satisfy this request, execute it, "
        "and write out any output files via the File Writer tool."
    ),
    expected_output=("The actual code used to get the answer to the file."),
    agent=programmer,
)
# class research_task(Task):
#     def __init__(self):
#         super().__init__(
#             config=tasks_config['research_task'], # type: ignore[index]
#         )


# class reporting_task(Task):
#     def __init__(self,agent:Agent):
#         super().__init__(
#             config=tasks_config['reporting_task'], # type: ignore[index]
#             output_file='report.md',
#             agent=agent
#         )


# class distribute_task(Task):
#     def __init__(self,agent:Agent):
#         super().__init__(
#             config=tasks_config['distribute_task'], # type: ignore[index]
#             agent=agent
#         )
