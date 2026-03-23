from langchain.chains import RetrievalQA
from langchain.chat_models import OllamaChat

# Load vector store (if saved)
vector_store = FAISS.load_local("rag_faiss_index", embeddings)

# Define retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Connect RAG chain to Ollama
llm = OllamaChat(model="all-minillm:33m")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # can use "map_reduce" or "refine" for longer docs
    retriever=retriever,
    return_source_documents=True
)

# Example query
query = "What are the steps to register a startup in Tunisia?"
result = qa_chain(query)

print("Answer:\n", result["result"])
print("Sources:\n", [doc.metadata["source"] for doc in result["source_documents"]])
