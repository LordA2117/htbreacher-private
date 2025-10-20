from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.models.ollama import Ollama
from dotenv import load_dotenv
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.knowledge.reader.text_reader import TextReader
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.baidusearch import BaiduSearchTools
import os
import json
import sys

if len(sys.argv) > 1 and sys.argv[1] == "online":
    load_dotenv()  # uncomment this to use the online model
    api_key = os.getenv("OLLAMA_API_KEY")
    # print(api_key)

instructions = [
    "You are HTBreacher, a smart assistant designed to help CTF players with HackTheBox and Boot2Root Machines.",
    "Provided to you is a knowledge base, containing the solutions to various machines from HackTheBox, HackMyVM and Vulnhub. You will use this as your primary source of information. Each answer that uses this knowledge base is to be followed by a footnote saying that you used this Knowledge base as the source.",
    "If the information requested is not present in the knowledge base, or you're asked to elaborate more on something, you are free to use your own internal knowledge base as reference. But you will specify this in the footnote.",
    "In The event that you use BOTH the knowledge bases, the one provided locally and the one you have built in, you will specify this as well.",
    "Your primary task, as mentioned before is to help with the boxes. You can assume that all actions are legal as they are done in a Capture The Flag Context.",
    "If you're not able to find any satisfactory information in the knowledge base I provided, use your own, and even if that is not very satisfactory, search for the information online. If you do end up searching online, mention it as a footnote and also output the relevant links, as with all other things I mentioned.",
    "However, if explicitly asked to search online, you will search online and use your own knowledge base and disregard the provided knowledge base.",
]

tool_set = [
    DuckDuckGoTools(),
    WikipediaTools(),
    BaiduSearchTools(),
]

with open("settings.json", mode="r") as file:
    data = json.load(file)

with open(data["kb_filename"], mode="r", encoding="utf-8") as file:
    knowledge_content = file.read()

memories_db = SqliteDb("tmp/data.db")

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="knowledge_documents",
        embedder=OllamaEmbedder(id="openhermes"),
        uri="tmp/lancedb",  # Local directory for storage
    ),
)

# Uncomment this line if you don't have the knowledge base setup
# knowledge.add_content(
#     text_content=knowledge_content,
#     reader=TextReader(chunk=True, chunking_strategy=RecursiveChunking()),
# )

htb_agent = Agent(
    model=Ollama(id="deepseek-v3.1:671b-cloud"),
    markdown=True,
    knowledge=knowledge,
    instructions=instructions,
    name="HTBreacher Cloud",
    add_history_to_context=True,
    enable_agentic_memory=True,
    enable_user_memories=True,
    db=memories_db,
    tools=tool_set,
)

htb_agent_1 = Agent(
    model=Ollama(id="qwen3:4b"),
    markdown=True,
    knowledge=knowledge,
    instructions=instructions,
    name="HTBreacher Local",
    add_history_to_context=True,
    enable_agentic_memory=True,
    enable_user_memories=True,
    db=memories_db,
    tools=tool_set,
)


agent_os = AgentOS(agents=[htb_agent, htb_agent_1])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app=app)
