import json
import os

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

JSON_PATH = "data/shl_product_catalog.json"
VECTOR_PATH = "data/faiss"

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

documents = []

for item in catalog:

    text = f"""
Name: {item.get("name")}

Description:
{item.get("description")}

Job Levels:
{", ".join(item.get("job_levels", []))}

Languages:
{", ".join(item.get("languages", []))}

Duration:
{item.get("duration")}

Categories:
{", ".join(item.get("keys", []))}
"""

    metadata = {
        "name": item.get("name"),
        "url": item.get("link"),
        "test_type": ", ".join(item.get("keys", [])),
        "duration": item.get("duration"),
        "job_levels": item.get("job_levels"),
        "remote": item.get("remote"),
        "adaptive": item.get("adaptive"),
    }

    documents.append(
        Document(
            page_content=text,
            metadata=metadata,
        )
    )

print(f"Loaded {len(documents)} assessments")

vectorstore = FAISS.from_documents(
    documents,
    embedding,
)

os.makedirs(VECTOR_PATH, exist_ok=True)

vectorstore.save_local(VECTOR_PATH)

print("Vectorstore created.")