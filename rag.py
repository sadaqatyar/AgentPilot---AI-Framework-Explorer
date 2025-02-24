import os
import dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# ✅ Load environment variables
dotenv.load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING-V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# ✅ Function to Load & Process Documents
def load_documents():
    """Loads documents from the web and splits them into chunks."""
    loader = WebBaseLoader("https://python.langchain.com/docs/tutorials/")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(documents)

# ✅ Load and split documents
chunks = load_documents()

# ✅ Generate Embeddings & Store in FAISS
embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(chunks, embedder)

# ✅ Define Retriever
retriever = RunnableLambda(vectorstore.similarity_search)

# ✅ Define LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# ✅ Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a LangChain assistant. Answer the user's question using only the given context."),
    ("user", "Question: {question}\nContext:\n{context}")
])

# ✅ Define RAG Chain
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# ✅ Function to process queries
def process_query(user_query):
    """Processes the user's query using the RAG pipeline."""
    if not user_query.strip():
        return "⚠️ Please enter a valid query."
    return rag_chain.invoke(user_query)  # ✅ Returns only one value

# ✅ Main Execution
def process_query(user_query, source="LangChain", llm="Gemini 2.0"):
    """
    Process user query using the selected WebBase Loader source and LLM model.
    """
    # ✅ Select WebBase Loader Source
    if source == "LangChain":
        loader = WebBaseLoader("https://python.langchain.com")
    elif source == "CrewAI":
        loader = WebBaseLoader("https://crewai.com")
    elif source == "LangGraph":
        loader = WebBaseLoader("https://langgraph.com")
    elif source == "PhiData":
        loader = WebBaseLoader("https://phidata.com")
    else:
        raise ValueError("Invalid source selected!")

    # ✅ Load and Process Documents
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # ✅ Choose LLM Model
    if llm == "Gemini 2.0":
        llm_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    elif llm == "Gemini 1.5":
        llm_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    else:
        raise ValueError("Invalid LLM model selected!")

    # ✅ Generate Embeddings & Store in FAISS
    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embedder)

    # ✅ Define Retriever
    retriever = RunnableLambda(vectorstore.similarity_search)

    # ✅ Define Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a LangChain assistant. Answer the user's question using only the given context."),
        ("user", "Question: {question}\nContext:\n{context}")
    ])

    # ✅ Define RAG Chain
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm_model

    # ✅ Process User Query
    return rag_chain.invoke(user_query)
  # ✅ Print the response correctly
