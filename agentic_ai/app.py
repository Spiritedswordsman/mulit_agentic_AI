import os
from dotenv import load_dotenv
load_dotenv()

pinecone_api = os.environ['pinecone_api']
groq_api_key = os.environ['GROQ_API_KEY']
gemini_api_key = os.environ['gemini_api_key']

#######################################
import os
import typer
from typing import Optional
from rich.prompt import Prompt

from agno.agent import Agent
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.pineconedb import PineconeDB
from phi.agent import Agent
from phi.model.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

from agno.embedder.google import GeminiEmbedder

import nltk
nltk.download('punkt_tab')

index_name = "thai-recipe-hybrid-search"

gemini_embed = GeminiEmbedder(api_key = gemini_api_key)



vector_db = PineconeDB(
    name=index_name,
    dimension=768,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
    api_key=pinecone_api,
    embedder=gemini_embed,
    use_hybrid_search=True,
    hybrid_alpha=0.5,
)

knowledge_base = WebsiteKnowledgeBase(
    urls=["https://docs.phidata.com/introduction"],
    max_links=10,
    vector_db=vector_db,
    embedder = gemini_embed,
)

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGoTools],
    knowledge=knowledge_base,
    show_tool_calls=True,
    search_knowledge=True,
)
# agent.knowledge.load(recreate=True)

agent.print_response("What is the history of Thai curry?", stream=True,markdown=True)