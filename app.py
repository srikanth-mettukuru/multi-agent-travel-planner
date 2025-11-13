import streamlit as st
import os
import time
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, ClientSecretCredential

load_dotenv()

# Connect to your Azure AI Foundry project
# Check if we have service principal credentials
if os.getenv('AZURE_CLIENT_ID') and os.getenv('AZURE_CLIENT_SECRET') and os.getenv('AZURE_TENANT_ID'):
    credential = ClientSecretCredential(
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET')
    )    
else:
    credential = DefaultAzureCredential()
    
project = AIProjectClient(
    endpoint=os.getenv('AZURE_AI_PROJECT_ENDPOINT'),
    credential=credential,
    project_name=os.getenv('AZURE_AI_PROJECT_NAME')
)

st.set_page_config(page_title="AI Travel Planner", page_icon="🧭", layout="wide")

# Sidebar with app information
st.sidebar.title("🤖 Multi-Agent System")
st.sidebar.markdown("---")

st.sidebar.markdown("### How It Works")
st.sidebar.markdown("""
This travel planner uses a **multi-agent architecture** to create comprehensive itineraries:
""")

st.sidebar.markdown("#### 🎯 Supervisor Agent")
st.sidebar.markdown("""
- Coordinates all other agents
- Receives your travel request
- Delegates tasks to specialized agents
- Assembles the final itinerary
""")

st.sidebar.markdown("#### ✈️ Flight Agent")
st.sidebar.markdown("""
- Provides flight options
""")

st.sidebar.markdown("#### 🏨 Hotel Agent")
st.sidebar.markdown("""
- Finds accommodation options
""")

st.sidebar.markdown("#### 🏛️ Attractions Agent")
st.sidebar.markdown("""
- Discovers local attractions

""")

st.sidebar.markdown("#### 🍽️ Food Agent")
st.sidebar.markdown("""
- Recommends restaurants
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Process Flow")
st.sidebar.markdown("""
1. **Input Processing**: Supervisor receives your travel details
2. **Task Delegation**: Each agent works on their specialty
3. **Information Gathering**: Agents collect relevant data
4. **Coordination**: Supervisor organizes all findings
5. **Final Assembly**: Complete itinerary is generated
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Powered By")
st.sidebar.markdown("""
- **Azure AI Foundry**
- **Multi-Agent Orchestration**
- **GPT-4 Models**
""")

# Main content
st.title("🧳 AI Travel Planner")
st.write("Plan your next adventure with AI-powered itinerary suggestions using our multi-agent system.")

# Add disclaimer
st.warning(
    "⚠️ **Important Disclaimer:** This is a demonstration application. "
    "The Flight Agent and Hotel Agent generate realistic-looking fictional data for "
    "demonstration purposes only. This application is **not connected to any real travel "
    "booking APIs** or live travel data sources. Please do not use this information for "
    "actual travel planning or booking."
)

col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origin City", placeholder="London")
    start_date = st.date_input("Start Date")

with col2:
    destination = st.text_input("Destination City", placeholder="Boston")
    end_date = st.date_input("End Date")

if st.button("Generate Itinerary", type="primary", use_container_width=True):
    if not all([origin, destination, start_date, end_date]):
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Multi-agent system is working on your itinerary..."):
            user_prompt = (
                f"I want to travel from {origin} to {destination} "
                f"between {start_date} and {end_date}. "
                f"Generate a detailed travel itinerary with flights, hotels, attractions, and restaurants."
            )

            try:
                # Create thread and run
                run = project.agents.create_thread_and_run(
                    agent_id=os.getenv('AZURE_AI_AGENT_ID'),
                    thread={
                        "messages": [
                            {"role": "user", "content": user_prompt}
                        ]
                    }
                )

                # Wait for completion
                while run.status in ["queued", "in_progress"]:
                    time.sleep(2)
                    run = project.agents.runs.get(thread_id=run.thread_id, run_id=run.id)

                # Get the response messages
                messages = project.agents.messages.list(thread_id=run.thread_id)
                messages_list = list(messages)

                # Display the assistant's response
                if messages_list:
                    assistant_messages = [msg for msg in messages_list if msg.role == "assistant"]
                    
                    if assistant_messages:
                        assistant_message = assistant_messages[0]
                        if hasattr(assistant_message, 'content') and assistant_message.content:
                            result_text = assistant_message.content[0].text.value
                            st.success("Your Multi-Agent Generated Itinerary:")
                            st.markdown(result_text)
                        else:
                            st.error("Unable to retrieve itinerary. Please try again.")
                    else:
                        st.error("No response received. Please try again.")
                else:
                    st.error("No messages found. Please try again.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please try again or check your connection.")