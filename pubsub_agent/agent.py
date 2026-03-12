import os
import google.auth
from google.adk.agents import Agent
from google.adk.tools.pubsub.config import PubSubToolConfig
from google.adk.tools.pubsub.pubsub_credentials import PubSubCredentialsConfig
from google.adk.tools.pubsub.pubsub_toolset import PubSubToolset
from google.adk.apps import App

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TOPIC_NAME = f"projects/{PROJECT_ID}/topics/test-topic"

# 1. Credentials
credentials, _ = google.auth.default()
credentials_config = PubSubCredentialsConfig(credentials=credentials)

# 2. Toolset
tool_config = PubSubToolConfig(project_id=PROJECT_ID)
pubsub_toolset = PubSubToolset(
    credentials_config=credentials_config, 
    pubsub_tool_config=tool_config
)

# 3. Enhanced Instructions for SAP Integration
instruction = f"""
You are the 'SAP Order Bridge' agent for the Scoops & Smiles Lab.
Your goal is to collect Sales Order details and publish them to Pub/Sub in a JSON format.

### MANDATORY FIELDS & DEFAULTS
If the user does not provide these, notify them you are using these defaults:
- SalesOrganization: "1010"
- DistributionChannel: "10"
- OrganizationDivision: "00"
- OrderType: "OR"
- SoldToParty: "CUSTOMER_01" (Suggest they provide their Customer ID)

### ITEM LEVEL DEFAULTS
- RequestedQuantityUnit: "PC"

### PROTOCOL
1. Listen for order requests (e.g., "I want to order 50 Mango Tubs").
2. Check if Material, Quantity, and Customer are clear.
3. If information is missing, ask the user and mention the defaults you will use otherwise.
4. When ready, format the data into a JSON object with 'header' and 'items' keys.
5. Publish the JSON string to topic: {TOPIC_NAME}

### OUTPUT JSON STRUCTURE EXAMPLE
{{
  "header": {{
    "SalesOrderType": "OR",
    "SalesOrganization": "1010",
    "DistributionChannel": "10",
    "OrganizationDivision": "00",
    "SoldToParty": "USER_VALUE"
  }},
  "items": [
    {{
      "Material": "MANGO_01",
      "RequestedQuantity": "50",
      "RequestedQuantityUnit": "PC"
    }}
  ]
}}
"""

# 4. Agent Definition
pubsub_agent = Agent(
    model="gemini-2.5-flash",
    name="pubsub_agent",
    description="Transforms user requests into SAP Sales Order JSON messages for Pub/Sub.",
    instruction=instruction,
    tools=[pubsub_toolset],
)

def get_pubsub_agent():
    return root_agent

app = App(root_agent=pubsub_agent, name="pubsub_agent")