from crewai import Agent
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

from ast_toolkit import JavaASTTool, PythonASTTool, GoASTTool, TypeScriptASTTool, PHPASTTool
from git_and_k8s_tools import GitTool, K8sYAMLTool
from mcm_git_diff_tool import MCMGitDiffTool

# Load vector store
vectorstore = Chroma(persist_directory="vector_store", embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

class CodebaseQueryTool:
    def __init__(self, label, filter_keyword=None):
        self.label = label
        self.filter_keyword = filter_keyword

    def search(self, query):
        results = vectorstore.similarity_search(query, k=5)
        if self.filter_keyword:
            results = [doc for doc in results if self.filter_keyword.lower() in doc.metadata.get("source", "").lower()]
        return f"[{self.label} results]\n" + "\n---\n".join([doc.page_content for doc in results])

# Tool instances
java_tool = CodebaseQueryTool("Java", ".java")
go_tool = CodebaseQueryTool("Go", ".go")
php_tool = CodebaseQueryTool("PHP", ".php")
ts_tool = CodebaseQueryTool("TS", ".ts")
py_tool = CodebaseQueryTool("Python", ".py")
docs_tool = CodebaseQueryTool("Docs")

# LLMs
java_llm = Ollama(model="deepseek-coder")
go_llm = Ollama(model="codellama")
php_llm = Ollama(model="code-llama")
ts_llm = Ollama(model="code-llama")
py_llm = Ollama(model="codellama")
docs_llm = Ollama(model="mistral")
architect_llm = Ollama(model="llama3")
k8s_llm = Ollama(model="mistral")
mcm_llm = Ollama(model="code-llama")

# AST tools
java_ast_tool = JavaASTTool("data/code")
python_ast_tool = PythonASTTool("data/code")
go_ast_tool = GoASTTool("data/code")
ts_ast_tool = TypeScriptASTTool("data/code")
php_ast_tool = PHPASTTool("data/code")

# External tools
git_tool = GitTool("data/code")
k8s_yaml_tool = K8sYAMLTool("data/code")
mcm_diff_tool = MCMGitDiffTool("data/code/mcm")  # specify correct MCM repo path

# Agents
docs_agent = Agent(
    role="Documentation Researcher",
    goal="Search through wikis, Slack logs, and notes to find context.",
    backstory="You specialize in synthesizing business knowledge from unstructured sources.",
    tools=[docs_tool.search],
    llm=docs_llm,
    verbose=True
)

java_agent = Agent(
    role="Java Microservice Analyst",
    goal="Analyze Java services for architecture, dependencies, and data flow.",
    backstory="You are an expert in Java and Spring Boot systems.",
    tools=[java_tool.search, java_ast_tool.search],
    llm=java_llm,
    verbose=True
)

go_agent = Agent(
    role="Go Backend Specialist",
    goal="Understand Go services and their concurrency logic.",
    backstory="You are proficient in idiomatic Go and microservices.",
    tools=[go_tool.search, go_ast_tool.search],
    llm=go_llm,
    verbose=True
)

php_agent = Agent(
    role="Legacy PHP Analyst",
    goal="Understand legacy PHP systems, logic, and integrations.",
    backstory="You analyze old PHP monoliths and service connectors.",
    tools=[php_tool.search, php_ast_tool.search],
    llm=php_llm,
    verbose=True
)

ts_agent = Agent(
    role="Frontend TS Analyst",
    goal="Analyze TypeScript UI services and component flow.",
    backstory="You specialize in TypeScript SPA logic and frontend structure.",
    tools=[ts_tool.search, ts_ast_tool.search],
    llm=ts_llm,
    verbose=True
)

py_agent = Agent(
    role="Python Utility Reviewer",
    goal="Understand Python tools, scripts, and support services.",
    backstory="You assist in identifying utility patterns and logic across scripts.",
    tools=[py_tool.search, python_ast_tool.search],
    llm=py_llm,
    verbose=True
)

kubernetes_agent = Agent(
    role="Kubernetes Config Inspector",
    goal="Explore and answer questions about Kubernetes YAML configs, labels, namespaces, secrets, and config maps.",
    backstory="You use YAML parsing and kubectl to analyze the cluster state and config files, but never modify anything.",
    tools=[k8s_yaml_tool.find_metadata, k8s_yaml_tool.describe, k8s_yaml_tool.get],
    llm=k8s_llm,
    verbose=True
)

mcm_agent = Agent(
    role="MCM Git Diff & Divergence Analyst",
    goal="Help detect deviations from the MCM v3 default implementation by comparing domain branches and flagging unexpected changes outside allowed customization areas.",
    backstory=(
        "You are an expert in the MCM v3 architecture, which is a modular TypeScript/NestJS platform structured for domain isolation. "
        "Each integration is expected to customize billing channel logic exclusively under `src/aggregator/channels/<network>/<billing_channel>`, "
        "based on a default implementation rooted in `aggregator/hyve`. However, in practice, domain branches (e.g., domains/ng.mycontent.mobi) often contain changes outside these paths, "
        "leading to fragile or undocumented behavior.\n\n"
        "Your job is to:\n"
        "- Compare a given domain branch to the reference (e.g., default-integration).\n"
        "- Exclude changes inside the channels directory.\n"
        "- Highlight all other diffs, per line.\n"
        "- Additionally, perform AST-based inspection of changed TypeScript files, focusing on inserted logic inside method bodies (like conditionals or guards).\n\n"
        "This allows developers to quickly identify where integration-specific logic has leaked into shared layers, breaking intended modularity."
    ),
    tools=[
        ts_tool.search,
        git_tool.checkout_branch,
        git_tool.grep_file,
        mcm_diff_tool.diff_to_html
    ],
    llm=mcm_llm,
    verbose=True
)

architect_agent = Agent(
    role="Lead Software Architect",
    goal="Answer questions using knowledge from all code and context sources.",
    backstory="You coordinate multiple specialists to generate accurate system-level insights.",
    tools=[
        java_tool.search, go_tool.search, php_tool.search,
        ts_tool.search, py_tool.search, docs_tool.search,
        java_ast_tool.search, python_ast_tool.search,
        go_ast_tool.search, ts_ast_tool.search, php_ast_tool.search,
        k8s_yaml_tool.find_metadata, k8s_yaml_tool.describe,
        git_tool.checkout_branch, git_tool.grep_file,
        mcm_diff_tool.diff_to_html
    ],
    llm=architect_llm,
    verbose=True
)
