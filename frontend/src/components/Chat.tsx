import React, { useState, useEffect, useCallback } from 'react';
import { Box, Flex, useBreakpointValue } from '@chakra-ui/react';
import { v4 as uuidv4 } from 'uuid';
import Sidebar from './Sidebar';
import ChatWindow from './ChatWindow';
import ChatInput from './ChatInput';
import WelcomeScreen from './WelcomeScreen';
import { Message, Conversation } from '../types/chat';
import { chatApi } from '../services/api';
import { useDisclosure } from '../hooks/useDisclosure';
import { useToast } from '../hooks/useToast';

const Chat: React.FC = () => {
  // State
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Mobile sidebar control
  const { isOpen, onOpen, onClose, onToggle } = useDisclosure();
  const isMobile = useBreakpointValue({ base: true, md: false }) || false;

  // Toast for error notifications
  const toast = useToast();

  // Helper to get current conversation
  const currentConversation = useCallback(() => {
    if (!currentConversationId) return null;
    return conversations.find(c => c.id === currentConversationId) || null;
  }, [conversations, currentConversationId]);

  // Create a new conversation
  const createNewConversation = useCallback(() => {
    const newId = uuidv4();
    const newConversation: Conversation = {
      id: newId,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    setConversations(prev => [...prev, newConversation]);
    setCurrentConversationId(newId);
    
    if (isMobile) {
      onClose(); // Close sidebar on mobile when creating a new conversation
    }
    
    return newId;
  }, [isMobile, onClose]);

  // Select a conversation
  const selectConversation = useCallback((id: string) => {
    setCurrentConversationId(id);
    
    if (isMobile) {
      onClose(); // Close sidebar on mobile when selecting a conversation
    }
  }, [isMobile, onClose]);

  // Send a message
  const sendMessage = useCallback(async (message: string) => {
    // Create a new conversation if needed
    let conversationId = currentConversationId;
    if (!conversationId) {
      conversationId = createNewConversation();
    }
    
    // Create user message
    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    
    // Add user message to conversation
    setConversations(prev => {
      return prev.map(c => {
        if (c.id === conversationId) {
          return {
            ...c,
            messages: [...c.messages, userMessage],
            updatedAt: new Date(),
            title: c.messages.length === 0 ? message.substring(0, 30) : c.title,
          };
        }
        return c;
      });
    });
    
    // Set loading state
    setIsLoading(true);
    setError(null);
    
    try {
      // Make API request
      const response = await chatApi.sendMessage({
        query: message,
        conversation_id: conversationId,
      });
      
      // Create assistant message
      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        agent_name: response.agent_name,
      };
      
      // Add assistant message to conversation
      setConversations(prev => {
        return prev.map(c => {
          if (c.id === conversationId) {
            return {
              ...c,
              messages: [...c.messages, assistantMessage],
              updatedAt: new Date(),
            };
          }
          return c;
        });
      });
    } catch (err) {
      // Handle error
      const errorMessage = 'Failed to get response. Please try again.';
      setError(errorMessage);
      
      toast({
        title: 'Error',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  }, [createNewConversation, currentConversationId, toast]);

  useEffect(() => {
    // Initialize with a new conversation
    if (conversations.length === 0) {
      createNewConversation();
    }
  }, [conversations.length, createNewConversation]);

  // Display welcome screen if no conversation is in progress
  const currentMessages = currentConversation()?.messages || [];
  if (currentMessages.length === 0) {
    return <WelcomeScreen onSendMessage={sendMessage} isLoading={isLoading} />;
  }

  return (
    <Flex h="100vh" overflow="hidden">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onNewConversation={createNewConversation}
        onSelectConversation={selectConversation}
        isMobile={isMobile}
        isOpen={isOpen}
        onToggle={onToggle}
      />
      
      {/* Chat Area */}
      <Flex
        flex="1"
        direction="column"
        h="100vh"
        overflow="hidden"
      >
        {/* Chat messages */}
        <ChatWindow
          messages={currentMessages}
          isLoading={isLoading}
        />
        
        {/* Input area */}
        <ChatInput
          onSendMessage={sendMessage}
          isLoading={isLoading}
        />
      </Flex>
    </Flex>
  );
};

export default Chat; 