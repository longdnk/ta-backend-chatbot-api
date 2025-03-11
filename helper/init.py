import os

from tqdm import tqdm
from pymilvus import MilvusClient
from langchain_milvus import Milvus
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

MILVUS_URL = os.getenv("MILVUS_URL")
MODEL_EMBEDDING = "BAAI/bge-m3"
path_pdfs = "documents/"

client = MilvusClient(uri=MILVUS_URL)

def init_knowledge_base():

    unique_texts = {}
    docs_processed = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n\n", "\n\n", "\n", ".", " ", "", "•", "  ", "   "],
    )

    for file in tqdm(os.listdir(path_pdfs)):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(path_pdfs, file)
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            for doc in tqdm(documents):
                new_docs = text_splitter.split_documents([doc])
                for new_doc in tqdm(new_docs):
                    if new_doc.page_content not in unique_texts:
                        unique_texts[new_doc.page_content] = True
                        docs_processed.append(new_doc)

    all_splits = text_splitter.split_documents(docs_processed)

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_EMBEDDING,
        model_kwargs={"device": "cpu", "trust_remote_code": True},
        encode_kwargs={'normalize_embeddings': True},
    )

    vectorstore = Milvus.from_documents(
        documents=all_splits,
        embedding=embeddings,
        connection_args={"uri": MILVUS_URL},
        drop_old=True,
    )
    return vectorstore
