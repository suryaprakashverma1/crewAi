import os
import tempfile
from gtts import gTTS
from IPython.display import Audio

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool   # ✅ matches your pattern
from crewai_tools import SerperDevTool

# --- LLMs ---
ollama_llm = LLM(
    model="ollama/llama3.1:latest",
    base_url="http://host.docker.internal:11434"
)
openai_llm = LLM(model="gpt-4o-mini")

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# Set API keys if needed for search tool
os.environ["SERPER_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""


# --- Custom Tool (TTS) ---
@tool("Text to Speech Tool")
def text_to_speech_tool(text: str) -> str:
    """Convert text to speech and save as mp3 file. Returns file path."""
    output_path = os.path.join(tempfile.gettempdir(), "response.mp3")
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)
    return output_path

# --- Tools ---
search_tool = SerperDevTool()

# instantiate decorated tool properly
tts_tool = text_to_speech_tool  

# --- Agents ---
market_researcher = Agent(
    role="Real Estate Market Researcher",
    goal="Find detailed insights about {developer_name}, their projects, and market positioning.",
    backstory="Expert in analyzing real estate developers and projects.",
    llm=openai_llm,
    tools=[search_tool],
    verbose=True,
    memory=True
)

property_advisor = Agent(
    role="Real Estate Property Advisor",
    goal="Provide client-friendly answers about {developer_name} in response to {user_query}.",
    backstory="Seasoned advisor turning research into clear spoken explanations.",
    llm=openai_llm,
    verbose=True,
    memory=True
)

speech_generator = Agent(
    role="Speech Generator",
    goal="Convert the final text answer into a natural spoken audio file.",
    backstory="Specialist in generating clear speech from text.",
    llm=openai_llm,
    tools=[tts_tool],
    verbose=True
)

# --- Tasks ---
research_task = Task(
    description="Research {developer_name} and collect key insights.",
    expected_output="Bullet-point list of insights.",
    tools=[search_tool],
    agent=market_researcher,
)

answer_task = Task(
    description="Answer '{user_query}' based on research about {developer_name}.",
    expected_output="3–4 paragraph conversational text.",
    agent=property_advisor,
)

speech_task = Task(
    description="Convert the final text into an audio file with TTS. Return ONLY the file path.",
    expected_output="Path to an mp3 file containing spoken response.",
    tools=[tts_tool],
    agent=speech_generator,
)

# --- Crew ---
crew = Crew(
    agents=[market_researcher, property_advisor, speech_generator],
    tasks=[research_task, answer_task, speech_task],
    process=Process.sequential,
    memory=True,
    verbose=False
)

# --- Run ---
inputs = {
    "developer_name": "Emaar Properties",
    "user_query": "What are their best luxury projects in Dubai?"
}

result = crew.kickoff(inputs=inputs)

print("Audio saved at:", result)
Audio(filename=result.raw)   # play in Jupyter
