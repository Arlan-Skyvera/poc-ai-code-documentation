from llama_index.vector_stores.neo4jvector import Neo4jVectorStore

from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext

from llama_index.core.memory import ChatMemoryBuffer

from dotenv import load_dotenv

import openai

openai.api_key = "<api_key>"

load_dotenv()

vector_store = Neo4jVectorStore(
    username="neo4j",
    password="poc-documentation",
    url="bolt://localhost:7687",
    embedding_dimension=1536,
    database="poc",
)

index = VectorStoreIndex.from_vector_store(vector_store)

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        "You are a senior software engineer that helps junior developers get onboarded to the codebase."
    )
)

message = input("Arlan: ")

while message != 'exit':
    response = chat_engine.chat(message)
    print(f"AI: {response}")
    message = input("Arlan: ")