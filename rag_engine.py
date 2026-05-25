import os
import pandas as pd
import chromadb

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
    StorageContext,
    Document
)

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore


def setup_models():
    Settings.llm = Ollama(
        model="llama3.1:8b",
        request_timeout=120
    )

    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text"
    )


def spreadsheet_to_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)

    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    else:
        return ""

    text_rows = []

    for index, row in df.iterrows():
        row_text = []

        for column in df.columns:
            value = row[column]

            if pd.notna(value):
                row_text.append(
                    f"{column}: {value}"
                )

        if row_text:
            text_rows.append(
                " | ".join(row_text)
            )

    return "\n".join(text_rows)


def load_documents_from_folder(folder_path):
    documents = []

    normal_files = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext in [".csv", ".xlsx", ".xls"]:
            text = spreadsheet_to_text(file_path)

            if text.strip():
                documents.append(
                    Document(
                        text=text,
                        metadata={
                            "file_name": filename,
                            "file_type": ext
                        }
                    )
                )

        else:
            normal_files.append(file_path)

    if normal_files:
        loaded_docs = SimpleDirectoryReader(
            input_files=normal_files
        ).load_data()

        documents.extend(loaded_docs)

    return documents


def build_persistent_index_from_folder(
    folder_path,
    persist_dir="./chroma_db",
    collection_name="risk_assessment_docs"
):
    setup_models()

    documents = load_documents_from_folder(folder_path)

    chroma_client = chromadb.PersistentClient(
        path=persist_dir
    )

    chroma_collection = chroma_client.get_or_create_collection(
        collection_name
    )

    vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

    return index


def query_uploaded_documents(folder_path, question):
    index = build_persistent_index_from_folder(folder_path)

    query_engine = index.as_query_engine(
        similarity_top_k=8
    )

    response = query_engine.query(question)

    return str(response)
