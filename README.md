# 🛡️ Secure RAG Enterprise Vault

> **A privacy-first, multi-tenant document intelligence system powered by RAG (Retrieval-Augmented Generation)**

Query your confidential documents using natural language — with zero PII exposure. Every name, ID, bank account, Aadhaar number, and contact detail is automatically detected and masked before storage.

---

## ✨ Key Features

- 🔒 **Automatic PII Masking** — 14 custom entity types detected and anonymized before any data is stored
- 🏢 **Multi-Tenant Isolation** — Customer_A, Customer_B, Customer_C operate in completely separate namespaces
- 🤖 **LLM-Powered Q&A** — Ask questions in plain English; get intelligent answers from your documents
- 📄 **PDF Support** — Upload any confidential PDF (Admit Cards, Bank Statements, Financial Reports)
- 🛡️ **Zero Leakage Architecture** — Raw PII never touches the vector database
- ⚡ **Fast Inference** — Powered by Groq's ultra-low-latency LLaMA 3.1 API

---

## 🚀 Demo

### Document Upload & Masking
Upload a PDF → the system automatically extracts text, detects all PII, replaces it with anonymized labels, and stores only the masked version in the vector database.

### Natural Language Query
Ask: *"What is the account number mentioned in the document?"*
The system retrieves relevant context and responds: *"The account number is protected. Note: Sensitive info is not included in the response."*

---

## 🗂️ Project Structure

```
Rag_Assesment/
│
├── app.py                    # Streamlit frontend — main entry point
│
├── utils/
│   ├── pii_masker.py         # PII detection & masking engine (Presidio)
│   ├── vector_store.py       # Document ingestion & ChromaDB management
│   ├── llm_chain.py          # RAG query chain & Groq LLM integration
│   └── __init__.py           # Package initializer
│
├── chroma_db/                # ChromaDB persistent storage (auto-generated)
├── data/                     # Sample / test data
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── .env                      # API keys (never committed to Git)
├── requirements.txt          # Python dependencies
└── .gitignore
```

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **RAG Framework** | LangChain 0.2.x |
| **Vector Database** | ChromaDB (local, disk-persisted) |
| **Embedding Model** | `all-MiniLM-L6-v2` (HuggingFace, runs locally) |
| **LLM** | Groq API — LLaMA 3.1 8B Instant |
| **PII Detection** | Microsoft Presidio + 14 custom recognizers |
| **NLP Backbone** | spaCy `en_core_web_lg` |
| **PDF Parsing** | PyPDF (via LangChain) |

---

## 🛡️ PII Entities Detected & Masked

The system automatically detects and anonymizes all of the following:

| Entity | Examples |
|---|---|
| `PERSON` | Candidate names, honorifics (Mr./Dr./Shri), Indian surnames |
| `ROLL_NUMBER` | Exam roll numbers, hall ticket numbers, seat numbers |
| `ID_NUMBER` | Application IDs, registration numbers, candidate IDs |
| `BANK_ACCOUNT` | Account numbers, A/c No, IBAN |
| `FINANCIAL_CODE` | IFSC, MICR, SWIFT/BIC, CIF, routing numbers |
| `CREDIT_CARD` | Card numbers, CVV, ATM PIN |
| `NATIONAL_ID` | Aadhaar, PAN, Passport, Driving License, Voter ID, GSTIN |
| `DATE_OF_BIRTH` | DOB in any format |
| `DEMOGRAPHIC` | Age, Gender, Category (GEN/OBC/SC/ST/EWS) |
| `PHONE_NUMBER` | Indian mobile numbers, international formats |
| `EMAIL_ADDRESS` | Email addresses |
| `ADDRESS` | Postal addresses, PIN codes, ZIP codes |
| `PASSWORD` | Password, secret key, token values |
| `CLIENT_ID` | client_id, tenant_id fields |

---

## 🔧 Setup & Installation

### Prerequisites
- Python 3.9 or higher
- A free [Groq API Key](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Divyansh2510/Rag_Assesment.git
cd Rag_Assesment
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ `torch` and `sentence-transformers` are large packages. Installation may take a few minutes.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your-groq-api-key-here"
```

Get your free API key at [console.groq.com](https://console.groq.com/).

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📖 How to Use

### Step 1 — Select Tenant
In the left sidebar, select a workspace tenant: **Customer_A**, **Customer_B**, or **Customer_C**. Each tenant is fully isolated.

### Step 2 — Upload a Document
Go to the **"Document Ingestion & PII Vault"** tab:
- Click **"Select PDF Document"** and choose any PDF
- Optionally check **"Replace existing workspace documents"** to clear previous uploads
- Click **"🚀 Upload & Mask"**

The system will extract text, mask all PII, embed the content, and store it in ChromaDB.

### Step 3 — Query Your Documents
Go to the **"Secure Intelligence Query"** tab:
- Type your question in natural language
- Click **"💬 Submit Query"**
- The LLM will retrieve relevant context and return a privacy-safe answer

---

## 🔐 Security Design

| Layer | How It's Handled |
|---|---|
| **PII at ingestion** | Masked before embedding — never stored in raw form |
| **Tenant isolation** | Every chunk tagged with `customer_id`; retrieval is always filtered by tenant |
| **LLM output** | System prompt forbids revealing masked values; output is post-processed to strip leaked tokens |
| **API keys** | Stored in `.env`, excluded from Git via `.gitignore` |
| **Cross-tenant leakage** | ChromaDB metadata filter enforces complete namespace separation |

---

## 📋 Requirements

```
streamlit
langchain==0.2.17
langchain-core==0.2.43
langchain-community==0.2.19
langchain-classic==1.0.4
langchain-text-splitters==0.2.4
langchain-groq
chromadb
torch
torchvision
sentence-transformers
presidio-analyzer
presidio-anonymizer
pypdf
python-dotenv
spacy
https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a [GitHub Issue](https://github.com/Divyansh2510/Rag_Assesment/issues).

---

## 📄 License

This project is developed as part of a RAG system assessment. All rights reserved.

---

<p align="center">
  Built with ❤️ using Python · Streamlit · LangChain · ChromaDB · Microsoft Presidio · Groq
</p>
