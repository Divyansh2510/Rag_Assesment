import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.vector_store import process_and_store_document, clear_customer_documents
from utils.llm_chain import answer_query

# 1. Setup Page Configuration
st.set_page_config(
    page_title="Secure RAG Enterprise Vault",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inject Premium Custom CSS & Typography
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hero Banner Card */
    .hero-banner {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #CBD5E1;
        margin: 0;
        font-weight: 400;
    }

    /* Sidebar Badge Cards */
    .sidebar-badge {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-left: 4px solid #6366F1;
        border-radius: 10px;
        padding: 16px;
        margin-top: 14px;
        font-size: 0.92rem;
        line-height: 1.6;
        color: #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .sidebar-badge b {
        color: #818CF8;
    }

    /* Streamlit Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 0 28px;
        background-color: rgba(30, 41, 59, 0.65);
        border-radius: 10px 10px 0 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94A3B8;
        font-weight: 600;
        font-size: 1.02rem;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
    }

    /* Button Hover & Glow Animations */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 28px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(99, 102, 241, 0.6);
        background: linear-gradient(135deg, #818CF8 0%, #6366F1 100%);
    }

    /* Response Answer Card */
    .response-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.45);
        border-radius: 14px;
        padding: 26px 30px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    .response-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #A855F7;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .response-body {
        font-size: 1.08rem;
        line-height: 1.7;
        color: #F8FAFC;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Sidebar - Tenant Workspace Selection
with st.sidebar:
    st.markdown("## 🔒 System Security Context")
    current_customer_id = st.selectbox(
        "🏢 Active Workspace Tenant",
        options=["Customer_A", "Customer_B", "Customer_C"],
        index=0,
        help="Select the tenant workspace. Documents and embeddings are strictly isolated by workspace ID."
    )
    
    st.markdown(
        """
        <div class="sidebar-badge">
            <b>🔐 Zero-Leakage Tenant Isolation</b><br>
            Each tenant workspace operates in an isolated cryptographic & vector namespace. Documents cannot bleed across workspaces.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="sidebar-badge" style="border-left-color: #A855F7;">
            <b>🛡️ Enterprise PII Protection</b><br>
            Automated deep masking of:<br>
            • <b>Names & Titles</b><br>
            • <b>Admit Card Roll & Exam IDs</b><br>
            • <b>Bank Accounts & Financial Codes</b><br>
            • <b>National IDs (PAN, Aadhaar)</b><br>
            • <b>Contact Details & DOB</b>
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. Main Area Header Card
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🛡️ Secure RAG Enterprise Vault</div>
        <p class="hero-subtitle">Zero-Leakage Multi-Tenant Document Intelligence with Comprehensive Automated PII Masking</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Interactive Tabs
tab1, tab2 = st.tabs(["📄 Document Ingestion & PII Vault", "💬 Secure Intelligence Query"])

# --- Tab 1: Upload Documents ---
with tab1:
    st.markdown("### 📤 Ingest Documents into Secure Vault")
    st.markdown("Upload any confidential PDF document (Admit Cards, Bank Statements, Financial Reports). Our pipeline automatically detects and redacts all PII before vector storage.")
    
    st.markdown(
        """
        <div class="sidebar-badge" style="border-left-color: #38BDF8; margin-top: 0px; margin-bottom: 16px;">
            <b>💡 Multi-Document vs. Single-Document Mode:</b><br>
            By default, uploading new PDFs <i>adds</i> them to this workspace's existing knowledge base (which is why older documents like a Resume can appear alongside a newer Offer Letter).<br>
            • To query <b>only</b> your newly uploaded file without older documents, keep <b>"Replace existing workspace documents"</b> checked below or click <b>"🗑️ Clear Workspace"</b>.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_clear_opt, col_btn_clear = st.columns([3, 1])
    with col_clear_opt:
        replace_existing = st.checkbox(
            "🧽 Replace existing workspace documents (clear older PDFs from this tenant before upload)",
            value=True,
            help="If checked, removes older documents (like previously uploaded Resumes) from this tenant's vector store so only the new PDF is queried."
        )
    with col_btn_clear:
        if st.button("🗑️ Clear Workspace"):
            if clear_customer_documents(current_customer_id):
                st.success(f"✅ All stored documents cleared for workspace: **{current_customer_id}**")
            else:
                st.error("❌ Failed to clear workspace documents.")
    
    uploaded_file = st.file_uploader("Select PDF Document", type="pdf", label_visibility="collapsed")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        upload_btn = st.button("🚀 Upload & Mask")
        
    if upload_btn:
        if uploaded_file is not None:
            with st.spinner("Encrypting, Redacting PII, and Indexing Document..."):
                try:
                    if replace_existing:
                        clear_customer_documents(current_customer_id)
                        
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    success = process_and_store_document(tmp_file_path, current_customer_id)
                    
                    if success:
                        st.success(f"✅ Document successfully masked and stored in workspace: **{current_customer_id}**")
                    else:
                        st.error("❌ Failed to process the document.")
                        
                    os.unlink(tmp_file_path)
                except Exception as e:
                    st.error(f"❌ An error occurred during upload: {e}")
        else:
            st.warning("⚠️ Please select a PDF file to upload first.")

# --- Tab 2: Query System ---
with tab2:
    st.markdown("### 🔍 Query Your Protected Documents")
    st.markdown("Ask natural language questions against your tenant workspace. The assistant retrieves relevant chunks without exposing masked personal data.")
    
    user_query = st.text_input("Enter your query:", placeholder="e.g. What is the Roll Number or Account Number mentioned in the document?")
    
    col_submit, _ = st.columns([1, 4])
    with col_submit:
        query_btn = st.button("💬 Submit Query")
        
    if query_btn:
        if user_query.strip() == "":
            st.warning("⚠️ Please enter a valid question.")
        else:
            with st.spinner("Retrieving secure context and generating response..."):
                try:
                    answer = answer_query(user_query, current_customer_id)
                    st.markdown(
                        f"""
                        <div class="response-card">
                            <div class="response-header">✨ Secure Assistant Response</div>
                            <div class="response-body">{answer}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"❌ Failed to execute query. Make sure documents are uploaded for this customer. Error: {e}")

