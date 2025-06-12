# Summer Camp Chatbot - Backend

A FastAPI-based backend service for an AI-powered summer camp discovery chatbot. The system uses LangGraph for intelligent conversation flow and integrates with Supabase for camp data storage.

## Architecture

### Core Components

- **FastAPI**: Web framework for REST API endpoints
- **LangGraph**: AI agent orchestration with state management
- **Google Gemini**: Large language model for natural language processing
- **Supabase**: Database for camp data storage and retrieval
- **LangSmith**: Optional tracing and monitoring for AI workflows

### Key Features

- Intelligent intent classification (search, filter, general conversation)
- Session-based conversation memory
- Dynamic camp search with natural language queries
- Real-time filtering of cached results
- Contextual response generation

## Project Structure

```
backend/
├── agents/
│   ├── camp_agent_dynamic.py    # Main AI agent with LangGraph workflow
│   ├── state.py                 # Conversation state management
│   └── tools/
│       └── database_tools.py    # LangGraph tool definitions
├── api/
│   └── chat.py                  # FastAPI chat endpoints
├── database/
│   └── supabase_client.py       # Supabase database client
├── models/
│   └── schemas.py               # Pydantic data models
├── config.py                    # Application configuration
├── main.py                      # FastAPI application entry point
└── requirements.txt             # Python dependencies
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# API Configuration
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Database Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# LLM Configuration
LLM_PROVIDER=gemini  # or "openai"
GOOGLE_API_KEY=your_google_api_key  # Required for Gemini
GEMINI_MODEL=gemini-pro  # Optional, defaults to gemini-pro
OPENAI_API_KEY=your_openai_api_key  # Required if using OpenAI
OPENAI_MODEL=gpt-3.5-turbo  # Optional, defaults to gpt-3.5-turbo

# LangSmith Configuration (Optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=summer-camp-chatbot

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## LLM Configuration

The chatbot supports two LLM providers:

1. **Gemini (Default)**
   - Set `LLM_PROVIDER=gemini`
   - Requires `GOOGLE_API_KEY`
   - Optional: `GEMINI_MODEL` (defaults to "gemini-pro")

2. **OpenAI**
   - Set `LLM_PROVIDER=openai`
   - Requires `OPENAI_API_KEY`
   - Optional: `OPENAI_MODEL` (defaults to "gpt-3.5-turbo")

## Setup Instructions

### 1. Environment Setup

Create a `.env` file in the backend directory:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Google AI Configuration
GOOGLE_API_KEY=your_google_gemini_api_key
GEMINI_MODEL=gemini-pro

# LangSmith Configuration (Optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=summer-camp-chatbot

# Application Configuration
APP_NAME=Summer Camp Chatbot API
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Ensure your Supabase database has the following tables:
- `organizations`
- `locations` 
- `camps`
- `camp_sessions`
- `categories`
- `camp_categories`

### 4. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```
Returns application health status.

### Chat Endpoint
```
POST /api/v1/chat
```

**Request Body:**
```json
{
  "message": "Find soccer camps for 8 year olds",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I found 5 soccer camps suitable for 8-year-olds...",
  "session_id": "generated-or-provided-session-id",
  "context": {
    "intent": "search",
    "search_count": 5,
    "conversation_length": 2,
    "has_cached_results": true
  }
}
```

## AI Agent Workflow

The system uses a sophisticated LangGraph workflow:

1. **Intent Classification**: Determines if the user wants to search, filter, or have general conversation
2. **Conditional Routing**: 
   - `search`: Query database for new camps
   - `filter`: Filter existing cached results
   - `general`: Generate conversational response
3. **Response Generation**: Create contextual, helpful responses using Gemini

### Session Management

- Each conversation maintains state across multiple messages
- Cached search results persist within sessions
- Intent classification considers conversation history

## Testing

### Run Database Tests
```bash
python test_camp_search.py
```

### Run Chat Tests
```bash
python test_chat.py
```

### Get Available Categories
```bash
python get_categories.py
```

## Configuration Options

### LangSmith Integration
Enable detailed AI workflow tracing by setting:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_api_key
LANGCHAIN_PROJECT=your_project_name
```

### CORS Configuration
Update `CORS_ORIGINS` in `.env` to allow requests from your frontend domain.

### Model Selection
Change `GEMINI_MODEL` to use different Gemini variants:
- `gemini-pro`
- `gemini-pro-vision`

## Development

### Adding New Features
1. Update state models in `agents/state.py`
2. Add new nodes to the LangGraph workflow in `camp_agent_dynamic.py`
3. Create corresponding API endpoints in `api/`
4. Update database schemas in `models/schemas.py`

### Debugging
- Enable debug mode: `DEBUG=true` in `.env`
- Check logs for detailed workflow execution
- Use LangSmith for AI workflow visualization

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **supabase**: Database client
- **langgraph**: AI agent orchestration
- **langchain-google-genai**: Google AI integration
- **python-dotenv**: Environment variable management
- **pydantic-settings**: Configuration management
- **langsmith**: AI workflow monitoring
