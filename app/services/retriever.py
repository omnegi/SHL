from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

db = FAISS.load_local(
    "data/faiss",
    embedding,
    allow_dangerous_deserialization=True,
)


def search_assessments(query: str, k: int = 20):
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": 30,
        },
    )

    return retriever.invoke(query)