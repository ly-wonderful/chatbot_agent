# Summer Camp Chatbot Backend

A FastAPI-based backend for an intelligent summer camp search chatbot that helps parents find the perfect camps for their children.

## 🏗️ Project Structure

```
backend/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration settings
│   ├── api/                      # API routes and endpoints
│   │   ├── __init__.py
│   │   └── chat.py              # Chat API endpoints
│   ├── agents/                   # AI agents and workflows
│   │   ├── __init__.py
│   │   ├── camp_agent_dynamic.py # Main camp search agent
│   │   ├── llm_utils.py         # LLM utility functions
│   │   └── tools/               # Agent tools
│   │       ├── __init__.py
│   │       └── database_tools.py
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   └── supabase_client.py   # Supabase client
│   ├── models/                   # Data models and schemas
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── distance_utils.py    # Distance calculation utilities
├── tests/                        # Test files
│   ├── __init__.py
│   ├── test_three_agent_system.py
│   ├── test_camp_search.py
│   ├── test_chat.py
│   ├── test_distance_search.py
│   └── test_supabase.py
├── scripts/                      # Utility scripts
│   ├── collect_user_profile.py
│   ├── get_categories.py
│   └── visualize_graph.py
├── docs/                         # Documentation and visualizations
│   ├── camp_agent_workflow.mmd
│   └── camp_agent_workflow
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the application:**
   ```bash
   python -m app.main
   ```

4. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

## 🧪 Testing

The project includes comprehensive tests for all components:

- **Agent Tests**: Test the three-agent workflow system
- **API Tests**: Test the FastAPI endpoints
- **Database Tests**: Test Supabase integration
- **Utility Tests**: Test distance calculations and other utilities

Run specific tests:
```bash
# Test the three-agent system
python tests/test_three_agent_system.py

# Test the API
python tests/test_chat.py

# Test database functionality
python tests/test_supabase.py
```

## 🏛️ Architecture

### Three-Agent System

The chatbot uses a three-agent architecture:

1. **Profile Collector Agent**: Collects user and child information
2. **SQL Query Generator Agent**: Converts profile to database search filters
3. **Table Formatter Agent**: Formats search results for display

### Key Components

- **FastAPI**: Web framework for the API
- **LangGraph**: Workflow orchestration
- **Supabase**: Database and authentication
- **Google Maps API**: Distance calculations
- **Gemini/OpenAI**: LLM providers

## 🔧 Configuration

Key configuration options in `app/config.py`:

- **LLM Provider**: Choose between Gemini and OpenAI
- **Database**: Supabase connection settings
- **API Keys**: Google Maps, LLM providers
- **CORS**: Cross-origin resource sharing settings

## 📊 API Endpoints

- `POST /api/v1/chat`: Main chat endpoint
- `GET /api/v1/chat/health`: Health check
- `GET /health`: Application health check

## 🤝 Contributing

1. Follow the established project structure
2. Add tests for new features
3. Update documentation as needed
4. Use proper logging and error handling

## 📝 License

This project is licensed under the MIT License.
