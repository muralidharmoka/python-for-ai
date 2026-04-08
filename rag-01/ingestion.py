from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

file_path = "./example_data/layout-parser-paper.pdf"
loader = PyPDFLoader("./data.pdf")

#EN V Setup
load_dotenv()  # Carga las variables de entorno desde el archivo .env

#Configuration
PDF_FILE_PATH = "data.pdf"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "docs_en"

#STEP1 LODING THE PDF
loader = PyPDFLoader(file_path=PDF_FILE_PATH)
pdf_docs = loader.load()

#STEP2 SPLIT THE DOCUMENT INTO CHUNKS
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunk_documents = text_splitter.split_documents(pdf_docs)

# #STEP3 PRINT THE CHUNKS
# for i, chunk in enumerate(chunk_documents):
#     print(f"Chunk {i}:")
#     print(chunk.page_content)
#     print("\n--------------------------------------------\n")

#STEP3 CREATE THE EMBEDDINGS - choose the embedding model you want to use, for example, OpenAI's text-embedding-3-large
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#STEP 4: STORE THE CHUNKS IN VECTOR DATABASE
qdrant = QdrantVectorStore.from_documents(
    documents=chunk_documents
    , embedding=embeddings
    , collection_name=COLLECTION_NAME
    , url=QDRANT_URL
)   

print("Ingestion completed successfully!")