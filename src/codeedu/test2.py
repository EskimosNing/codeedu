from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeInterpreterTool
from crewai_tools import FileWriterTool
from langchain.tools import tool
import os
import subprocess
import sys
from dotenv import load_dotenv 


##############
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


# Tools
code_tool = CodeInterpreterTool()
write_tool = FileWriterTool()

# Agent definition
agent = Agent(
    role="Python Code Execution Specialist",
    goal=(
        "Take a natural‑language coding request, generate and run "
        "a Python script that solves it, capture its stdout, and "
        "persist any files as needed."
    ),
    backstory=(
        "You’re an expert Python developer and execution runtime. "
        "Your job is to translate user prompts into working scripts, "
        "run them reliably, and return both the code and its results."
    ),
    tools=[code_tool, write_tool],
    allow_code_execution=True,
    verbose=True,
    allow_delegation=False,
)

# Task definition
task = Task(
    description=(
        "User has asked:\n\n"
        "{question}\n\n"
        "Generate the Python code to satisfy this request, execute it, "
        "and write out any output files via the File Writer tool."
    ),
    expected_output=("The actual code used to get the answer to the file."),
    agent=agent,
)

# Crew orchestration
crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True
)

# Kickoff
while True:
    question = input("Enter your code question: ")
    result = crew.kickoff(inputs={"question": question})
    