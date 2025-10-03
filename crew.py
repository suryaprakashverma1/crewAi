import os
import tempfile
import logging
from gtts import gTTS
from dotenv import load_dotenv
import speech_recognition as sr
from playsound import playsound

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool  
from crewai_tools import SerperDevTool

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validate environment variables
google_key = os.getenv("GOOGLE_API_KEY")
if not google_key:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY is required")

serper_key = os.getenv("SERPER_API_KEY")
if not serper_key:
    logger.warning("SERPER_API_KEY not found - search functionality may be limited")

# --- LLMs ---
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)


import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# --- Custom Tool (TTS) ---
@tool("Text to Speech Tool")
def text_to_speech_tool(text: str) -> str:
    """Convert text to speech and save as high-quality MP3 file with natural voice settings. Returns file path."""
    output_path = os.path.join(tempfile.gettempdir(), f"response_{hash(text)}.mp3")
    # Use US English accent for more natural sound, normal speed
    tts = gTTS(text=text, lang="en", tld="us", slow=False)
    tts.save(output_path)
    return output_path

# --- STT Function ---
def listen_for_query():
    """Listen for user voice input and return transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your query...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.WaitTimeoutError:
            print("No speech detected. Listening again...")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return None

# --- Tools ---
search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))

# instantiate decorated tool properly
tts_tool = text_to_speech_tool  

# --- Agents ---
market_researcher = Agent(
    role="Senior Real Estate Market Analyst",
    goal="Conduct comprehensive research on {developer_name}, including their portfolio of projects, market reputation, financial performance, and competitive positioning in the real estate industry.",
    backstory="A seasoned real estate analyst with over 15 years of experience in market research, specializing in developer profiling, project analysis, and industry trends. Expert in synthesizing data from multiple sources to provide actionable insights.",
    llm=llm,
    tools=[search_tool],
    verbose=True,
    memory=False
)

property_advisor = Agent(
    role="Friendly Real Estate Consultant",
    goal="Act as a human-like assistant answering customer questions about {developer_name} properties in a natural, conversational manner, providing helpful information based on research.",
    backstory="A warm, experienced real estate professional who speaks directly to customers like a trusted friend or advisor. Specializes in giving straightforward, personalized answers that sound natural and human, avoiding jargon while being informative and engaging.",
    llm=llm,
    verbose=True,
    memory=False
)

speech_generator = Agent(
    role="Professional Voice Synthesizer",
    goal="Transform written content into high-quality, natural-sounding speech that maintains the original meaning while optimizing for listener engagement and clarity.",
    backstory="An AI specialist in natural language processing and voice synthesis, with expertise in creating human-like audio content. Focuses on pacing, intonation, and pronunciation to deliver professional-grade audio experiences.",
    llm=llm,
    tools=[tts_tool],
    verbose=True,
    memory=False
)

# --- Tasks ---
research_task = Task(
    description="Perform in-depth research on {developer_name} by searching reliable sources for information about their company history, current projects, completed developments, market reputation, financial stability, and competitive advantages. Focus on recent news, awards, and customer reviews.",
    expected_output="A comprehensive bullet-point list covering: company overview, key projects (ongoing and completed), market positioning, financial health indicators, and notable achievements or controversies.",
    tools=[search_tool],
    agent=market_researcher,
)

answer_task = Task(
    description="Using the research insights about {developer_name}, provide a direct, human-like response to '{user_query}' as if you are a knowledgeable real estate consultant speaking to a potential customer. Be conversational, friendly, and focus only on answering the specific question asked.",
    expected_output="A natural, spoken-style response of 2-3 paragraphs that directly addresses the user's question with relevant information from research. Use contractions, personal language, and maintain a helpful, professional tone like a human assistant would.",
    agent=property_advisor,
)

speech_task = Task(
    description="Take the final text response and convert it into a high-quality audio file using text-to-speech technology. Optimize the speech for natural pacing, clear pronunciation, and engaging delivery that sounds human-like and professional.",
    expected_output="Full path to the generated MP3 audio file containing the spoken version of the text response.",
    tools=[tts_tool],
    agent=speech_generator,
)

# --- Crew ---
crew = Crew(
    agents=[market_researcher, property_advisor, speech_generator],
    tasks=[research_task, answer_task, speech_task],
    process=Process.sequential,
    memory=False,
    verbose=False
)

# --- Run ---
if __name__ == "__main__":
    print("Starting live voice assistant. Say 'exit' to quit.")
    while True:
        user_query = listen_for_query()
        if user_query:
            if user_query.lower() in ['exit', 'quit', 'stop']:
                print("Exiting...")
                break
            inputs = {
                "developer_name": "Emaar Properties",
                "user_query": user_query
            }
            try:
                logger.info("Starting CrewAI execution")
                result = crew.kickoff(inputs=inputs)
                logger.info(f"Crew execution completed. Playing audio...")
                playsound(result)
            except Exception as e:
                logger.error(f"Error during crew execution: {str(e)}")
                print(f"Error: {e}")
        else:
            continue