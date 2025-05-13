#!/usr/bin/env python
import sys
import warnings
import json
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
#from codeedu.crew import Codeedu
from src.codeedu.agent_pool import planner, researcher, reporting_analyst, programmer, educator,agents_config
from src.codeedu.task import distribute_task, code_task, reporting_task, tasks_config,research_task,education_task
from crewai.process import Process
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
#from codeedu.survey import SurveyFlow
from typing import List,Dict 
from crewai_tools import SerperDevTool
import yaml
from crewai import LLM
from dotenv import load_dotenv 
import os
import sys
import subprocess
from pydantic import BaseModel,Field

##############
load_dotenv()
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")




agents_dict = {
  'researcher': {"id": "researcher", "configuration": agents_config["researcher"], "agent": researcher},
  'reporting_analyst': {"id": "reporting_analyst", "configuration": agents_config["reporting_analyst"], "agent": reporting_analyst},
  'programmer': {"id": "programmer", "configuration": agents_config["programmer"], "agent": programmer},
  'educator': {"id": "educator", "configuration": agents_config["educator"], "agent": educator},
  #'executor': {"id": "executor", "configuration": agents_config["executor"], "agent": executor},
}
#print("agents_dict: ",agents_dict)
tasks_dict = {
  'research_task': {"id": "research_task", "configuration": tasks_config["research_task"], "task": research_task},
  'reporting_task': {"id": "reporting_task", "configuration": tasks_config["reporting_task"], "task": reporting_task},
  'code_task': {"id": "code_task", "configuration": tasks_config["code_task"], "task": code_task},
  'education_task': {"id": "education_task", "configuration": tasks_config["education_task"], "task": education_task},
}
#print("tasks_dict:   ",tasks_dict)
llm=LLM(model=os.environ["MODEL"],api_key=os.environ["OPENROUTER_API_KEY"],base_url=os.environ["BASE_URL"])

managerCrew=Crew(
            agents=[planner],
            tasks=[distribute_task],
            process=Process.sequential,
            verbose=True,
            #memory=True
            
        )

# class resultFlow(BaseModel):
#     agents:Json=Field(description="The agents to be used in the delegation")
#     tasks:Json=Field(description="The tasks to be used in the delegation")

class AskFlow(Flow):

    @start()
    def chooseAgentAndTask(self):
        """
        This function is responsible for choosing the agents and tasks to resolve the user request.
        It returns a dictionary with the delegation configuration and the user request.
        The delegation configuration is a dictionary with the agents and tasks to be used in the delegation.
        The user request is the request that the user made to the system.
        """
        print("Starting the flow...Starting the flow...Starting the flow...")
        #print(f"State ID: {self.state['id']}")
        request = self._state['request']
        
        # crew=Crew(
        #     agents=self.agents,
        #     tasks=self.tasks,
        #     process=Process.sequential,
        #     verbose=True,
        #     memory=True
        #     )
        
        #print("crew: ",crew)

        inputs={
            "request": request,
            "agents": json.dumps({"Agents": [{"id": item["id"], "configuration": item["configuration"]} for item in agents_dict.values()]}),
            "tasks": json.dumps({"Tasks": [{"id": item["id"], "configuration": item["configuration"]} for item in tasks_dict.values()]}),
        }

        result = managerCrew.kickoff(inputs=inputs)
        # print(f"Raw Output: {result.raw}")
        result=json.loads(result.raw)
        #print("result: ",result.to_dict())
        #print("result: ",type(result))
        self.state['result'] = result
        self.state['user_request'] = request
        
        return {'distribution_config': result, "user_request": request}
    
    @listen(chooseAgentAndTask)
    def resolveUserRequest(self):
        """
        This function is responsible for resolving the user request.
        It returns the final result of the user request.
        """
        
        #print("Received messageReceived messageReceived messageReceived message")
        #print(f"Received message: {self.state['result']}")
        chosen_agents = [agents_dict[agent["id"]]["agent"] for agent in self.state['result']["distribution_config"]["agents"]]
        choosen_tasks = [tasks_dict[task["id"]]["task"] for task in self.state['result']["distribution_config"]["tasks"]]
        #print("chosen_agents: ",chosen_agents[0])
        #print("choosen_tasks: ",choosen_tasks)
        print("Received messageReceived messageReceived messageReceived message")
        crew=Crew(
            agents=chosen_agents, 
            tasks=choosen_tasks,
            process=Process.sequential,
            #planning=True,
            verbose=True,
            #memory=True,
            )
        #print("crew: ",crew)
        output = crew.kickoff(inputs={"request": self.state["user_request"],"question":self.state["user_request"]})


        return {'result': output}


    # def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'Python, algorithms, or frameworks',
#         'current_year': str(datetime.now().year)
#     }
    
#     try:
#         Codeedu().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")
    
# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'Python, algorithms, or frameworks',
#         'current_year': str(datetime.now().year)
#     }
#     flow = AskFlow()
#     result=flow.kickoff(inputs=inputs)
#     print(result)   

def kickoff():
    inputs = {
        'request': 'Search the PyTorch documentation, and teach me about Tensors and save as pytorch_turtor.md. Do not need programming.',
        
        
    }
    flow = AskFlow()
    result=flow.kickoff(inputs=inputs)
    #print(result)   

if __name__ == "__main__":
    # flow = SurveyFlow()
    # result=flow.kickoff(inputs={'request': 'search for the best way to learn ranking algorrithms in python,search the infomation and summarize it',
    #                               'topic': 'ranking algorithms python'})
    # # print(result)
    kickoff()

# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         Codeedu().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Codeedu().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         Codeedu().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
