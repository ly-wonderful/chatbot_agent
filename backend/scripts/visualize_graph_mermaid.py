import asyncio
from app.agents.camp_agent_dynamic import CampAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def visualize_graph():
    """Generate Mermaid diagram for the three-agent camp search system"""
    mermaid = """
```mermaid
flowchart TD
    Start(["Start"]) --> Agent1["Agent 1: Collect Profile"]
    
    %% Agent 1 - Profile Collection
    Agent1 --> ProfileSteps["Profile Collection Steps"]
    ProfileSteps --> Name["Name"]
    ProfileSteps --> ChildName["Child's Name"]
    ProfileSteps --> ChildAge["Child's Age"]
    ProfileSteps --> ChildGrade["Child's Grade"]
    ProfileSteps --> Interests["Interests"]
    ProfileSteps --> Address["Address"]
    ProfileSteps --> MaxDistance["Max Distance"]
    ProfileSteps --> ProfileComplete["Profile Complete"]
    
    %% Agent 2 - SQL Query & Database Search
    ProfileComplete --> Agent2["Agent 2: Generate SQL Query"]
    Agent2 --> ConvertFilters["Convert Profile to Filters"]
    ConvertFilters --> GradeFilter["Grade Level Filter"]
    ConvertFilters --> LocationFilter["Location & Distance Filter"]
    ConvertFilters --> InterestsFilter["Interests Filter"]
    ConvertFilters --> CategoriesFilter["Categories Filter"]
    
    Agent2 --> DatabaseSearch["Execute Database Search"]
    DatabaseSearch --> QueryDB["Query Supabase Database"]
    DatabaseSearch --> DistanceCalc["Apply Distance Calculations"]
    DatabaseSearch --> FilterResults["Filter by Grade & Interests"]
    
    %% Agent 3 - Table Formatting
    FilterResults --> Agent3["Agent 3: Format Table"]
    Agent3 --> ProcessResults["Process Search Results"]
    ProcessResults --> ExtractInfo["Extract Camp Information"]
    ProcessResults --> FormatLocation["Format Location Data"]
    ProcessResults --> FormatPrice["Format Price Information"]
    
    Agent3 --> GenerateTable["Generate Markdown Table"]
    GenerateTable --> TableOutput["Camp Name | Organization | Location | Grades | Price | Distance | Description"]
    GenerateTable --> TopResults["Top 10 Results Displayed"]
    GenerateTable --> Summary["Summary & Next Steps"]
    
    Summary --> End(["End"])
    
    %% Subgraphs for better organization
    subgraph Agent1Group["Agent 1: Profile Collector"]
        Agent1
        ProfileSteps
        Name
        ChildName
        ChildAge
        ChildGrade
        Interests
        Address
        MaxDistance
        ProfileComplete
    end
    
    subgraph Agent2Group["Agent 2: SQL Query & Database Search"]
        Agent2
        ConvertFilters
        GradeFilter
        LocationFilter
        InterestsFilter
        CategoriesFilter
        DatabaseSearch
        QueryDB
        DistanceCalc
        FilterResults
    end
    
    subgraph Agent3Group["Agent 3: Table Formatter"]
        Agent3
        ProcessResults
        ExtractInfo
        FormatLocation
        FormatPrice
        GenerateTable
        TableOutput
        TopResults
        Summary
    end
    
    %% Styling
    classDef system fill:#b3e6ff,stroke:#333,stroke-width:2px
    classDef agent fill:#ffb3b3,stroke:#333,stroke-width:2px
    classDef process fill:#ffffb3,stroke:#333,stroke-width:2px
    classDef data fill:#b3ffb3,stroke:#333,stroke-width:2px
    classDef output fill:#ffb3ff,stroke:#333,stroke-width:2px
    classDef subgraph fill:#f5f5f5,stroke:#333,stroke-width:1px
    
    class Start,End system
    class Agent1,Agent2,Agent3 agent
    class ProfileSteps,ConvertFilters,DatabaseSearch,ProcessResults,GenerateTable process
    class Name,ChildName,ChildAge,ChildGrade,Interests,Address,MaxDistance,GradeFilter,LocationFilter,InterestsFilter,CategoriesFilter,QueryDB,DistanceCalc,FilterResults,ExtractInfo,FormatLocation,FormatPrice data
    class ProfileComplete,TableOutput,TopResults,Summary output
    class Agent1Group,Agent2Group,Agent3Group subgraph
```
"""
    print(mermaid)
    logger.info("Mermaid diagram generated")

if __name__ == "__main__":
    visualize_graph() 