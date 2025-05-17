from crewai import Task, Crew
from crew_agents import architect_agent, java_agent, go_agent, php_agent, docs_agent, ts_agent

print("\n💬 Ask your question about the codebase:")
user_input = input("> ")

# You can swap in java_agent, go_agent, etc. if you want to route directly
task = Task(
    description=user_input,
    agent=architect_agent
)

crew = Crew(
    agents=[architect_agent, java_agent, go_agent, php_agent, docs_agent, ts_agent],
    tasks=[task],
    verbose=True
)

print("\n🧠 AI is thinking...")
result = crew.run()

print("\n✅ Answer:\n")
print(result)