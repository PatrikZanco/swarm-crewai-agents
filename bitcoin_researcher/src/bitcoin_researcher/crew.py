from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from bitcoin_researcher.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SerperDevTool

from langchain_community.llms import Ollama

import os 
from dotenv import load_dotenv

load_dotenv()


llm_ollama = Ollama (model = "llama3", base_url= "http://10.111.0.79:11434/")


scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()



@CrewBase
class BitcoinResearcherCrew():
	"""BitcoinResearcher crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			llm = llm_ollama,
			tools = [
				scrape_tool,
				search_tool,
			]
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm = llm_ollama
		)
	
	@agent
	def translator(self) -> Agent:
		return Agent(
			config = self.agents_config['translator'],
			verbose = True,
			llm = llm_ollama
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)
	
	@task
	def translate_task(self) -> Task:
		return Task (
			config = self.tasks_config['translate_task'],
			agent = self.translator(),
			output_file = 'analyzes_pt-br.md'
		)
	

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='analyzes.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the BitcoinResearcher crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)