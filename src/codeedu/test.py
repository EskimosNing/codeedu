from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeInterpreterTool
from crewai_tools import FileWriterTool
from langchain.tools import tool
import os
import subprocess
import sys
from dotenv import load_dotenv 
from codeedu.agent_pool import programmer   
from codeedu.task import code_task

##############
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


# Crew orchestration
crew = Crew(
    agents=[programmer],
    tasks=[code_task],
    process=Process.sequential,
    verbose=True
)

question = input("Enter your code question: ")
result = crew.kickoff(inputs={"question": question})
print(result)
