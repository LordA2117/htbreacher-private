from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.models.ollama import Ollama
from dotenv import load_dotenv
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.os import AgentOS
import os
import json

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
# print(api_key)

with open("settings.json", mode="r") as file:
    data = json.load(file)

with open(data["kb_filename"], mode="r", encoding="utf-8") as file:
    knowledge_content = file.read()

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="knowledge_documents",
        embedder=OllamaEmbedder(id="openhermes"),
        uri="tmp/lancedb",  # Local directory for storage
    ),
)


knowledge.add_content(text_content=knowledge_content)

htb_agent = Agent(
    model=Ollama(id="deepseek-v3.1:671b-cloud"),
    markdown=True,
    # knowledge=knowledge,
    instructions=[
        "Always check your knowledge base for answers. It is your primary source of information. You are an agent with the knowledge to perform attacks based on the Knowledge Base I provided. If it doesn't exist here, check your own knowledge base, but specify that you did so."
    ],
    name="HTBreacher",
)

agent_os = AgentOS(agents=[htb_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app=app)
