'use client'

import { useState, useRef, useEffect } from 'react'

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { 
      type: 'bot', 
      text: '👋 Hi there! I\'m your AI camp search assistant. I\'m here to help you find the perfect summer camp for your child. Just send me a message to get started!',
      isGreeting: true
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [currentStep, setCurrentStep] = useState('name')
  const [profileData, setProfileData] = useState({})
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage = { type: 'user', text: inputText }
    setMessages(prev => [...prev, userMessage])
    
    const currentInput = inputText
    setInputText('')
    setIsLoading(true)

    try {
      const requestBody = {
        message: currentInput,
        session_id: sessionId
      }

      console.log('🚀 Sending request:', { 
        message: currentInput, 
        session_id: sessionId ? sessionId.slice(-8) : 'new' 
      })

      const response = await fetch('http://localhost:8001/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      })

      if (response.ok) {
        const data = await response.json()
        
        if (data.session_id && data.session_id !== sessionId) {
          setSessionId(data.session_id)
          console.log('💾 Session ID stored:', data.session_id.slice(-8))
        }

        // Check if this is a profile collection step
        const isProfileStep = data.response && (
          data.response.includes('What\'s your name?') ||
          data.response.includes('What\'s your child\'s name?') ||
          data.response.includes('How old is') ||
          data.response.includes('What grade is') ||
          data.response.includes('What are') && data.response.includes('interests?') ||
          data.response.includes('Where are you located?') ||
          data.response.includes('maximum driving distance')
        )

        // Check if profile collection is complete
        const isProfileComplete = data.response && data.response.includes('Thank you for providing your information!')

        // Check if this is a search result
        const isSearchResult = data.response && (
          data.response.includes('Found') && data.response.includes('camps') ||
          data.response.includes('Perfect! I\'m preparing a search') ||
          data.response.includes('Great! I found')
        )

        const botMessage = { 
          type: 'bot', 
          text: data.response || 'Sorry, I encountered an error.',
          isProfileStep: isProfileStep,
          isProfileComplete: isProfileComplete,
          isSearchResult: isSearchResult
        }
        
        setMessages(prev => [...prev, botMessage])

        // Update current step based on response
        if (data.response) {
          if (data.response.includes('What\'s your name?')) {
            setCurrentStep('name')
          } else if (data.response.includes('What\'s your child\'s name?')) {
            setCurrentStep('child_name')
          } else if (data.response.includes('How old is')) {
            setCurrentStep('child_age')
          } else if (data.response.includes('What grade is')) {
            setCurrentStep('child_grade')
          } else if (data.response.includes('What are') && data.response.includes('interests?')) {
            setCurrentStep('interests')
          } else if (data.response.includes('Where are you located?')) {
            setCurrentStep('address')
          } else if (data.response.includes('maximum driving distance')) {
            setCurrentStep('distance')
          }
        }

      } else {
        throw new Error('Network response was not ok')
      }
    } catch (error) {
      console.error('❌ Error:', error)
      const errorMessage = { 
        type: 'bot', 
        text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      sendMessage()
    }
  }

  const formatMessage = (message) => {
    if (message.isError) {
      return <div className="error-message">{message.text}</div>
    }

    if (message.isGreeting) {
      return (
        <div className="greeting-message">
          <div className="greeting-icon">👋</div>
          <p>{message.text}</p>
        </div>
      )
    }

    if (message.isProfileComplete) {
      return (
        <div className="profile-complete">
          <div className="profile-summary">
            <h3>🎉 Profile Complete!</h3>
            <p>{message.text}</p>
          </div>
          <div className="next-steps">
            <p>Type "continue" to search for camps, or ask me anything else!</p>
          </div>
        </div>
      )
    }

    if (message.isSearchResult) {
      return (
        <div className="search-result">
          <div className="search-info">
            <p>{message.text}</p>
          </div>
          <div className="search-actions">
            <p>Type "search" to execute the search, or "format" to see formatted results.</p>
          </div>
        </div>
      )
    }

    if (message.isProfileStep) {
      return (
        <div className="profile-step">
          <div className="step-indicator">
            {currentStep === 'name' && '👤 Step 1: Parent Name'}
            {currentStep === 'child_name' && '👶 Step 2: Child Name'}
            {currentStep === 'child_age' && '🎂 Step 3: Child Age'}
            {currentStep === 'child_grade' && '📚 Step 4: Child Grade'}
            {currentStep === 'interests' && '🎯 Step 5: Interests'}
            {currentStep === 'address' && '📍 Step 6: Location'}
            {currentStep === 'distance' && '🚗 Step 7: Max Distance'}
          </div>
          <p>{message.text}</p>
        </div>
      )
    }

    return <p>{message.text}</p>
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🏕️ Summer Camp Assistant</h1>
        <p>Your AI-powered camp search companion</p>
        {sessionId && (
          <div className="session-info">
            Session: {sessionId.slice(-8)}
          </div>
        )}
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            {formatMessage(message)}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="loading">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={
            currentStep === 'name' ? 'Enter your name...' :
            currentStep === 'child_name' ? 'Enter your child\'s name...' :
            currentStep === 'child_age' ? 'Enter age (4-18)...' :
            currentStep === 'child_grade' ? 'Enter grade (0-12)...' :
            currentStep === 'interests' ? 'Enter interests (separate with commas)...' :
            currentStep === 'address' ? 'Enter your address...' :
            currentStep === 'distance' ? 'Enter max distance in miles...' :
            'Ask me about summer camps...'
          }
          disabled={isLoading}
        />
        <button 
          onClick={sendMessage}
          disabled={isLoading || !inputText.trim()}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
