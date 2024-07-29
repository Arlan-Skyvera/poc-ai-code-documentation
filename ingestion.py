from llama_index.core import (
    SimpleDirectoryReader,
    PropertyGraphIndex,
)

from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

from transformations.codesplitter import DynamicCodeSplitter

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from dotenv import load_dotenv
from typing import Literal

import openai
import nest_asyncio
import asyncio

nest_asyncio.apply()

openai.api_key = "<api_key>"

load_dotenv()

reader = SimpleDirectoryReader('./xml', recursive=True, num_files_limit=50)
documents = reader.load_data()

graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="password",
    url="neo4j+s://a8265be6.databases.neo4j.io:7687",
)

# entities = Literal["MODULE", "CLASS", "FUNCTION", "ARGUMENT", "VARIABLE", "FILE", "LANGUAGE", "DOCUMENTATION", "COMMENTS"]
# relations = Literal["CONTAINS", "INHERITS_FROM", "IMPLEMENTS", "CALLS", "DECLARES", "HAS_ARGUMENT", "WRITTEN_IN", "DEPENDS_ON", "DEFINED_IN"]
# schema = {
#     "MODULE": [
#         "CONTAINS", "DEPENDS_ON"
#     ],
#     "CLASS": [
#         "CONTAINS", "INHERITS_FROM", "IMPLEMENTS", "DECLARES", "DEPENDS_ON", "DEFINED_IN"
#     ],
#     "FUNCTION": [
#         "CONTAINS", "CALLS", "HAS_ARGUMENT", "DECLARES", "DEFINED_IN"
#     ],
#     "ARGUMENT": [
#         "HAS_ARGUMENT"
#     ],
#     "VARIABLE": [
#         "DECLARES"
#     ],
#     "FILE": [
#         "CONTAINS", "WRITTEN_IN", "DEPENDS_ON", "DEFINED_IN"
#     ],
#     "DOCUMENTATION": [
#         "CONTAINS", "WRITTEN_IN"
#     ],
#     "COMMENTS": [
#         "WRITTEN_IN"
#     ],
#     "LANGUAGE": [
#         "WRITTEN_IN"
#     ]
# }

index = PropertyGraphIndex.from_documents(
    documents,
    embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
    kg_extractors=[
        SchemaLLMPathExtractor(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.0),
            # possible_entities=entities,
            # possible_relations=relations,
            # kg_validation_schema=schema
        )
    ],
    property_graph_store=graph_store,
    show_progress=True,
    use_async=True
)