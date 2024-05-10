from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, StorageContext, load_index_from_storage,PromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.tools import RetrieverTool
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import RouterRetriever

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
app = FastAPI()
#sasd
class HybridRetriever(BaseRetriever):
    def __init__(self, vector_retriever, bm25_retriever):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        super().__init__()

    def _retrieve(self, query, **kwargs):
        bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)
        vector_nodes = self.vector_retriever.retrieve(query, **kwargs)

        # combine the two lists of nodes
        all_nodes = []
        node_ids = set()
        for n in bm25_nodes + vector_nodes:
            if n.node.node_id not in node_ids:
                all_nodes.append(n)
                node_ids.add(n.node.node_id)
        return all_nodes
#embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
print("sdasd")
llm = TogetherLLM(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_base="https://api.together.xyz/v1",
    api_key="1c006a785da00c29211ad62e70fdd8da47a52803af9c4b2821d03cb444b6689f",
    is_chat_model=True,
    is_function_calling_model=True,
    temperature=0.1,
)


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en",embed_batch_size=10)
print("sdasadasdsadsd")
Settings.llm=llm
Settings.embed_model=embed_model
Settings.chunk_size= 1000
Settings.chunk_overlap= 20






# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./persist_data")


try:
    print("Attempting to load index from storage...")
    index = load_index_from_storage(storage_context=storage_context)
    print("Index loaded successfully.")
    
    print("Initializing vector retriever...")
    vector_retriever = VectorIndexRetriever(index)
    print("Vector retriever initialized.")
    
    print("Initializing BM25 retriever...")
    bm25_retriever = BM25Retriever.from_defaults(index=index, similarity_top_k=2)
    print("BM25 retriever initialized.")
    
except Exception as e:
    print(f"An error occurred: {e}")

index.as_retriever(similarity_top_k=5)

hybrid_retriever = HybridRetriever(vector_retriever, bm25_retriever)
retriever_tools = [
    RetrieverTool.from_defaults(
        retriever=vector_retriever,
        description="Useful in most cases",
    ),
    RetrieverTool.from_defaults(
        retriever=bm25_retriever,
        description="Useful if searching about specific information",
    ),
]
retriever = RouterRetriever.from_defaults(
    retriever_tools=retriever_tools,
    llm=llm,
    select_multi=True,
)
reranker = SentenceTransformerRerank(top_n=4, model="BAAI/bge-reranker-base")
# load index


class MessageBody(BaseModel):
    message: str


query_engine = RetrieverQueryEngine.from_args(
    retriever=hybrid_retriever,
    node_postprocessors=[reranker],
    llm=llm,
    similarity_top_k=4,
     response_mode="tree_summarize",
)

new_summary_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge,never answer general knowledge , always use context , NEVER MAKE MENTION OF THE CONTEXT, dont mention the context at all , just answer the question"
    "make response formatted well , seperate paragraphs and stuff , DONT MENTION WHERE THE INFORMATION WAS TAKEN FROM OR MENTION IT JUST ANSWER THE QUESTION"
    "Dont mention where the answer was drawn from or any of the prior rules i set for you , never say things like 'Based on the context given'\n"
    "Query: {query_str}\n"
    "Answer: "
)
# output everything in their expected html format ,make sure to add some appropriate breaks where needed , 
new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)
query_engine.update_prompts(
    {"response_synthesizer:summary_template": new_summary_tmpl}
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/message/") 
async def sendMessage(message: MessageBody): 
    response = query_engine.query(message.message)
    print(response)
    return {"response":response,"message":message.message}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

