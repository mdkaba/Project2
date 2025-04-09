import { useState, useEffect, useRef } from 'react';
import { COLORS } from './utils/constants';
import axios from 'axios';

// Simple Message type
interface SimpleMessage {
  id: string;
  content: string;
  isUser: boolean;
  agentName?: string;
}

// CSS styles
const styles = {
  container: {
    height: '100vh',
    width: '100%', 
    display: 'flex',
    flexDirection: 'column' as const,
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f9f9f9',
  },
  chatContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    flex: 1,
    width: '100%',
    maxWidth: '800px',
    margin: '0 auto',
    height: '100%',
    position: 'relative' as const,
    backgroundColor: '#ffffff',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
  },
  welcomeContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    width: '100%',
    padding: '20px',
  },
  welcomeContent: {
    maxWidth: '600px',
    width: '100%',
    textAlign: 'center' as const,
    padding: '40px 20px',
  },
  header: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: COLORS.burgundy,
    marginBottom: '24px',
  },
  description: {
    fontSize: '16px',
    marginBottom: '32px',
    color: '#555',
    lineHeight: 1.5,
  },
  inputContainer: {
    display: 'flex',
    width: '100%',
    maxWidth: '800px',
    margin: '0 auto',
    padding: '16px',
    borderTop: '1px solid #e6e6e6',
    backgroundColor: '#fff',
    position: 'sticky' as const,
    bottom: 0,
    zIndex: 10,
  },
  input: {
    flex: 1,
    padding: '12px 16px',
    borderRadius: '6px',
    border: '1px solid #d9d9e3',
    fontSize: '16px',
    backgroundColor: '#fff',
    marginRight: '10px',
    outline: 'none',
  },
  button: {
    padding: '0 16px',
    backgroundColor: COLORS.burgundy,
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '16px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  buttonHover: {
    backgroundColor: '#701a2b',
  },
  messageContainer: {
    flex: 1,
    padding: '20px',
    overflow: 'auto',
    display: 'flex',
    flexDirection: 'column' as const,
  },
  messageWrapper: {
    display: 'flex',
    flexDirection: 'column' as const,
    width: '100%',
    padding: '10px 0',
    borderBottom: '1px solid #f0f0f0',
  },
  message: (isUser: boolean) => ({
    alignSelf: isUser ? 'flex-end' : 'flex-start',
    maxWidth: '90%',
    padding: '0',
  }),
  messageContent: {
    padding: '8px 12px',
    borderRadius: '6px',
    fontSize: '16px',
    lineHeight: 1.5,
  },
  userMessageContent: {
    backgroundColor: '#f7f7f8',
    color: '#000',
  },
  assistantMessageContent: {
    backgroundColor: '#fff',
    color: '#000',
  },
  agentName: {
    fontSize: '12px',
    color: COLORS.darkGray,
    marginBottom: '4px',
    fontWeight: 'bold',
  },
  errorMessage: {
    padding: '12px',
    backgroundColor: '#fef1f1',
    border: '1px solid #f9d7d7',
    borderRadius: '6px',
    color: '#be3a3a',
    margin: '8px 0',
  },
  loadingIndicator: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '10px',
  },
  dots: {
    display: 'flex',
    gap: '4px',
  },
  dot: (delay: number) => ({
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: COLORS.burgundy,
    opacity: 0.6,
    animation: 'pulse 1.5s infinite ease-in-out',
    animationDelay: `${delay}s`,
  }),
  agentTypeBadge: (agentType: string) => {
    let color = COLORS.beige; // default color for GeneralAgent
    
    if (agentType === 'AdmissionsAgent') {
      color = COLORS.burgundy;
    } else if (agentType === 'AIExpertAgent') {
      color = COLORS.gold;
    }
    
    return {
      display: 'inline-block',
      backgroundColor: color,
      color: color === COLORS.beige ? '#333' : '#fff',
      padding: '2px 8px',
      borderRadius: '12px',
      fontSize: '12px',
      marginLeft: '8px',
      fontWeight: 'bold',
    };
  },
};

export const SimpleChat = () => {
  const [messages, setMessages] = useState<SimpleMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Send a message
  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    
    // Clear any previous errors
    setError(null);
    
    // Create unique ID
    const messageId = Date.now().toString();
    
    // Add user message
    const userMessage = {
      id: messageId,
      content: inputValue,
      isUser: true
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    try {
      // API call using axios instead of fetch
      const response = await axios.post('http://localhost:8000/api/v1/chat/', {
        query: inputValue,
        conversation_id: conversationId,
        metadata: {} // Add empty metadata to match API schema
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        }
      });
      
      const data = response.data;
      
      // Save conversation ID for follow-up messages
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }
      
      // Add bot message
      const botMessage = {
        id: Date.now().toString(),
        content: data.response,
        isUser: false,
        agentName: data.agent_name
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      if (axios.isAxiosError(error)) {
        setError(`Error: ${error.message}${error.response ? ` (${error.response.status})` : ''}`);
      } else {
        setError(`Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getAgentDisplayName = (agentName: string) => {
    switch(agentName) {
      case 'AdmissionsAgent':
        return 'Admissions';
      case 'AIExpertAgent':
        return 'AI Expert';
      case 'GeneralAgent':
        return 'General Assistant';
      default:
        return agentName;
    }
  };

  // LoadingDots component
  const LoadingDots = () => (
    <div style={styles.loadingIndicator}>
      <div style={styles.dots}>
        <div style={styles.dot(0)}></div>
        <div style={styles.dot(0.2)}></div>
        <div style={styles.dot(0.4)}></div>
      </div>
    </div>
  );

  // If no messages, show welcome screen
  if (messages.length === 0) {
    return (
      <div style={styles.container}>
        <div style={styles.welcomeContainer}>
          <div style={styles.welcomeContent}>
            <h1 style={styles.header}>Concordia AI Assistant</h1>
            <p style={styles.description}>
              Ask me anything about Concordia University, computer science, artificial intelligence, 
              or any other topic you'd like assistance with.
            </p>
            <div style={styles.inputContainer}>
              <input
                style={styles.input}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                onKeyDown={handleKeyPress}
                disabled={isLoading}
              />
              <button 
                style={{
                  ...styles.button,
                  ...(isLoading ? {} : { ':hover': styles.buttonHover })
                }}
                onClick={sendMessage}
                disabled={isLoading}
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
            {error && <div style={styles.errorMessage}>{error}</div>}
          </div>
        </div>
      </div>
    );
  }

  // Show chat interface
  return (
    <div style={styles.container}>
      <div style={styles.chatContainer}>
        <div style={styles.messageContainer}>
          {messages.map((msg) => (
            <div 
              key={msg.id} 
              style={styles.messageWrapper}
            >
              <div style={styles.message(msg.isUser)}>
                {!msg.isUser && msg.agentName && (
                  <div style={styles.agentName}>
                    {getAgentDisplayName(msg.agentName)}
                    <span style={styles.agentTypeBadge(msg.agentName)}></span>
                  </div>
                )}
                <div 
                  style={{
                    ...styles.messageContent,
                    ...(msg.isUser ? styles.userMessageContent : styles.assistantMessageContent)
                  }}
                >
                  {msg.content}
                </div>
              </div>
            </div>
          ))}
          {isLoading && <LoadingDots />}
          {error && <div style={styles.errorMessage}>{error}</div>}
          <div ref={messagesEndRef} />
        </div>
        
        <div style={styles.inputContainer}>
          <input
            style={styles.input}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={handleKeyPress}
            disabled={isLoading}
          />
          <button 
            style={styles.button}
            onClick={sendMessage}
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}; 