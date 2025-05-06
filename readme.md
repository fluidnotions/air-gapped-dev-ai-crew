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
- "Summarize what this Slack export says about the invoice pipeline."

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
- [ ] Add RBAC analysis
