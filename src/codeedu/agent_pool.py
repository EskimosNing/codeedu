from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool,CodeInterpreterTool,FileWriterTool
import os
from langchain.memory import ConversationBufferMemory
import sys
from dotenv import load_dotenv
import yaml
from crewai import LLM
import copy
from pathlib import Path
##############
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

llm=LLM(model=os.environ["MODEL"],api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])
#llm_codex=LLM(model="openrouter/openai/codex-mini",api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])
#llm_planner=LLM(model="openrouter/anthropic/claude-3.7-sonnet",api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])

search_tool=SerperDevTool()
code_tool=CodeInterpreterTool()
write_tool=FileWriterTool()
AGENTS_PATH = Path(__file__).parent / "config" / "agents.yaml"
agents_config=None

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)
agents_config = load_yaml(AGENTS_PATH)    

chatAgent=Agent(
    role="Chat Agent",
    goal="You are a chat agent that can answer questions and help with tasks",
    backstory="You are a chat agent that can answer questions and help with tasks",
    memory=True,
    verbose=True,
)

planner = Agent(
    config=agents_config['planner'], # type: ignore[index]
    memory=True,  # Default: True
    verbose=True,  # Default: False
    allow_delegation=True,  # Default: False
    #tools=[search_tool],  # Optional: List of tools
    llm=llm,
)

researcher = Agent(
    config=agents_config['researcher'],
    
    memory=True,  # Default: True
    verbose=True,  # Default: False
    allow_delegation=False,  # Default: False
    tools=[search_tool],  # Optional: List of tools
    llm=llm
)
reporting_analyst = Agent(
    config=agents_config['reporting_analyst'], # type: ignore[index]
    #llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4
    memory=True,  # Default: True
    verbose=True,  # Default: False
    allow_delegation=False,  # Default: False
    llm=llm,
    tools=[write_tool]
)
programmer = Agent(
    config=agents_config['programmer'],
    tools=[code_tool, write_tool],
    allow_code_execution=True,
    memory=True,  # Default: True
    verbose=True,
    llm=llm,
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





    