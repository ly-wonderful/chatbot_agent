# Summer Camp Chatbot

An intelligent AI-powered chatbot for discovering and searching summer camps. The system combines natural language processing with a comprehensive camp database to help parents find the perfect summer programs for their children.

## 🏕️ Overview

The Summer Camp Chatbot uses advanced AI to understand natural language queries and provide personalized camp recommendations. Users can search by activity type, location, age group, budget, and other criteria through conversational interactions.

### Key Features

- **Natural Language Search**: "Find soccer camps for 8-year-olds in California"
- **Intelligent Filtering**: Refine results through follow-up questions
- **Session Memory**: Maintains conversation context across multiple queries
- **Real-time Responses**: Fast, contextual responses powered by Google Gemini
- **Comprehensive Database**: Extensive camp data with locations, pricing, and details

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **LangGraph**: AI agent orchestration and workflow management
- **Google Gemini**: Large language model for natural language understanding
- **Supabase**: PostgreSQL database with real-time capabilities
- **LangSmith**: AI workflow monitoring and debugging (optional)

### Frontend
- **Next.js 14**: React framework with App Router
- **React 18**: Modern React with hooks and concurrent features
- **CSS3**: Custom responsive styling

## 📁 Project Structure

```
test2/
├── backend/                     # FastAPI backend service
│   ├── agents/                  # AI agent logic and tools
│   │   ├── camp_agent_dynamic.py   # Main LangGraph workflow
│   │   ├── state.py                # Conversation state management
│   │   └── tools/                  # Database tools for AI agent
│   ├── api/                     # REST API endpoints
│   ├── database/                # Database client and queries
│   ├── models/                  # Pydantic data models
│   ├── config.py               # Application configuration
│   ├── main.py                 # FastAPI application entry
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Next.js frontend application
│   ├── app/                    # Next.js App Router pages
│   ├── components/             # React components
│   │   └── ChatInterface.js    # Main chat interface
│   ├── package.json           # Node.js dependencies
│   └── next.config.js         # Next.js configuration
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**: For backend development
- **Node.js 18+**: For frontend development
- **Supabase Account**: For database hosting
- **Google AI API Key**: For Gemini integration

### 1. Clone the Repository

```bash
git clone <repository-url>
cd test2
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API keys and database credentials

# Run the backend server
python main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install Node.js dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# AI Configuration
GOOGLE_API_KEY=your_google_gemini_api_key
GEMINI_MODEL=gemini-pro

# Optional: LangSmith Monitoring
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=summer-camp-chatbot

# Application Settings
DEBUG=true
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Database Schema

The application requires the following Supabase tables:

- **organizations**: Camp organizations and providers
- **locations**: Geographic locations for camps
- **camps**: Main camp information (name, description, pricing)
- **camp_sessions**: Specific camp sessions with dates and times
- **categories**: Camp activity categories (sports, arts, academic, etc.)
- **camp_categories**: Many-to-many relationship between camps and categories

## 🤖 How It Works

### AI Workflow

1. **Intent Classification**: The system analyzes user input to determine intent:
   - `search`: Find new camps in the database
   - `filter`: Refine existing search results
   - `general`: Handle conversational queries

2. **Dynamic Routing**: Based on intent, the system routes to appropriate handlers:
   - Database search for new queries
   - In-memory filtering for refinements
   - General conversation responses

3. **Context-Aware Responses**: The AI generates responses considering:
   - Previous conversation history
   - Current search results
   - User's apparent preferences

### Example Conversation

```
User: "Hi, I'm looking for summer camps for my 8-year-old"
Bot: "I'd be happy to help you find camps! What activities is your 8-year-old interested in?"

User: "Soccer camps in California"
Bot: "I found 12 soccer camps in California suitable for 8-year-olds. Here are the top options..."

User: "What about the first three?"
Bot: "Here are details for the first three soccer camps: [detailed information]"

User: "Any under $200 per week?"
Bot: "From your search results, here are the soccer camps under $200/week..."
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Test database connectivity
python test_camp_search.py

# Test chat API endpoints
python test_chat.py

# View available camp categories
python get_categories.py
```

### Frontend Testing

The frontend can be tested by:
1. Running the development server (`npm run dev`)
2. Opening `http://localhost:3000` in a browser
3. Interacting with the chat interface

## 📚 API Documentation

### Chat Endpoint

**POST** `/api/v1/chat`

Request:
```json
{
  "message": "Find art camps for teenagers",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "response": "I found 8 art camps perfect for teenagers...",
  "session_id": "generated-session-id",
  "context": {
    "intent": "search",
    "search_count": 8,
    "conversation_length": 1,
    "has_cached_results": true
  }
}
```

### Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "app": "Summer Camp Chatbot API"
}
```

## 🎯 Use Cases

- **Parents**: Find camps matching their child's interests and schedule
- **Camp Organizers**: Showcase their programs to interested families
- **Educational Consultants**: Research camp options for clients
- **Travel Planners**: Discover camps in specific geographic regions

## 🔄 Development Workflow

1. **Feature Development**: Add new capabilities to the AI agent
2. **Database Updates**: Extend the schema for new camp attributes
3. **Frontend Enhancements**: Improve the user interface and experience
4. **Testing**: Ensure all components work together seamlessly
5. **Deployment**: Deploy to production environments

## 📈 Performance Optimization

- **Caching**: Search results are cached within user sessions
- **Efficient Queries**: Database queries are optimized for performance
- **Lazy Loading**: Frontend components load as needed
- **Session Management**: Minimal server-side state storage

## 🔐 Security Considerations

- **API Keys**: Stored securely in environment variables
- **CORS**: Configured to allow only specified frontend domains
- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Consider implementing for production use

## 🚀 Deployment

### Production Deployment

1. **Backend**: Deploy to cloud platforms like Railway, Heroku, or AWS
2. **Frontend**: Deploy to Vercel, Netlify, or similar static hosting
3. **Database**: Use Supabase production instance
4. **Monitoring**: Enable LangSmith for AI workflow monitoring

### Docker Support

Both frontend and backend can be containerized using Docker for consistent deployment across environments.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support:
- Check the individual README files in `backend/` and `frontend/` directories
- Review the test files for usage examples
- Consult the API documentation above

---

Built with ❤️ for families seeking the perfect summer camp experience.
