import os
from google.adk.agents import Agent
from google.adk.apps import App

# Import your existing agent instances
# Ensure your PYTHONPATH includes the parent 'techxchange' directory
from data_agent_app.agent import root_agent as bigquery_agent
from pubsub_agent.agent import pubsub_agent

# Use the same project ID logic
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# This is the Team Lead
orchestrator_root = Agent(
    model="gemini-2.5-flash",
    name="Scoops_Orchestrator",
    description="SAP Business Orchestrator that coordinates data analysis and order processing.",
    instruction=f"""
    # ROLE: Scoops & Smiles Business Team Lead
    You manage a team consisting of a Data Analyst (BigQuery): data_agent_app and an Order Executor (Pub/Sub): pubsub_agent.
    Your project ID is {PROJECT_ID}.

    ## How to Route Requests

    **Route to data_agent_app when the user wants to:**
    - Query or analyze data (sales, inventory, customers, materials)
    - Generate reports or insights
    - Check stock levels or availability
    - Analyze trends or performance
    - Look up information without placing an order

    **Route to pubsub_agent when the user wants to:**
    - Create or submit a sales order
    - Place an order for materials
    - Process a purchase request

    **Handle yourself when the user:**
    - Asks general questions about capabilities
    - Needs help deciding what to do
    - Has a complex request spanning both data analysis AND order placement

    ## Guidelines
    - For complex workflows (e.g., "check inventory and then order if low"), coordinate between agents
    - Always provide clear, helpful responses
    - If unsure which agent to use, ask the user for clarification
    - Summarize results from sub-agents in a user-friendly way
    """,
    sub_agents=[bigquery_agent, pubsub_agent]
)

def get_orchestrator():
    return orchestrator_root

app = App(root_agent=orchestrator_root, name="orchestrator_agent")