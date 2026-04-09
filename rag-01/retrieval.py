from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

#Environment Setup
load_dotenv()  # Carga las variables de entorno desde el archivo .env
client = OpenAI()

#choose embedding model must be the same as the one used in ingestion
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#Connect to Qdrant and specify the collection name
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "docs_en"
vector_db = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
    embedding=embeddings
)

#Accept user query
query = input("HUMAN INPUT: ")

context_blcoks = []

#RUN A SIMILARITY SEARCH for user query in vector database
search_results = vector_db.similarity_search(query=query)
print("SIMILAR DOCUMENTS:")
for results in search_results:
    block = f""" 
    Page Content: {results.page_content} \n 
    Page Number: {results.metadata.get('page_number')} \n 
    -------------------------------------------- \n"""
    context_blcoks.append(block)

#System prompt for the LLM call
system_prompt = f"""You are a RAG AI assistant. 
You have been given content extracted from a PDF document. \n

Each section contains:
- Page Content: The text content of the page \n
- Page Number: The page number from which the content was extracted \n
Use the following content to answer the user's question: \n
if the answer exists in the content, provide the answer along with the page number. \n

If the answer is not found in the content, say "Sorry, I couldn't find the answer in the provided content." \n
Here is the content: \n
Do not addd outside information, only use the content provided below: \n
{context_blcoks} \n
User's question: {query}
"""

response = client.responses.create(
    model="gpt-4o", 
    instructions=system_prompt,
    input=query
)

print(response.output_text)