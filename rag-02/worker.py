from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import redis

#Environment Setup
load_dotenv()  # Carga las variables de entorno desde el archivo .env
client = OpenAI()
#choose embedding model must be the same as the one used in ingestion
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
#Connect to redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
#pull data out of the queue
def pull_from_queue():
    while True:
        payload = redis_client.blpop("query_queue", timeout=0)  # Block until a new query is available
        if payload:
            _, data = payload
            print(data)  # Convert string back to dictionary

pull_from_queue()