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

st.set_page_config(page_title="AI Travel Planner", page_icon="🧭")
st.title("🧳 AI Travel Planner")
st.write("Plan your next adventure with AI-powered itinerary suggestions.")

# --- User Inputs ---
origin = st.text_input("Origin City", placeholder="e.g., Nashville, TN")
destination = st.text_input("Destination City", placeholder="e.g., Boston, MA")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Generate Itinerary"):
    if not all([origin, destination, start_date, end_date]):
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Building your personalized itinerary..."):
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
                            st.success("🎉 Your Itinerary:")
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