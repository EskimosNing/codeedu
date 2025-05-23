from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool,CodeInterpreterTool,FileWriterTool
import os
import sys
from dotenv import load_dotenv
import yaml
from crewai import LLM
import copy

##############
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

llm=LLM(model=os.environ["MODEL"],api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])


search_tool=SerperDevTool()
code_tool=CodeInterpreterTool()
write_tool=FileWriterTool()
agents_config=None
with open("src/codeedu/config/agents.yaml") as file:
    agents_config=yaml.safe_load(file)

#planner_llm=LLM(model="openrouter/anthropic/claude-3.7-sonnet",api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])
#code_llm=LLM(model="openrouter/anthropic/claude-3.7-sonnet",api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])
# define agents
planner = Agent(
    #config=agents_config['planner'], # type: ignore[index]
    role="Task Planner",
    goal="Responsible for choosing the agents and tasks to according to the input['request'] , the information are including input['agents'] and input['tasks']",
    backstory="You can get information about current agents and tasks from input.You are an advanced AI assistant with vast knowledge spanning multiple disciplines, designed to engage in diverse conversations and provide helpful information",
    memory=True,  # Default: True
    verbose=False,  # Default: False
    allow_delegation=True,  # Default: False
    #tools=[search_tool],  # Optional: List of tools
    llm=copy.deepcopy(llm),
)

researcher = Agent(
    config=agents_config['researcher'],
    
    memory=True,  # Default: True
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    tools=[search_tool],  # Optional: List of tools
    llm=copy.deepcopy(llm)
)
reporting_analyst = Agent(
    config=agents_config['reporting_analyst'], # type: ignore[index]
    #llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4
    memory=True,  # Default: True
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    llm=copy.deepcopy(llm),
    tools=[write_tool]
)
programmer = Agent(
    role="Python Code Execution Specialist",
    goal=(
        "Take a natural-language coding request, generate and run "
        "a Python script that solves it, capture its stdout, and "
        "persist any files as needed."
    ),
    backstory=(
        "You're an expert Python developer and execution runtime. "
        "Your job is to translate user prompts into working scripts, "
        "run them reliably, and return both the code and its results."
    ),
    tools=[code_tool, write_tool],
    allow_code_execution=True,
    verbose=True,
    llm=copy.deepcopy(llm),
    allow_delegation=False,
)


educator = Agent(
    config=agents_config['educator'], # type: ignore[index]
    #llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4
    memory=True,  # Default: True
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    llm=copy.deepcopy(llm),
    tools=[write_tool]
)


# class planner(Agent):
#     def __init__(self):
#         super().__init__(
#             config=agents_config['planner'], # type: ignore[index]
#             verbose=True,
#             tools=[SerperDevTool]
#         )




# class researcher(Agent):
#     def __init__(self):
#         super().__init__(
#             config=agents_config['researcher'], # type: ignore[index]
#             verbose=True,
#             tools=[SerperDevTool]
#         )


# class reporting_analyst(Agent):
#     def __init__(self):
#         super().__init__(
#             config=agents_config['reporting_analyst'], # type: ignore[index]
#             verbose=True
#         )



# class programmer(Agent):
#     def __init__(self):
#         super().__init__(
#             config=agents_config['programmer'], # type: ignore[index]
#             verbose=True,
#             allow_code_execution=True
#         )


# class educator(Agent):
#     def __init__(self):
#         super().__init__(
#             config=agents_config['educator'], # type: ignore[index]
#             verbose=True
#         )

# @agent
# class executor(Agent):
#     def __init__(self):
#         super().__init__(
#             config=agents_config['Executor'], # type: ignore[index]
#             verbose=True
#         )


    