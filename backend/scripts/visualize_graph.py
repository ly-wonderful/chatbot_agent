import asyncio
from app.agents.camp_agent_dynamic import CampAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def visualize_graph():
    """Visualize the camp agent workflow using ASCII art"""
    workflow = """
Three-Agent Camp Search System
=============================

[Start] --> [Agent 1: Collect Profile]
    |
    |--> [Profile Collection Steps]
    |     |
    |     |--> [Name]
    |     |--> [Child's Name]
    |     |--> [Child's Age]
    |     |--> [Child's Grade]
    |     |--> [Interests]
    |     |--> [Address]
    |     |--> [Max Distance]
    |     |
    |     |--> [Profile Complete]
    |
    |--> [Agent 2: Generate SQL Query]
    |     |
    |     |--> [Convert Profile to Filters]
    |     |     |
    |     |     |--> [Grade Level Filter]
    |     |     |--> [Location & Distance Filter]
    |     |     |--> [Interests Filter]
    |     |     |--> [Categories Filter]
    |     |
    |     |--> [Execute Database Search]
    |           |
    |           |--> [Query Supabase Database]
    |           |--> [Apply Distance Calculations]
    |           |--> [Filter by Grade & Interests]
    |
    |--> [Agent 3: Format Table]
          |
          |--> [Process Search Results]
          |     |
          |     |--> [Extract Camp Information]
          |     |--> [Calculate Distances]
          |     |--> [Format Location Data]
          |     |--> [Format Price Information]
          |
          |--> [Generate Markdown Table]
                |
                |--> [Camp Name | Organization | Location | Grades | Price | Distance | Description]
                |
                |--> [Top 10 Results Displayed]
                |
                |--> [Summary & Next Steps]

Agent Responsibilities:
======================

Agent 1 - Profile Collector:
- Collects user and child information
- Validates input data
- Manages conversation flow
- Ensures complete profile before proceeding

Agent 2 - SQL Query Generator & Database Search:
- Converts profile to search filters
- Generates appropriate database queries
- Executes searches with distance calculations
- Handles database errors and timeouts

Agent 3 - Table Formatter:
- Processes raw database results
- Formats data into readable table
- Extracts key information (name, location, price, etc.)
- Provides summary and next action suggestions

Workflow Features:
=================
- Sequential processing through three specialized agents
- Profile-driven search with automatic filtering
- Distance-based camp matching
- Clean table output with key information
- Error handling at each step
- Personalized responses using child's name

Node Types:
- Start/End: System nodes
- Profile Collection: Input collection nodes
- SQL Generation: Data processing nodes
- Database Search: External service nodes
- Table Formatting: Output formatting nodes
"""
    print(workflow)
    logger.info("Workflow visualization printed")

if __name__ == "__main__":
    visualize_graph() 