'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 21:38:39
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 21:38:49
 # @ Description:
 '''
from agent_pool import researcher, reporting_analyst, programmer, educator,agents_config
from task import code_task, reporting_task, tasks_config,research_task,education_task,generate_quiz_task
agents_dict = {
  'researcher': {"id": "researcher", "configuration": agents_config["researcher"], "agent": researcher},
  'reporting_analyst': {"id": "reporting_analyst", "configuration": agents_config["reporting_analyst"], "agent": reporting_analyst},
  'programmer': {"id": "programmer", "configuration": agents_config["programmer"], "agent": programmer},
  'educator': {"id": "educator", "configuration": agents_config["educator"], "agent": educator},
 
}

tasks_dict = {
  'research_task': {"id": "research_task", "configuration": tasks_config["research_task"], "task": research_task},
  'reporting_task': {"id": "reporting_task", "configuration": tasks_config["reporting_task"], "task": reporting_task},
  'code_task': {"id": "code_task", "configuration": tasks_config["code_task"], "task": code_task},
  'education_task': {"id": "education_task", "configuration": tasks_config["education_task"], "task": education_task},
  'generate_quiz_task':{"id": "generate_quiz_task", "configuration": tasks_config["generate_quiz_task"], "task": generate_quiz_task},
}
