from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


@lru_cache(maxsize=1)
def get_db():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        "data/faiss",
        embedding,
        allow_dangerous_deserialization=True,
    )


def search_assessments(query: str, k: int = 20):
    db = get_db()

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": 30,
        },
    )

    return retriever.invoke(query)