'use client'

import { useState } from 'react'

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hi! I can help you find the perfect summer camp for your child. What are you looking for?' }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)

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

      const response = await fetch('http://localhost:8000/api/v1/chat', {
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
        

        if (data.context) {
          console.log('📊 Context:', {
            intent: data.context.intent,
            search_count: data.context.search_count,
            conversation_length: data.context.conversation_length,
            has_cached_results: data.context.has_cached_results
          })
        }
        
        const botMessage = { type: 'bot', text: data.response || 'Sorry, I encountered an error.' }
        setMessages(prev => [...prev, botMessage])
      } else {
        throw new Error('Network response was not ok')
      }
    } catch (error) {
      console.error('❌ Error:', error)
      const errorMessage = { type: 'bot', text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.' }
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

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Summer Camp Assistant</h1>
        {sessionId && (
          <div className="session-info">
            Session: {sessionId.slice(-8)}
          </div>
        )}
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            {message.text}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            Thinking...
          </div>
        )}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me about summer camps..."
          disabled={isLoading}
        />
        <button 
          onClick={sendMessage}
          disabled={isLoading || !inputText.trim()}
        >
          Send
        </button>
      </div>
    </div>
  )
}
