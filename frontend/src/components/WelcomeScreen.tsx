import React, { useState } from 'react';
import { Box, VStack, Text, Container, Flex } from '@chakra-ui/react';
import ConcordiaLogo from './ConcordiaLogo';
import ChatInput from './ChatInput';
import { COLORS } from '../utils/constants';

interface WelcomeScreenProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onSendMessage, isLoading }) => {
  return (
    <Box 
      display="flex" 
      flexDirection="column" 
      alignItems="center" 
      justifyContent="center" 
      minH="100vh"
      bg={COLORS.white}
      position="relative"
    >
      {/* Branding header */}
      <Box 
        position="absolute" 
        top="0" 
        left="0" 
        width="100%"
        p={6} 
        display="flex" 
        justifyContent="center"
      >
        <ConcordiaLogo size="lg" />
      </Box>
      
      {/* Central content */}
      <Container maxW="800px" py={16} px={4} textAlign="center">
        <VStack gap={8} mb={12}>
          <Text 
            fontSize={{ base: '3xl', md: '4xl' }} 
            fontWeight="bold" 
            color={COLORS.burgundy}
          >
            What can I help with?
          </Text>
          
          <Text fontSize={{ base: 'md', md: 'lg' }} color={COLORS.darkGray}>
            Ask me anything about Concordia University, computer science, artificial intelligence,
            or other topics you'd like assistance with.
          </Text>
        </VStack>
        
        {/* Examples (could be added in the future) */}
        <Box mb={8}>
          {/* Suggestion buttons would go here */}
        </Box>
      </Container>
      
      {/* Input box */}
      <Box 
        position="fixed" 
        bottom="0"
        left="0" 
        width="100%" 
        p={4}
        bg={COLORS.white}
        borderTop={`1px solid ${COLORS.lightGray}`}
      >
        <ChatInput 
          onSendMessage={onSendMessage} 
          isLoading={isLoading} 
          placeholder="Ask a question..." 
        />
      </Box>
    </Box>
  );
};

export default WelcomeScreen; 