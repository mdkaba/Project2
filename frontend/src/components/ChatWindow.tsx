import React, { useEffect, useRef } from 'react';
import { Box, Flex, Text, Spinner } from '@chakra-ui/react';
import ChatMessage from './ChatMessage';
import { Message } from '../types/chat';
import { COLORS } from '../utils/constants';

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Box 
      flex="1" 
      overflow="auto" 
      display="flex" 
      flexDirection="column"
      bg={COLORS.white}
    >
      {messages.length === 0 ? (
        <Flex 
          flex="1" 
          align="center" 
          justify="center" 
          p={8}
          color={COLORS.darkGray}
          flexDirection="column"
        >
          <Text fontSize="2xl" mb={4} fontWeight="bold" color={COLORS.burgundy}>
            Concordia AI Assistant
          </Text>
          <Text fontSize="md" maxW="550px" textAlign="center">
            Ask me anything about Concordia University, computer science, artificial intelligence, 
            or any other topic you'd like assistance with.
          </Text>
        </Flex>
      ) : (
        <Box>
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <Box p={4} textAlign="center">
              <Spinner 
                thickness="4px"
                speed="0.65s"
                emptyColor="gray.200"
                color={COLORS.burgundy}
                size="md"
              />
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>
      )}
    </Box>
  );
};

export default ChatWindow; 