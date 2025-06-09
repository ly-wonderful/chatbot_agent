# Summer Camp Chatbot - Frontend

A modern React/Next.js frontend for the Summer Camp Chatbot application. Provides an intuitive chat interface for users to discover and search for summer camps using natural language.

## Features

- **Real-time Chat Interface**: Seamless conversation experience with the AI chatbot
- **Session Management**: Maintains conversation context across multiple messages
- **Responsive Design**: Works across desktop and mobile devices
- **Loading States**: Visual feedback during AI processing
- **Session Tracking**: Displays session ID for debugging and continuity

## Technology Stack

- **Next.js 14**: React framework with App Router
- **React 18**: Modern React with hooks
- **CSS3**: Custom styling with Flexbox layouts
- **Fetch API**: HTTP client for backend communication

## Project Structure

```
frontend/
├── app/
│   ├── globals.css              # Global styles and chat interface CSS
│   ├── layout.js                # Root layout component
│   └── page.js                  # Home page
├── components/
│   └── ChatInterface.js         # Main chat component
├── package.json                 # Dependencies and scripts
└── next.config.js              # Next.js configuration
```

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

The frontend connects to the backend at `http://localhost:8000` by default. If your backend runs on a different port or domain, update the API URL in `components/ChatInterface.js`:

```javascript
const response = await fetch('http://your-backend-url/api/v1/chat', {
  // ... rest of the configuration
})
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

## Component Overview

### ChatInterface.js

The main chat component handles:
- **Message Management**: Stores and displays conversation history
- **Session Handling**: Maintains session ID for conversation continuity
- **API Communication**: Sends messages to backend and processes responses
- **Loading States**: Shows "Thinking..." indicator during processing
- **Error Handling**: Graceful error handling with user-friendly messages

#### Key State Variables

```javascript
const [messages, setMessages] = useState([])      // Conversation history
const [inputText, setInputText] = useState('')    // Current user input
const [isLoading, setIsLoading] = useState(false) // Loading state
const [sessionId, setSessionId] = useState(null)  // Session identifier
```

#### Message Flow

1. User types message and presses Enter or clicks Send
2. Message is added to conversation history
3. Request sent to backend with message and session ID
4. Loading state displayed
5. Response received and added to conversation
6. Session ID stored for future requests

## Styling

### CSS Architecture

The application uses a clean, modern design with:
- **Color Scheme**: Blue primary (#2563eb) with neutral grays
- **Layout**: Flexbox-based responsive design
- **Typography**: Clean Arial font family
- **Message Bubbles**: Rounded corners with distinct colors for user/bot
- **Responsive**: Adapts to different screen sizes

### Key Style Classes

- `.chat-container`: Main chat layout container
- `.chat-header`: Top header with title and session info
- `.chat-messages`: Scrollable message area
- `.message.user`: User message styling (blue, right-aligned)
- `.message.bot`: Bot message styling (gray, left-aligned)
- `.chat-input`: Input area with text field and send button

## API Integration

### Request Format

```javascript
{
  message: "User's message text",
  session_id: "optional-session-identifier"
}
```

### Response Format

```javascript
{
  response: "Bot's response text",
  session_id: "session-identifier",
  context: {
    intent: "search|filter|general",
    search_count: 5,
    conversation_length: 3,
    has_cached_results: true
  }
}
```

### Error Handling

The frontend gracefully handles:
- Network connection errors
- Backend server errors
- Invalid response formats
- Timeout scenarios

## Development

### Adding New Features

1. **New Components**: Add to `components/` directory
2. **Styling**: Update `app/globals.css` or create component-specific CSS
3. **API Integration**: Extend the fetch logic in `ChatInterface.js`
4. **State Management**: Add new state variables as needed

### Debugging

- **Console Logs**: The app logs API requests and responses
- **Session Tracking**: Session ID visible in the header
- **Network Tab**: Monitor API calls in browser dev tools
- **React DevTools**: Inspect component state and props

### Common Customizations

#### Change API Endpoint
```javascript
// In ChatInterface.js
const response = await fetch('http://your-new-endpoint/api/v1/chat', {
  // ... configuration
})
```

#### Modify Styling
```css
/* In globals.css */
.chat-container {
  max-width: 1000px; /* Increase chat width */
}

.message.user {
  background-color: #your-color; /* Change user message color */
}
```

#### Add New Message Types
```javascript
// In ChatInterface.js
const messageTypes = {
  user: 'user',
  bot: 'bot',
  system: 'system', // New type
  error: 'error'    // New type
}
```

## Scripts

- `npm run dev`: Start development server
- `npm run build`: Create production build
- `npm start`: Start production server
- `npm run lint`: Run ESLint for code quality

## Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile**: iOS Safari, Android Chrome
- **Features Used**: ES6+, Fetch API, CSS Grid/Flexbox

## Performance Considerations

- **Message History**: Keeps full conversation in memory
- **API Calls**: Debouncing could be added for rapid message sending
- **Rendering**: React's virtual DOM optimizes re-renders
- **Bundle Size**: Minimal dependencies for fast loading

## Deployment

### Static Hosting (Recommended)
```bash
npm run build
# Deploy the .next folder to your static hosting service
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables
For production deployments, you may want to use environment variables for the backend URL:

```javascript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```
