from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators




SerperDevTool=SerperDevTool()

@CrewBase
class Codeedu():
    """Codeedu crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    agents: List[BaseAgent]
    tasks: List[Task]


    #llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, max_retry_limit=2,memory=True)
    
    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool],
            memory=True
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool],
            memory=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True,
            memory=True
        )

    
    @agent
    def programmer(self) -> Agent:
        return Agent(
            config=self.agents_config['programmer'], # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            memory=True
        )
    @agent
    def educator(self) -> Agent:
        return Agent(
            config=self.agents_config['educator'], # type: ignore[index]
            verbose=True,
            memory=True
        )

    @task
    def distribute_task(self) -> Task:
        return Task(
            config=self.tasks_config['distribute_task'], # type: ignore[index]
            
        )
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
              # type: ignore[index]
        )

   
    
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )
    @crew
    def crew(self) -> Crew:
        """Creates the Codeedu crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            #manager_agent=self.planner(),
            #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
    @crew
    def get_planner_crew(self)-> Crew:
        #self.planner()
        #self.distribute_task()
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            #memory=True
        )
