import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader, JSONLoader, CSVLoader, PyPDFLoader
from langchain.vectorstores import Chroma
from src.util import get_config, get_logger

class DocumentProcessor:
    def __init__(self):
        self.logger = get_logger(self)
        self.config = get_config()

    def process_documents(self):
        EXTENSIONS = [".java", ".go", ".ts", ".php", ".py"]
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        all_chunks = []

        # 1. Load and split source code files
        for root, _, files in os.walk(Config.code_directory):
            for file in files:
                if any(file.endswith(ext) for ext in EXTENSIONS):
                    loader = TextLoader(os.path.join(root, file))
                    docs = loader.load()
                    chunks = splitter.split_documents(docs)
                    all_chunks.extend(chunks)

        # 2. Load and split documentation files
        for root, _, files in os.walk(Config.docs_directory):
            for file in files:
                if file.endswith(".md") or file.endswith(".txt"):
                    loader = TextLoader(os.path.join(root, file))
                    docs = loader.load()
                    chunks = splitter.split_documents(docs)
                    all_chunks.extend(chunks)

        # 3. Load and split Slack JSON exports
        for root, _, files in os.walk(Config.slack_directory):
            for file in files:
                if file.endswith(".json"):
                    loader = JSONLoader(os.path.join(root, file))
                    docs = loader.load()
                    chunks = splitter.split_documents(docs)
                    all_chunks.extend(chunks)

        # 4. Load and split CSV files
        for root, _, files in os.walk(Config.code_directory):
            for file in files:
                if file.endswith(".csv"):
                    loader = CSVLoader(os.path.join(root, file))
                    docs = loader.load()
                    chunks = splitter.split_documents(docs)
                    all_chunks.extend(chunks)

        # 5. Special: Load and tag MCM v3 PDF documentation
        mcm_pdf_path = Path("/Users/justinrobinson/Documents/mcmv3-doc.pdf")
        if os.path.exists(mcm_pdf_path):
            loader = PyPDFLoader(mcm_pdf_path)
            docs = loader.load()
            chunks = splitter.split_documents(docs)
            for c in chunks:
                c.metadata["source"] = "mcm_v3_arch_doc"
            all_chunks.extend(chunks)
            self.logger.info(f"📘 Loaded and tagged MCM PDF with {len(chunks)} chunks")

        # 6. Embed and store in Chroma
        self.logger.info(f"🔢 Total chunks to embed: {len(all_chunks)}")
        vectorstore = Chroma.from_documents(all_chunks, embedding=embedding, persist_directory="vector_store")
        self.logger.info("✅ All documents indexed into Chroma.")
