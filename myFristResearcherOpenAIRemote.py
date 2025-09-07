##since we have not given any model , Open AI choose what ever it defaults to.
##open API key is provided during running the container.

from crewai import Agent, Task, Crew

# Define an agent
researcher = Agent(
    role="Researcher",
    goal="Find interesting facts about Mars",
    backstory="You are a space enthusiast who loves gathering information.",
)

# Define a task
task = Task(
    description="Collect 5 fun facts about Mars and summarize them.",
    expected_output="A short summary containing exactly 5 fun facts about Mars.",
    agent=researcher,
)

# Create a Crew with agent + task
crew = Crew(
    agents=[researcher],
    tasks=[task]
)

# Run it (new API)
result = crew.kickoff()

print("Crew Output:\n", result)

