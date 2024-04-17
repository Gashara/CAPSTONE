from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings


app = FastAPI()
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


llm = TogetherLLM(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_base="https://api.together.xyz/v1",
    api_key="1c006a785da00c29211ad62e70fdd8da47a52803af9c4b2821d03cb444b6689f",
    is_chat_model=True,
    is_function_calling_model=True,
    temperature=0.1,
)


Settings.llm=llm
Settings.embed_model=embed_model
Settings.chunk_size= 1000
Settings.chunk_overlap= 20

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
)


class MessageBody(BaseModel):
    message: str


query_engine = index.as_query_engine()


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

