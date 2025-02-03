from langchain_milvus import Milvus
from langchain_huggingface import HuggingFaceEmbeddings

MILVUS_URL = "tcp://127.0.0.1:19530"
MODEL_EMBEDDING = "BAAI/bge-m3"

class MilvusVectorStore:

    def __init__(self):
        self.vector_store = self.load_retriever()

    @staticmethod
    def load_retriever():
        embedding = HuggingFaceEmbeddings(
            model_name=MODEL_EMBEDDING,
            model_kwargs={"device": "mps", "trust_remote_code": True},
            encode_kwargs={"normalize_embeddings": False},
        )

        vector_store = Milvus(
            connection_args={"uri": MILVUS_URL},
            embedding_function=embedding
        )

        return vector_store.as_retriever()

retriever = MilvusVectorStore.load_retriever()