# 🧳 AI Travel Planner

A multi-agent travel planning application that creates comprehensive itineraries using Azure AI Foundry's agent orchestration capabilities.


## ⚠️ Important Disclaimer

**This is a demonstration application.** The Flight Agent and Hotel Agent generate realistic-looking fictional data for demonstration purposes only. This application is **not connected to any real travel booking APIs** or live travel data sources. Please do not use this information for actual travel planning or booking.



## 🤖 How It Works

This application uses a **multi-agent architecture** built in Azure AI Foundry to generate detailed travel itineraries.


### Agent Architecture

- **🎯 Itinerary Agent (Supervisor)**: Coordinates all other agents and assembles the final itinerary
- **✈️ Flight Agent**: Provides flight options and recommendations
- **🏨 Hotel Agent**: Finds accommodation options
- **🏛️ Attractions Agent**: Discovers local attractions and activities
- **🍽️ Food Agent**: Recommends restaurants and dining experiences


### Process Flow

1. User inputs travel details (origin, destination, dates)
2. Itinerary Agent receives the request and coordinates with specialized agents
3. Each agent works on their domain expertise
4. Itinerary Agent assembles all information into a comprehensive travel plan


## ⚡ Powered By

- **Azure AI Foundry**: Multi-agent orchestration platform
- **Streamlit**: Web application framework
- **GPT-4**: Large language models for intelligent responses