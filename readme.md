# 🛡️ Air-Gapped Codebase AI Assistant

A secure, offline-first AI system for exploring large, polyglot codebases using CrewAI, local LLMs, voice control, Git awareness, AST inspection, and Kubernetes context.

---

## 🚀 Features

- 💬 Natural language or voice chat interface to ask questions about your codebase
- 🧠 Multi-agent architecture with CrewAI, each agent specialized in a specific language or context domain
- 🔍 Hybrid search system: semantic vector search + AST-based structural detection + Git diff comparison
- 🎙️ Voice-to-text via Whisper + spoken answers via TTS
- 🔐 Fully offline — your proprietary code stays secure
- 📁 MCM support: cross-branch diffs, AST-based structural changes, and divergence analysis against default implementation
- 📄 Kubernetes YAML parsing with kubectl integration for config audits

---

## 🎯 Purpose

Traditional search (grep, symbols) is brittle in large, multilingual, and messy codebases. This system allows:

- Codebase questions like “Which methods emit Kafka?”
- Drift detection across Git branches
- Structured AST insights (e.g. added logic blocks)
- Real-time inspection of Kubernetes config and secrets
- Navigation of custom domain branches vs default integration (MCM-specific)

---

## 🧱 Architecture Overview

### Agent Specializations

| Agent              | Role                                                 | Special Tools                       |
|-------------------|------------------------------------------------------|-------------------------------------|
| `JavaAgent`        | Spring Boot & JPA                                   | Vector + Java AST                   |
| `GoAgent`          | gRPC & concurrency logic                            | Vector + Go AST                     |
| `PHPASTAgent`      | Legacy monoliths, web templates                     | Vector + PHP AST                    |
| `TSAstAgent`       | TypeScript SPA, NestJS handlers                     | Vector + TS AST                     |
| `PythonAgent`      | Scripting & utilities                               | Vector + Python AST                 |
| `DocsAgent`        | Documentation, Slack, business wikis                | Vector only                         |
| `KubernetesAgent`  | YAML, namespace, secrets, kubectl info              | PyYAML + subprocess `kubectl`       |
| `MCMGitDiffAgent`  | Cross-branch diffing for MCM v3 domains             | Git diff + TS AST diff + HTML view  |
| `ArchitectAgent`   | Orchestrates all agents for system-wide insight     | All tools combined                  |

---

## ⚙️ Configuration

This project uses a central `config` class to define key paths:

- `code_directory`: location of source code repositories (can include hundreds of Git repos)
- `docs_directory`: location of documentation files
- `slack_directory`: path for exported Slack JSON logs
- `mcm_pdf_path`: absolute path to the official MCM v3 reference PDF used for validation and structural comparison

---

## 🧪 Example Queries

- "What diverged in `domains/eg.mycontent.mobi` since the default integration?"
- "Where does Go code publish to Kafka?"
- "Does any handler override default logic outside its billing channel?"
- "What namespace is defined in the K8s YAML?"
- "Summarize what this Slack export says the issue being discussed, provide explination and additional context from other vector db entries."

---

## ✨ Early Enhancements

To improve reasoning accuracy, reduce hallucination, and enable long-term adaptability, the following enhancements are included by default in the initial build:

- **RAG Prompt Control**  
  All agents use strict prompt templates that instruct them to respond only using retrieved context, and to indicate when the context is insufficient.

- **Scoped Search Filtering**  
  Agents like `mcm_agent` and `docs_agent` have tools that limit vector search to only relevant tagged sources (e.g., `mcm_v3_arch_doc`), reducing irrelevant chunk injection.

- **Query Logging & Reflection (Optional)**  
  Every user question, retrieved context, and LLM response can be logged to JSON. This will support future ranking, error analysis, and the creation of hardcoded retrieval shortcuts.

- **Pluggable Embedding Models**  
  Embeddings for code, documentation, and Slack are treated separately and can be switched independently (e.g., `code-search-net` for code, `MiniLM` for docs).

- **Agent Memory Isolation**  
  Prompt history and tool interactions are isolated per agent for clearer traceability and to avoid cross-context bleed.

These choices lay the foundation for robust, interpretable behavior and future fine-tuning.

---

## 🛠️ To-Do / Improvements

### Git & Branch Comparison
- [x] Support branch diffs
- [x] Exclude billing channel folders from MCM diff
- [x] AST diff view of changed TypeScript methods
- [ ] Add HTML diff preview to main chat interface
- [ ] Link to IDE from diff view (e.g., `idea://open?...`)

### AST Tools
- [ ] Replace regex in Go and PHP with real parsers (`go/parser`, `php-parser`)
- [ ] Add structural matching of conditionals and switch blocks

### Kubernetes YAML
- [x] Parse secrets, configmaps, and namespaces
- [x] Support describe/get only (no apply/delete)
