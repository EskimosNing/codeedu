#!/usr/bin/env python
import sys
import warnings
import json
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
from codeedu.crew import Codeedu
from codeedu.task import research_task, reporting_task
from codeedu.agent_pool import planner, researcher, reporting_analyst, programmer, educator,agents_config
from codeedu.task import distribute_task, research_task, reporting_task, tasks_config
from crewai.process import Process
from crewai.crew import Crew

class SurveyFlow(Flow):
    @start
    def searchKnowledge(self):
        print("Starting the flow...")

        crew=Crew(
            agents=[researcher],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
        a=crew.agents[0].completions("search for the best way to learn ranking algorrithms in python,search the infomation and summarize it")
        print("a: ",a)
        output = crew.kickoff(inputs={"request": "search for the best way to learn ranking algorrithms in python,search the infomation and summarize it",
                                  "topic": "ranking algorithms python"})
        result = output.to_doct()
        self.state.result = result
        print("result: ",result)
        return "Starting the flow..."

    @listen(searchKnowledge)
    def reportKnowledge(self):
        print("Received message: ",self.state['result'])
        crew=Crew(
            agents=[reporting_analyst],
            tasks=[reporting_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
        output = crew.kickoff(inputs={"request": "report the knowledge found in the search",
                                  "topic": "ranking algorithms python"})
        result = output.to_doct()
        self.state.result = result
        print("result: ",result)
        return "end the report..."

# if __name__ == "__main__":
#     flow = SurveyFlow()
#     flow.kickoff(inputs={"request": "search for the best way to learn ranking algorrithms in python,search the infomation and summarize it",
#                                   "topic": "ranking algorithms python"})