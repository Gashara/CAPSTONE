
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings ,StorageContext,VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en",embed_batch_size=10)
Settings.embed_model=embed_model

reader = SimpleDirectoryReader("data")
documents=[]
try:
  print("Loading Documents from data folder to memory...")
  documents = reader.load_data()
  print("Documents Loaded")
except:
  print("An exception occurred with Loading Documents")


try:
  print("Getting nodes from documents...")
  nodes = SentenceSplitter(chunk_size=512).get_nodes_from_documents(documents)
  print("Nodes Loaded")
except:
  print("An exception occurred with Getting Nodes")
  
storage_context = StorageContext.from_defaults()
try:
  print("Loading nodes into the docstore...")
  storage_context.docstore.add_documents(nodes)
  print("Nodes Loaded into Docstore")
except:
  print("An exception occurred with Storing Nodes")

try:
  print("Indexing Nodes and Documents...")
  index = VectorStoreIndex(
    nodes=nodes,
    storage_context=storage_context,
    )
  print("Nodes and Documents Indexed")
except:
  print("An exception occurred with Indexing Nodes and Documents")

try:
  print("Persisting Data...")
  storage_context.persist("persist_data")
  index.storage_context.persist("persist_data")
  print("Data Persisted")
except:
  print("An exception occurred with Persisting Data")

