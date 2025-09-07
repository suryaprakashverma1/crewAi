from crewai import Agent, Task, Crew
from crewai.llm import LLM

# Tell CrewAI to use Ollama as backend
ollama_llm = LLM(
    model="ollama/llama3.1:latest",   # specify provider + model
    base_url="http://host.docker.internal:11434" # point to your running Ollama server
    #base_url="http://localhost:11434"
)

researcher = Agent(
    role="Researcher",
    goal="Find interesting facts",
    backstory="Expert researcher who loves astronomy",
    llm=ollama_llm
)

task = Task(
    description="Collect 5 fun facts about Mars and summarize them.",
    expected_output="A short summary containing exactly 5 fun facts about Mars.",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()

print("Crew Output:\n", result)
