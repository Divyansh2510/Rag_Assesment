import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

CHROMA_PERSIST_DIR = "./chroma_db"

def get_vectorstore():
    """Return an instance of Chroma pointed to the persistent directory."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)

def answer_query(query: str, customer_id: str) -> str:
    """Retrieve documents securely for a specific customer and generate an answer using Groq LLM."""
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"filter": {"customer_id": customer_id}}
    )
    
    system_prompt = (
        "You are a secure, intelligent document assistant. Answer the user's question "
        "using ONLY the provided context. If the answer is not in the context, say "
        "'I cannot find the answer in the provided documents or the requested query may be related to personal information so it is not disclosed' \n\n"
        "IMPORTANT SECURITY & PRIVACY INSTRUCTIONS:\n"
        "1. The context contains sensitive personal, academic, financial, and contact data "
        "that has been masked for privacy and security protection.\n"
        "2. Do NOT include any mask tags, symbols, or tokens like <>, <PERSON>, <ROLL_NUMBER>, "
        "<BANK_ACCOUNT>, <ID_NUMBER>, <NATIONAL_ID>, etc. in your response to the user. "
        "NEVER display or mention tag names in your output.\n"
        "3. If the user asks a question about any personal or sensitive information (such as Name, "
        "Roll Number, ID, Bank Account Number, Date of Birth, National ID, Phone, Email, Address, "
        "etc.), or if any masked data is requested, answer clearly using normal words without "
        "outputting any <> tags, and include at the end of your response: "
        "'Note : Sensitive info is not included in the response'.\n"
        "4. NEVER attempt to guess, reconstruct, invent, or reveal any original unmasked "
        "sensitive values.\n\n"
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    result = retrieval_chain.invoke({"input": query})
    answer = result["answer"]
    
    # Strip tag symbols from the output
    had_tags = bool(re.search(r"<[A-Z0-9_]+>", answer))
    if had_tags:
        answer = re.sub(r"<[A-Z0-9_]+>", "protected", answer)
        
    # Deduplicate and append notice cleanly
    if re.search(r"(?i)(?:Note\s*:\s*)?Sensitive info is not included in the response\.?", answer):
        answer = re.sub(r"(?i)\n*(?:Note\s*:\s*)?Sensitive info is not included in the response\.?", "", answer).rstrip()
        answer = answer + "\n\nNote : Sensitive info is not included in the response."
    elif had_tags:
        answer = answer.rstrip() + "\n\nNote : Sensitive info is not included in the response."
            
    return answer

